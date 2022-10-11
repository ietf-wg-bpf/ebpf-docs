.. contents::
.. sectnum::

=====================
BPF Type Format (BTF)
=====================

This file contains Linux-specific additions and clarifications
to the base BTF specification.

BTF Structures
=================
The file ``include/uapi/linux/btf.h`` provides high-level definition of how
types/strings are encoded.

The beginning of data blob must be::

    struct btf_header {
        __u16   magic;
        __u8    version;
        __u8    flags;
        __u32   hdr_len;

        /* All offsets are in bytes relative to the end of this header */
        __u32   type_off;       /* offset of type section       */
        __u32   type_len;       /* length of type section       */
        __u32   str_off;        /* offset of string section     */
        __u32   str_len;        /* length of string section     */
    };

The ``btf_header`` is designed to be extensible with
``hdr_len`` equal to ``sizeof(struct btf_header)`` when a data blob is
generated.


BTF Kernel API
=================

The following bpf syscall command involves BTF:
   * BPF_BTF_LOAD: load a blob of BTF data into kernel
   * BPF_MAP_CREATE: map creation with btf key and value type info.
   * BPF_PROG_LOAD: prog load with btf function and line info.
   * BPF_BTF_GET_FD_BY_ID: get a btf fd
   * BPF_OBJ_GET_INFO_BY_FD: btf, func_info, line_info
     and other btf related info are returned.

The workflow typically looks like:
::

  Application:
      BPF_BTF_LOAD
          |
          v
      BPF_MAP_CREATE and BPF_PROG_LOAD
          |
          V
      ......

  Introspection tool:
      ......
      BPF_{PROG,MAP}_GET_NEXT_ID (get prog/map id's)
          |
          V
      BPF_{PROG,MAP}_GET_FD_BY_ID (get a prog/map fd)
          |
          V
      BPF_OBJ_GET_INFO_BY_FD (get bpf_prog_info/bpf_map_info with btf_id)
          |                                     |
          V                                     |
      BPF_BTF_GET_FD_BY_ID (get btf_fd)         |
          |                                     |
          V                                     |
      BPF_OBJ_GET_INFO_BY_FD (get btf)          |
          |                                     |
          V                                     V
      pretty print types, dump func signatures and line info, etc.


BPF_BTF_LOAD
----------------

Load a blob of BTF data into kernel. A blob of data, described in
:ref:`BTF_Type_String`, can be directly loaded into the kernel. A ``btf_fd``
is returned to a userspace.

BPF_MAP_CREATE
------------------

A map can be created with ``btf_fd`` and specified key/value type id.::

    __u32   btf_fd;         /* fd pointing to a BTF type data */
    __u32   btf_key_type_id;        /* BTF type_id of the key */
    __u32   btf_value_type_id;      /* BTF type_id of the value */

In libbpf, the map can be defined with extra annotation like below:
::

    struct {
        __uint(type, BPF_MAP_TYPE_ARRAY);
        __type(key, int);
        __type(value, struct ipv_counts);
        __uint(max_entries, 4);
    } btf_map SEC(".maps");

During ELF parsing, libbpf is able to extract key/value type_id's and assign
them to BPF_MAP_CREATE attributes automatically.

.. _BPF_Prog_Load:

BPF_PROG_LOAD
-----------------

During prog_load, func_info and line_info can be passed to kernel with proper
values for the following attributes:
::

    __u32           insn_cnt;
    __aligned_u64   insns;
    ......
    __u32           prog_btf_fd;    /* fd pointing to BTF type data */
    __u32           func_info_rec_size;     /* userspace bpf_func_info size */
    __aligned_u64   func_info;      /* func info */
    __u32           func_info_cnt;  /* number of bpf_func_info records */
    __u32           line_info_rec_size;     /* userspace bpf_line_info size */
    __aligned_u64   line_info;      /* line info */
    __u32           line_info_cnt;  /* number of bpf_line_info records */

The func_info and line_info are an array of 
`Function Record <elf.rst#1443function-record>`_ and
`Line Record <elf.rst#1445line-record>`_ elements,
respectively.::

    struct bpf_func_info {
        __u32   insn_off; /* [0, insn_cnt - 1] */
        __u32   type_id;  /* pointing to a BTF_KIND_FUNC type */
    };
    struct bpf_line_info {
        __u32   insn_off; /* [0, insn_cnt - 1] */
        __u32   file_name_off; /* offset to string table for the filename */
        __u32   line_off; /* offset to string table for the source line */
        __u32   line_col; /* line number and column number */
    };

func_info_rec_size is the size of each func_info record, and
line_info_rec_size is the size of each line_info record. Passing the record
size to kernel make it possible to extend the record itself in the future.

Below are requirements for func_info:
  * func_info[0].insn_off must be 0.
  * the func_info insn_off is in strictly increasing order and matches
    bpf func boundaries.

Below are requirements for line_info:
  * the first insn in each func must have a line_info record pointing to it.
  * the line_info insn_off is in strictly increasing order.

For line_info, the line number and column number are defined as below:
::

    #define BPF_LINE_INFO_LINE_NUM(line_col)        ((line_col) >> 10)
    #define BPF_LINE_INFO_LINE_COL(line_col)        ((line_col) & 0x3ff)

BPF_{PROG,MAP}_GET_NEXT_ID
------------------------------

In kernel, every loaded program, map or btf has a unique id. The id won't
change during the lifetime of a program, map, or btf.

The bpf syscall command BPF_{PROG,MAP}_GET_NEXT_ID returns all id's, one for
each command, to user space, for bpf program or maps, respectively, so an
inspection tool can inspect all programs and maps.

BPF_{PROG,MAP}_GET_FD_BY_ID
-------------------------------

An introspection tool cannot use id to get details about program or maps.
A file descriptor needs to be obtained first for reference-counting purpose.

BPF_OBJ_GET_INFO_BY_FD
--------------------------

Once a program/map fd is acquired, an introspection tool can get the detailed
information from kernel about this fd, some of which are BTF-related. For
example, ``bpf_map_info`` returns ``btf_id`` and key/value type ids.
``bpf_prog_info`` returns ``btf_id``, func_info, and line info for translated
bpf byte codes, and jited_line_info.

BPF_BTF_GET_FD_BY_ID
------------------------

With ``btf_id`` obtained in ``bpf_map_info`` and ``bpf_prog_info``, bpf
syscall command BPF_BTF_GET_FD_BY_ID can retrieve a btf fd. Then, with
command BPF_OBJ_GET_INFO_BY_FD, the btf blob, originally loaded into the
kernel with BPF_BTF_LOAD, can be retrieved.

With the btf blob, ``bpf_map_info``, and ``bpf_prog_info``, an introspection
tool has full btf knowledge and is able to pretty print map key/values, dump
func signatures and line info, along with byte/jit codes.

Using BTF
============

bpftool map pretty print
----------------------------

With BTF, the map key/value can be printed based on fields rather than simply
raw bytes. This is especially valuable for large structure or if your data
structure has bitfields. For example, for the following map,::

      enum A { A1, A2, A3, A4, A5 };
      typedef enum A ___A;
      struct tmp_t {
           char a1:4;
           int  a2:4;
           int  :4;
           __u32 a3:4;
           int b;
           ___A b1:4;
           enum A b2:4;
      };
      struct {
           __uint(type, BPF_MAP_TYPE_ARRAY);
           __type(key, int);
           __type(value, struct tmp_t);
           __uint(max_entries, 1);
      } tmpmap SEC(".maps");

bpftool is able to pretty print like below:
::

      [{
            "key": 0,
            "value": {
                "a1": 0x2,
                "a2": 0x4,
                "a3": 0x6,
                "b": 7,
                "b1": 0x8,
                "b2": 0xa
            }
        }
      ]

bpftool prog dump
---------------------

The following is an example showing how func_info and line_info can help prog
dump with better kernel symbol names, function prototypes and line
information.::

    $ bpftool prog dump jited pinned /sys/fs/bpf/test_btf_haskv
    [...]
    int test_long_fname_2(struct dummy_tracepoint_args * arg):
    bpf_prog_44a040bf25481309_test_long_fname_2:
    ; static int test_long_fname_2(struct dummy_tracepoint_args *arg)
       0:   push   %rbp
       1:   mov    %rsp,%rbp
       4:   sub    $0x30,%rsp
       b:   sub    $0x28,%rbp
       f:   mov    %rbx,0x0(%rbp)
      13:   mov    %r13,0x8(%rbp)
      17:   mov    %r14,0x10(%rbp)
      1b:   mov    %r15,0x18(%rbp)
      1f:   xor    %eax,%eax
      21:   mov    %rax,0x20(%rbp)
      25:   xor    %esi,%esi
    ; int key = 0;
      27:   mov    %esi,-0x4(%rbp)
    ; if (!arg->sock)
      2a:   mov    0x8(%rdi),%rdi
    ; if (!arg->sock)
      2e:   cmp    $0x0,%rdi
      32:   je     0x0000000000000070
      34:   mov    %rbp,%rsi
    ; counts = bpf_map_lookup_elem(&btf_map, &key);
    [...]

Verifier Log
----------------

The following is an example of how line_info can help debugging verification
failure.::

       /* The code at tools/testing/selftests/bpf/test_xdp_noinline.c
        * is modified as below.
        */
       data = (void *)(long)xdp->data;
       data_end = (void *)(long)xdp->data_end;
       /*
       if (data + 4 > data_end)
               return XDP_DROP;
       */
       *(u32 *)data = dst->dst;

    $ bpftool prog load ./test_xdp_noinline.o /sys/fs/bpf/test_xdp_noinline type xdp
        ; data = (void *)(long)xdp->data;
        224: (79) r2 = *(u64 *)(r10 -112)
        225: (61) r2 = *(u32 *)(r2 +0)
        ; *(u32 *)data = dst->dst;
        226: (63) *(u32 *)(r2 +0) = r1
        invalid access to packet, off=0 size=4, R2(id=0,off=0,r=0)
        R2 offset is outside of the packet

BTF Generation
=================

You need latest pahole

  https://git.kernel.org/pub/scm/devel/pahole/pahole.git/

or llvm (8.0 or later). The pahole acts as a dwarf2btf converter. It doesn't
support .BTF.ext and btf BTF_KIND_FUNC type yet. For example,::

      -bash-4.4$ cat t.c
      struct t {
        int a:2;
        int b:3;
        int c:2;
      } g;
      -bash-4.4$ gcc -c -O2 -g t.c
      -bash-4.4$ pahole -JV t.o
      File t.o:
      [1] STRUCT t kind_flag=1 size=4 vlen=3
              a type_id=2 bitfield_size=2 bits_offset=0
              b type_id=2 bitfield_size=3 bits_offset=2
              c type_id=2 bitfield_size=2 bits_offset=5
      [2] INT int size=4 bit_offset=0 nr_bits=32 encoding=SIGNED

The llvm is able to generate .BTF and .BTF.ext directly with -g for bpf target
only. The assembly code (-S) is able to show the BTF encoding in assembly
format.::

    -bash-4.4$ cat t2.c
    typedef int __int32;
    struct t2 {
      int a2;
      int (*f2)(char q1, __int32 q2, ...);
      int (*f3)();
    } g2;
    int main() { return 0; }
    int test() { return 0; }
    -bash-4.4$ clang -c -g -O2 -target bpf t2.c
    -bash-4.4$ readelf -S t2.o
      ......
      [ 8] .BTF              PROGBITS         0000000000000000  00000247
           000000000000016e  0000000000000000           0     0     1
      [ 9] .BTF.ext          PROGBITS         0000000000000000  000003b5
           0000000000000060  0000000000000000           0     0     1
      [10] .rel.BTF.ext      REL              0000000000000000  000007e0
           0000000000000040  0000000000000010          16     9     8
      ......
    -bash-4.4$ clang -S -g -O2 -target bpf t2.c
    -bash-4.4$ cat t2.s
      ......
            .section        .BTF,"",@progbits
            .short  60319                   # 0xeb9f
            .byte   1
            .byte   0
            .long   24
            .long   0
            .long   220
            .long   220
            .long   122
            .long   0                       # BTF_KIND_FUNC_PROTO(id = 1)
            .long   218103808               # 0xd000000
            .long   2
            .long   83                      # BTF_KIND_INT(id = 2)
            .long   16777216                # 0x1000000
            .long   4
            .long   16777248                # 0x1000020
      ......
            .byte   0                       # string offset=0
            .ascii  ".text"                 # string offset=1
            .byte   0
            .ascii  "/home/yhs/tmp-pahole/t2.c" # string offset=7
            .byte   0
            .ascii  "int main() { return 0; }" # string offset=33
            .byte   0
            .ascii  "int test() { return 0; }" # string offset=58
            .byte   0
            .ascii  "int"                   # string offset=83
      ......
            .section        .BTF.ext,"",@progbits
            .short  60319                   # 0xeb9f
            .byte   1
            .byte   0
            .long   24
            .long   0
            .long   28
            .long   28
            .long   44
            .long   8                       # FuncInfo
            .long   1                       # FuncInfo section string offset=1
            .long   2
            .long   .Lfunc_begin0
            .long   3
            .long   .Lfunc_begin1
            .long   5
            .long   16                      # LineInfo
            .long   1                       # LineInfo section string offset=1
            .long   2
            .long   .Ltmp0
            .long   7
            .long   33
            .long   7182                    # Line 7 Col 14
            .long   .Ltmp3
            .long   7
            .long   58
            .long   8206                    # Line 8 Col 14

Testing
==========

Kernel bpf selftest `test_btf.c` provides extensive set of BTF-related tests.
