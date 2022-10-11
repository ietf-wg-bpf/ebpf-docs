.. contents::
.. sectnum::

=====================
BPF Type Format (BTF)
=====================

Introduction
===============

BTF (BPF Type Format) is the metadata format which encodes the debug info
related to BPF program/map. The name BTF was used initially to describe data
types. The BTF was later extended to include function info for defined
subroutines, and line info for source/line information.

The debug info is used for map pretty print, function signature, etc. The
function signature enables better bpf program/function kernel symbol. The line
info helps generate source annotated translated byte code, jited code and
verifier log.

The BTF specification contains two parts,
  * BTF kernel API
  * BTF ELF file format

The kernel API is the contract between user space and kernel. The kernel
verifies the BTF info before using it. The ELF file format is a user space
contract between ELF file and libbpf loader.

The type and string sections are part of the BTF kernel API, describing the
debug info (mostly types related) referenced by the bpf program. These two
sections are discussed in details in :ref:`BTF_Type_String`.

.. _BTF_Type_String:

BTF Type and String Encoding
===============================

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

The magic is ``0xeB9F``, which has different encoding for big and little
endian systems, and can be used to test whether BTF is generated for big- or
little-endian target. The ``btf_header`` is designed to be extensible with
``hdr_len`` equal to ``sizeof(struct btf_header)`` when a data blob is
generated.

String Encoding
-------------------

The first string in the string section must be a null string. The rest of
string table is a concatenation of other null-terminated strings.

Type Encoding
-----------------

The type id ``0`` is reserved for ``void`` type. The type section is parsed
sequentially and type id is assigned to each recognized type starting from id
``1``. Currently, the following types are supported::

    #define BTF_KIND_INT            1       /* Integer      */
    #define BTF_KIND_PTR            2       /* Pointer      */
    #define BTF_KIND_ARRAY          3       /* Array        */
    #define BTF_KIND_STRUCT         4       /* Struct       */
    #define BTF_KIND_UNION          5       /* Union        */
    #define BTF_KIND_ENUM           6       /* Enumeration up to 32-bit values */
    #define BTF_KIND_FWD            7       /* Forward      */
    #define BTF_KIND_TYPEDEF        8       /* Typedef      */
    #define BTF_KIND_VOLATILE       9       /* Volatile     */
    #define BTF_KIND_CONST          10      /* Const        */
    #define BTF_KIND_RESTRICT       11      /* Restrict     */
    #define BTF_KIND_FUNC           12      /* Function     */
    #define BTF_KIND_FUNC_PROTO     13      /* Function Proto       */
    #define BTF_KIND_VAR            14      /* Variable     */
    #define BTF_KIND_DATASEC        15      /* Section      */
    #define BTF_KIND_FLOAT          16      /* Floating point       */
    #define BTF_KIND_DECL_TAG       17      /* Decl Tag     */
    #define BTF_KIND_TYPE_TAG       18      /* Type Tag     */
    #define BTF_KIND_ENUM64         19      /* Enumeration up to 64-bit values */

Note that the type section encodes debug info, not just pure types.
``BTF_KIND_FUNC`` is not a type, and it represents a defined subprogram.

Each type contains the following common data::

    struct btf_type {
        __u32 name_off;
        /* "info" bits arrangement
         * bits  0-15: vlen (e.g. # of struct's members)
         * bits 16-23: unused
         * bits 24-28: kind (e.g. int, ptr, array...etc)
         * bits 29-30: unused
         * bit     31: kind_flag, currently used by
         *             struct, union, fwd, enum and enum64.
         */
        __u32 info;
        /* "size" is used by INT, ENUM, STRUCT, UNION and ENUM64.
         * "size" tells the size of the type it is describing.
         *
         * "type" is used by PTR, TYPEDEF, VOLATILE, CONST, RESTRICT,
         * FUNC, FUNC_PROTO, DECL_TAG and TYPE_TAG.
         * "type" is a type_id referring to another type.
         */
        union {
                __u32 size;
                __u32 type;
        };
    };

For certain kinds, the common data are followed by kind-specific data. The
``name_off`` in ``struct btf_type`` specifies the offset in the string table.
The following sections detail encoding of each kind.

BTF_KIND_INT
~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
 * ``name_off``: any valid offset
 * ``info.kind_flag``: 0
 * ``info.kind``: BTF_KIND_INT
 * ``info.vlen``: 0
 * ``size``: the size of the int type in bytes.

``btf_type`` is followed by a ``u32`` with the following bits arrangement::

  #define BTF_INT_ENCODING(VAL)   (((VAL) & 0x0f000000) >> 24)
  #define BTF_INT_OFFSET(VAL)     (((VAL) & 0x00ff0000) >> 16)
  #define BTF_INT_BITS(VAL)       ((VAL)  & 0x000000ff)

The ``BTF_INT_ENCODING`` has the following attributes::

  #define BTF_INT_SIGNED  (1 << 0)
  #define BTF_INT_CHAR    (1 << 1)
  #define BTF_INT_BOOL    (1 << 2)

The ``BTF_INT_ENCODING()`` provides extra information: signedness, char, or
bool, for the int type. The char and bool encoding are mostly useful for
pretty print. At most one encoding can be specified for the int type.

The ``BTF_INT_BITS()`` specifies the number of actual bits held by this int
type. For example, a 4-bit bitfield encodes ``BTF_INT_BITS()`` equals to 4.
The ``btf_type.size * 8`` must be equal to or greater than ``BTF_INT_BITS()``
for the type. The maximum value of ``BTF_INT_BITS()`` is 128.

The ``BTF_INT_OFFSET()`` specifies the starting bit offset to calculate values
for this int. For example, a bitfield struct member has:

 * btf member bit offset 100 from the start of the structure,
 * btf member pointing to an int type,
 * the int type has ``BTF_INT_OFFSET() = 2`` and ``BTF_INT_BITS() = 4``

Then in the struct memory layout, this member will occupy ``4`` bits starting
from bits ``100 + 2 = 102``.

Alternatively, the bitfield struct member can be the following to access the
same bits as the above:

 * btf member bit offset 102,
 * btf member pointing to an int type,
 * the int type has ``BTF_INT_OFFSET() = 0`` and ``BTF_INT_BITS() = 4``

The original intention of ``BTF_INT_OFFSET()`` is to provide flexibility of
bitfield encoding. Currently, both llvm and pahole generate
``BTF_INT_OFFSET() = 0`` for all int types.

BTF_KIND_PTR
~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_PTR
  * ``info.vlen``: 0
  * ``type``: the pointee type of the pointer

No additional type data follow ``btf_type``.

BTF_KIND_ARRAY
~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_ARRAY
  * ``info.vlen``: 0
  * ``size/type``: 0, not used

``btf_type`` is followed by one ``struct btf_array``::

    struct btf_array {
        __u32   type;
        __u32   index_type;
        __u32   nelems;
    };

The ``struct btf_array`` encoding:
  * ``type``: the element type
  * ``index_type``: the index type
  * ``nelems``: the number of elements for this array (``0`` is also allowed).

The ``index_type`` can be any regular int type (``u8``, ``u16``, ``u32``,
``u64``, ``unsigned __int128``). The original design of including
``index_type`` follows DWARF, which has an ``index_type`` for its array type.
Currently in BTF, beyond type verification, the ``index_type`` is not used.

The ``struct btf_array`` allows chaining through element type to represent
multidimensional arrays. For example, for ``int a[5][6]``, the following type
information illustrates the chaining:

  * [1]: int
  * [2]: array, ``btf_array.type = [1]``, ``btf_array.nelems = 6``
  * [3]: array, ``btf_array.type = [2]``, ``btf_array.nelems = 5``

Currently, both pahole and llvm collapse multidimensional array into
one-dimensional array, e.g., for ``a[5][6]``, the ``btf_array.nelems`` is
equal to ``30``. This is because the original use case is map pretty print
where the whole array is dumped out so one-dimensional array is enough. As
more BTF usage is explored, pahole and llvm can be changed to generate proper
chained representation for multidimensional arrays.

BTF_KIND_STRUCT
~~~~~~~~~~~~~~~~~~~~~

BTF_KIND_UNION
~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0 or offset to a valid C identifier
  * ``info.kind_flag``: 0 or 1
  * ``info.kind``: BTF_KIND_STRUCT or BTF_KIND_UNION
  * ``info.vlen``: the number of struct/union members
  * ``info.size``: the size of the struct/union in bytes

``btf_type`` is followed by ``info.vlen`` number of ``struct btf_member``.::

    struct btf_member {
        __u32   name_off;
        __u32   type;
        __u32   offset;
    };

``struct btf_member`` encoding:
  * ``name_off``: offset to a valid C identifier
  * ``type``: the member type
  * ``offset``: <see below>

If the type info ``kind_flag`` is not set, the offset contains only bit offset
of the member. Note that the base type of the bitfield can only be int or enum
type. If the bitfield size is 32, the base type can be either int or enum
type. If the bitfield size is not 32, the base type must be int, and int type
``BTF_INT_BITS()`` encodes the bitfield size.

If the ``kind_flag`` is set, the ``btf_member.offset`` contains both member
bitfield size and bit offset. The bitfield size and bit offset are calculated
as below.::

  #define BTF_MEMBER_BITFIELD_SIZE(val)   ((val) >> 24)
  #define BTF_MEMBER_BIT_OFFSET(val)      ((val) & 0xffffff)

In this case, if the base type is an int type, it must be a regular int type:

  * ``BTF_INT_OFFSET()`` must be 0.
  * ``BTF_INT_BITS()`` must be equal to ``{1,2,4,8,16} * 8``.

The following kernel patch introduced ``kind_flag`` and explained why both
modes exist:

  https://github.com/torvalds/linux/commit/9d5f9f701b1891466fb3dbb1806ad97716f95cc3#diff-fa650a64fdd3968396883d2fe8215ff3

BTF_KIND_ENUM
~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0 or offset to a valid C identifier
  * ``info.kind_flag``: 0 for unsigned, 1 for signed
  * ``info.kind``: BTF_KIND_ENUM
  * ``info.vlen``: number of enum values
  * ``size``: 1/2/4/8

``btf_type`` is followed by ``info.vlen`` number of ``struct btf_enum``.::

    struct btf_enum {
        __u32   name_off;
        __s32   val;
    };

The ``btf_enum`` encoding:
  * ``name_off``: offset to a valid C identifier
  * ``val``: any value

If the original enum value is signed and the size is less than 4,
that value will be sign extended into 4 bytes. If the size is 8,
the value will be truncated into 4 bytes.

BTF_KIND_FWD
~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: offset to a valid C identifier
  * ``info.kind_flag``: 0 for struct, 1 for union
  * ``info.kind``: BTF_KIND_FWD
  * ``info.vlen``: 0
  * ``type``: 0

No additional type data follow ``btf_type``.

BTF_KIND_TYPEDEF
~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: offset to a valid C identifier
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_TYPEDEF
  * ``info.vlen``: 0
  * ``type``: the type which can be referred by name at ``name_off``

No additional type data follow ``btf_type``.

BTF_KIND_VOLATILE
~~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_VOLATILE
  * ``info.vlen``: 0
  * ``type``: the type with ``volatile`` qualifier

No additional type data follow ``btf_type``.

BTF_KIND_CONST
~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_CONST
  * ``info.vlen``: 0
  * ``type``: the type with ``const`` qualifier

No additional type data follow ``btf_type``.

BTF_KIND_RESTRICT
~~~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_RESTRICT
  * ``info.vlen``: 0
  * ``type``: the type with ``restrict`` qualifier

No additional type data follow ``btf_type``.

BTF_KIND_FUNC
~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: offset to a valid C identifier
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_FUNC
  * ``info.vlen``: linkage information (BTF_FUNC_STATIC, BTF_FUNC_GLOBAL
                   or BTF_FUNC_EXTERN)
  * ``type``: a BTF_KIND_FUNC_PROTO type

No additional type data follow ``btf_type``.

A BTF_KIND_FUNC defines not a type, but a subprogram (function) whose
signature is defined by ``type``. The subprogram is thus an instance of that
type. The BTF_KIND_FUNC may in turn be referenced by a func_info in the
:ref:`BTF_Ext_Section` (ELF) or in the arguments to :ref:`BPF_Prog_Load`
(ABI).

Currently, only linkage values of BTF_FUNC_STATIC and BTF_FUNC_GLOBAL are
supported in the kernel.

BTF_KIND_FUNC_PROTO
~~~~~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_FUNC_PROTO
  * ``info.vlen``: # of parameters
  * ``type``: the return type

``btf_type`` is followed by ``info.vlen`` number of ``struct btf_param``.::

    struct btf_param {
        __u32   name_off;
        __u32   type;
    };

If a BTF_KIND_FUNC_PROTO type is referred by a BTF_KIND_FUNC type, then
``btf_param.name_off`` must point to a valid C identifier except for the
possible last argument representing the variable argument. The btf_param.type
refers to parameter type.

If the function has variable arguments, the last parameter is encoded with
``name_off = 0`` and ``type = 0``.

BTF_KIND_VAR
~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: offset to a valid C identifier
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_VAR
  * ``info.vlen``: 0
  * ``type``: the type of the variable

``btf_type`` is followed by a single ``struct btf_variable`` with the
following data::

    struct btf_var {
        __u32   linkage;
    };

``struct btf_var`` encoding:
  * ``linkage``: currently only static variable 0, or globally allocated
                 variable in ELF sections 1

Not all type of global variables are supported by LLVM at this point.
The following is currently available:

  * static variables with or without section attributes
  * global variables with section attributes

The latter is for future extraction of map key/value type id's from a
map definition.

BTF_KIND_DATASEC
~~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: offset to a valid name associated with a variable or
                  one of .data/.bss/.rodata
  * ``info.kind_flag``: 0
  * ``info.kind``: BTF_KIND_DATASEC
  * ``info.vlen``: # of variables
  * ``size``: total section size in bytes (0 at compilation time, patched
              to actual size by BPF loaders such as libbpf)

``btf_type`` is followed by ``info.vlen`` number of ``struct btf_var_secinfo``.::

    struct btf_var_secinfo {
        __u32   type;
        __u32   offset;
        __u32   size;
    };

``struct btf_var_secinfo`` encoding:
  * ``type``: the type of the BTF_KIND_VAR variable
  * ``offset``: the in-section offset of the variable
  * ``size``: the size of the variable in bytes

BTF_KIND_FLOAT
~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
 * ``name_off``: any valid offset
 * ``info.kind_flag``: 0
 * ``info.kind``: BTF_KIND_FLOAT
 * ``info.vlen``: 0
 * ``size``: the size of the float type in bytes: 2, 4, 8, 12 or 16.

No additional type data follow ``btf_type``.

BTF_KIND_DECL_TAG
~~~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
 * ``name_off``: offset to a non-empty string
 * ``info.kind_flag``: 0
 * ``info.kind``: BTF_KIND_DECL_TAG
 * ``info.vlen``: 0
 * ``type``: ``struct``, ``union``, ``func``, ``var`` or ``typedef``

``btf_type`` is followed by ``struct btf_decl_tag``.::

    struct btf_decl_tag {
        __u32   component_idx;
    };

The ``name_off`` encodes btf_decl_tag attribute string.
The ``type`` should be ``struct``, ``union``, ``func``, ``var`` or ``typedef``.
For ``var`` or ``typedef`` type, ``btf_decl_tag.component_idx`` must be ``-1``.
For the other three types, if the btf_decl_tag attribute is
applied to the ``struct``, ``union`` or ``func`` itself,
``btf_decl_tag.component_idx`` must be ``-1``. Otherwise,
the attribute is applied to a ``struct``/``union`` member or
a ``func`` argument, and ``btf_decl_tag.component_idx`` should be a
valid index (starting from 0) pointing to a member or an argument.

BTF_KIND_TYPE_TAG
~~~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
 * ``name_off``: offset to a non-empty string
 * ``info.kind_flag``: 0
 * ``info.kind``: BTF_KIND_TYPE_TAG
 * ``info.vlen``: 0
 * ``type``: the type with ``btf_type_tag`` attribute

Currently, ``BTF_KIND_TYPE_TAG`` is only emitted for pointer types.
It has the following btf type chain:
::

  ptr -> [type_tag]*
      -> [const | volatile | restrict | typedef]*
      -> base_type

Basically, a pointer type points to zero or more
type_tag, then zero or more const/volatile/restrict/typedef
and finally the base type. The base type is one of
int, ptr, array, struct, union, enum, func_proto and float types.

BTF_KIND_ENUM64
~~~~~~~~~~~~~~~~~~~~~~

``struct btf_type`` encoding requirement:
  * ``name_off``: 0 or offset to a valid C identifier
  * ``info.kind_flag``: 0 for unsigned, 1 for signed
  * ``info.kind``: BTF_KIND_ENUM64
  * ``info.vlen``: number of enum values
  * ``size``: 1/2/4/8

``btf_type`` is followed by ``info.vlen`` number of ``struct btf_enum64``.::

    struct btf_enum64 {
        __u32   name_off;
        __u32   val_lo32;
        __u32   val_hi32;
    };

The ``btf_enum64`` encoding:
  * ``name_off``: offset to a valid C identifier
  * ``val_lo32``: lower 32-bit value for a 64-bit value
  * ``val_hi32``: high 32-bit value for a 64-bit value

If the original enum value is signed and the size is less than 8,
that value will be sign extended into 8 bytes.

