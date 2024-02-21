Initial values for the BPF Instruction sub-registry are given below.
The descriptions in this table are informative. In case of any discrepancy, the reference
is authoritative.

======  =======  ======  ====  ======================================================  ========  ========================================
opcode  src_reg  offset  imm   description                                             groups    reference
======  =======  ======  ====  ======================================================  ========  ========================================
0x00    0x0      0       any   (additional immediate value)                            base64    `64-bit immediate instructions`_
0x04    0x0      0       any   dst = (u32)((u32)dst + (u32)imm)                        base32    `Arithmetic instructions`_
0x05    0x0      any     0x00  goto +offset                                            base32    `Jump instructions`_
0x06    0x0      0       any   goto +imm                                               base32    `Jump instructions`_
0x07    0x0      0       any   dst += imm                                              base64    `Arithmetic instructions`_
0x0c    any      0       0x00  dst = (u32)((u32)dst + (u32)src)                        base32    `Arithmetic instructions`_
0x0f    any      0       0x00  dst += src                                              base64    `Arithmetic instructions`_
0x14    0x0      0       any   dst = (u32)((u32)dst - (u32)imm)                        base32    `Arithmetic instructions`_
0x15    0x0      any     any   if dst == imm goto +offset                              base64    `Jump instructions`_
0x16    0x0      any     any   if (u32)dst == imm goto +offset                         base32    `Jump instructions`_
0x17    0x0      0       any   dst -= imm                                              base64    `Arithmetic instructions`_
0x18    0x0      0       any   dst = (next_imm << 32) | imm                            base64    `64-bit immediate instructions`_
0x18    0x1      0       any   dst = map_by_fd(imm)                                    base64    `64-bit immediate instructions`_
0x18    0x2      0       any   dst = map_val(map_by_fd(imm)) + next_imm                base64    `64-bit immediate instructions`_
0x18    0x3      0       any   dst = var_addr(imm)                                     base64    `64-bit immediate instructions`_
0x18    0x4      0       any   dst = code_addr(imm)                                    base64    `64-bit immediate instructions`_
0x18    0x5      0       any   dst = map_by_idx(imm)                                   base64    `64-bit immediate instructions`_
0x18    0x6      0       any   dst = map_val(map_by_idx(imm)) + next_imm               base64    `64-bit immediate instructions`_
0x1c    any      0       0x00  dst = (u32)((u32)dst - (u32)src)                        base32    `Arithmetic instructions`_
0x1d    any      any     0x00  if dst == src goto +offset                              base64    `Jump instructions`_
0x1e    any      any     0x00  if (u32)dst == (u32)src goto +offset                    base32    `Jump instructions`_
0x1f    any      0       0x00  dst -= src                                              base64    `Arithmetic instructions`_
0x20    any      any     any   (deprecated, implementation-specific)                   legacy    `Legacy BPF Packet access instructions`_
0x24    0x0      0       any   dst = (u32)(dst \* imm)                                 divmul32  `Arithmetic instructions`_
0x25    0x0      any     any   if dst > imm goto +offset                               base64    `Jump instructions`_
0x26    0x0      any     any   if (u32)dst > imm goto +offset                          base32    `Jump instructions`_
0x27    0x0      0       any   dst \*= imm                                             divmul64  `Arithmetic instructions`_
0x28    any      any     any   (deprecated, implementation-specific)                   legacy    `Legacy BPF Packet access instructions`_
0x2c    any      0       0x00  dst = (u32)(dst \* src)                                 divmul32  `Arithmetic instructions`_
0x2d    any      any     0x00  if dst > src goto +offset                               base64    `Jump instructions`_
0x2e    any      any     0x00  if (u32)dst > (u32)src goto +offset                     base32    `Jump instructions`_
0x2f    any      0       0x00  dst \*= src                                             divmul64  `Arithmetic instructions`_
0x30    any      any     any   (deprecated, implementation-specific)                   legacy    `Legacy BPF Packet access instructions`_
0x34    0x0      0       any   dst = (u32)((imm != 0) ? ((u32)dst / (u32)imm) : 0)     divmul32  `Arithmetic instructions`_
0x34    0x0      1       any   dst = (u32)((imm != 0) ? ((s32)dst s/ imm) : 0)         divmul32  `Arithmetic instructions`_
0x35    0x0      any     any   if dst >= imm goto +offset                              base64    `Jump instructions`_
0x36    0x0      any     any   if (u32)dst >= imm goto +offset                         base32    `Jump instructions`_
0x37    0x0      0       any   dst = (imm != 0) ? (dst / (u32)imm) : 0                 divmul64  `Arithmetic instructions`_
0x37    0x0      1       any   dst = (imm != 0) ? (dst s/ imm) : 0                     divmul64  `Arithmetic instructions`_
0x3c    any      0       0x00  dst = (u32)((src != 0) ? ((u32)dst / (u32)src) : 0)     divmul32  `Arithmetic instructions`_
0x3c    any      1       0x00  dst = (u32)((src != 0) ? ((s32)dst s/(s32)src) : 0)     divmul32  `Arithmetic instructions`_
0x3d    any      any     0x00  if dst >= src goto +offset                              base64    `Jump instructions`_
0x3e    any      any     0x00  if (u32)dst >= (u32)src goto +offset                    base32    `Jump instructions`_
0x3f    any      0       0x00  dst = (src != 0) ? (dst / src) : 0                      divmul64  `Arithmetic instructions`_
0x3f    any      1       0x00  dst = (src != 0) ? (dst s/ src) : 0                     divmul64  `Arithmetic instructions`_
0x40    any      any     any   (deprecated, implementation-specific)                   legacy    `Legacy BPF Packet access instructions`_
0x44    0x0      0       any   dst = (u32)(dst \| imm)                                 base32    `Arithmetic instructions`_
0x45    0x0      any     any   if dst & imm goto +offset                               base64    `Jump instructions`_
0x46    0x0      any     any   if (u32)dst & imm goto +offset                          base32    `Jump instructions`_
0x47    0x0      0       any   dst \|= imm                                             base64    `Arithmetic instructions`_
0x48    any      any     any   (deprecated, implementation-specific)                   legacy    `Legacy BPF Packet access instructions`_
0x4c    any      0       0x00  dst = (u32)(dst \| src)                                 base32    `Arithmetic instructions`_
0x4d    any      any     0x00  if dst & src goto +offset                               base64    `Jump instructions`_
0x4e    any      any     0x00  if (u32)dst & (u32)src goto +offset                     base32    `Jump instructions`_
0x4f    any      0       0x00  dst \|= src                                             base64    `Arithmetic instructions`_
0x50    any      any     any   (deprecated, implementation-specific)                   legacy    `Legacy BPF Packet access instructions`_
0x54    0x0      0       any   dst = (u32)(dst & imm)                                  base32    `Arithmetic instructions`_
0x55    0x0      any     any   if dst != imm goto +offset                              base64    `Jump instructions`_
0x56    0x0      any     any   if (u32)dst != imm goto +offset                         base32    `Jump instructions`_
0x57    0x0      0       any   dst &= imm                                              base64    `Arithmetic instructions`_
0x5c    any      0       0x00  dst = (u32)(dst & src)                                  base32    `Arithmetic instructions`_
0x5d    any      any     0x00  if dst != src goto +offset                              base64    `Jump instructions`_
0x5e    any      any     0x00  if (u32)dst != (u32)src goto +offset                    base32    `Jump instructions`_
0x5f    any      0       0x00  dst &= src                                              base64    `Arithmetic instructions`_
0x61    any      any     0x00  dst = \*(u32 \*)(src + offset)                          base32    `Load and store instructions`_
0x62    0x0      any     any   \*(u32 \*)(dst + offset) = imm                          base32    `Load and store instructions`_
0x63    any      any     0x00  \*(u32 \*)(dst + offset) = src                          base32    `Load and store instructions`_
0x64    0x0      0       any   dst = (u32)(dst << imm)                                 base32    `Arithmetic instructions`_
0x65    0x0      any     any   if dst s> imm goto +offset                              base64    `Jump instructions`_
0x66    0x0      any     any   if (s32)dst s> (s32)imm goto +offset                    base32    `Jump instructions`_
0x67    0x0      0       any   dst <<= imm                                             base64    `Arithmetic instructions`_
0x69    any      any     0x00  dst = \*(u16 \*)(src + offset)                          base32    `Load and store instructions`_
0x6a    0x0      any     any   \*(u16 \*)(dst + offset) = imm                          base32    `Load and store instructions`_
0x6b    any      any     0x00  \*(u16 \*)(dst + offset) = src                          base32    `Load and store instructions`_
0x6c    any      0       0x00  dst = (u32)(dst << src)                                 base32    `Arithmetic instructions`_
0x6d    any      any     0x00  if dst s> src goto +offset                              base64    `Jump instructions`_
0x6e    any      any     0x00  if (s32)dst s> (s32)src goto +offset                    base32    `Jump instructions`_
0x6f    any      0       0x00  dst <<= src                                             base64    `Arithmetic instructions`_
0x71    any      any     0x00  dst = \*(u8 \*)(src + offset)                           base32    `Load and store instructions`_
0x72    0x0      any     any   \*(u8 \*)(dst + offset) = imm                           base32    `Load and store instructions`_
0x73    any      any     0x00  \*(u8 \*)(dst + offset) = src                           base32    `Load and store instructions`_
0x74    0x0      0       any   dst = (u32)(dst >> imm)                                 base32    `Arithmetic instructions`_
0x75    0x0      any     any   if dst s>= imm goto +offset                             base64    `Jump instructions`_
0x76    0x0      any     any   if (s32)dst s>= (s32)imm goto +offset                   base32    `Jump instructions`_
0x77    0x0      0       any   dst >>= imm                                             base64    `Arithmetic instructions`_
0x79    any      any     0x00  dst = \*(u64 \*)(src + offset)                          base64    `Load and store instructions`_
0x7a    0x0      any     any   \*(u64 \*)(dst + offset) = imm                          base64    `Load and store instructions`_
0x7b    any      any     0x00  \*(u64 \*)(dst + offset) = src                          base64    `Load and store instructions`_
0x7c    any      0       0x00  dst = (u32)(dst >> src)                                 base32    `Arithmetic instructions`_
0x7d    any      any     0x00  if dst s>= src goto +offset                             base64    `Jump instructions`_
0x7e    any      any     0x00  if (s32)dst s>= (s32)src goto +offset                   base32    `Jump instructions`_
0x7f    any      0       0x00  dst >>= src                                             base64    `Arithmetic instructions`_
0x84    0x0      0       0x00  dst = (u32)-dst                                         base32    `Arithmetic instructions`_
0x85    0x0      0       any   call helper function by address                         base32    `Helper functions`_
0x85    0x1      0       any   call PC += imm                                          base32    `Program-local functions`_
0x85    0x2      0       any   call helper function by BTF ID                          base32    `Helper functions`_
0x87    0x0      0       0x00  dst = -dst                                              base32    `Arithmetic instructions`_
0x94    0x0      0       any   dst = (u32)((imm != 0)?((u32)dst % (u32)imm) : dst)     divmul32  `Arithmetic instructions`_
0x94    0x0      1       any   dst = (u32)((imm != 0) ? ((s32)dst s% imm) : dst)       divmul32  `Arithmetic instructions`_
0x95    0x0      0       0x00  return                                                  base32    `Jump instructions`_
0x97    0x0      0       any   dst = (imm != 0) ? (dst % (u32)imm) : dst               divmul64  `Arithmetic instructions`_
0x97    0x0      1       any   dst = (imm != 0) ? (dst s% imm) : dst                   divmul64  `Arithmetic instructions`_
0x9c    any      0       0x00  dst = (u32)((src != 0)?((u32)dst % (u32)src) : dst)     divmul32  `Arithmetic instructions`_
0x9c    any      1       0x00  dst = (u32)((src != 0)?((s32)dst s% (s32)src) :dst)     divmul32  `Arithmetic instructions`_
0x9f    any      0       0x00  dst = (src != 0) ? (dst % src) : dst                    divmul64  `Arithmetic instructions`_
0x9f    any      1       0x00  dst = (src != 0) ? (dst s% src) : dst                   divmul64  `Arithmetic instructions`_
0xa4    0x0      0       any   dst = (u32)(dst ^ imm)                                  base32    `Arithmetic instructions`_
0xa5    0x0      any     any   if dst < imm goto +offset                               base64    `Jump instructions`_
0xa6    0x0      any     any   if (u32)dst < imm goto +offset                          base32    `Jump instructions`_
0xa7    0x0      0       any   dst ^= imm                                              base64    `Arithmetic instructions`_
0xac    any      0       0x00  dst = (u32)(dst ^ src)                                  base32    `Arithmetic instructions`_
0xad    any      any     0x00  if dst < src goto +offset                               base64    `Jump instructions`_
0xae    any      any     0x00  if (u32)dst < (u32)src goto +offset                     base32    `Jump instructions`_
0xaf    any      0       0x00  dst ^= src                                              base64    `Arithmetic instructions`_
0xb4    0x0      0       any   dst = (u32) imm                                         base32    `Arithmetic instructions`_
0xb5    0x0      any     any   if dst <= imm goto +offset                              base64    `Jump instructions`_
0xb6    0x0      any     any   if (u32)dst <= imm goto +offset                         base32    `Jump instructions`_
0xb7    0x0      0       any   dst = imm                                               base64    `Arithmetic instructions`_
0xbc    any      0       0x00  dst = (u32) src                                         base32    `Arithmetic instructions`_
0xbc    any      8       0x00  dst = (u32) (s32) (s8) src                              base32    `Arithmetic instructions`_
0xbc    any      16      0x00  dst = (u32) (s32) (s16) src                             base32    `Arithmetic instructions`_
0xbd    any      any     0x00  if dst <= src goto +offset                              base64    `Jump instructions`_
0xbe    any      any     0x00  if (u32)dst <= (u32)src goto +offset                    base32    `Jump instructions`_
0xbf    any      0       0x00  dst = src                                               base64    `Arithmetic instructions`_
0xbf    any      8       0x00  dst = (s64) (s8) src                                    base64    `Arithmetic instructions`_
0xbf    any      16      0x00  dst = (s64) (s16) src                                   base64    `Arithmetic instructions`_
0xbf    any      32      0x00  dst = (s64) (s32) src                                   base64    `Arithmetic instructions`_
0xc3    any      any     0x00  lock \*(u32 \*)(dst + offset) += src                    atomic32  `Atomic operations`_
0xc3    any      any     0x01  src = atomic_fetch_add_32((u32 \*)(dst + offset), src)  atomic32  `Atomic operations`_
0xc3    any      any     0x40  lock \*(u32 \*)(dst + offset) \|= src                   atomic32  `Atomic operations`_
0xc3    any      any     0x41  src = atomic_fetch_or_32((u32 \*)(dst + offset), src)   atomic32  `Atomic operations`_
0xc3    any      any     0x50  lock \*(u32 \*)(dst + offset) &= src                    atomic32  `Atomic operations`_
0xc3    any      any     0x51  src = atomic_fetch_and_32((u32 \*)(dst + offset), src)  atomic32  `Atomic operations`_
0xc3    any      any     0xa0  lock \*(u32 \*)(dst + offset) ^= src                    atomic32  `Atomic operations`_
0xc3    any      any     0xa1  src = atomic_fetch_xor_32((u32 \*)(dst + offset), src)  atomic32  `Atomic operations`_
0xc3    any      any     0xe1  src = xchg_32((u32 \*)(dst + offset), src)              atomic32  `Atomic operations`_
0xc3    any      any     0xf1  r0 = cmpxchg_32((u32 \*)(dst + offset), r0, src)        atomic32  `Atomic operations`_
0xc4    0x0      0       any   dst = (u32)(dst s>> imm)                                base32    `Arithmetic instructions`_
0xc5    0x0      any     any   if dst s< imm goto +offset                              base64    `Jump instructions`_
0xc6    0x0      any     any   if (s32)dst s< (s32)imm goto +offset                    base32    `Jump instructions`_
0xc7    0x0      0       any   dst s>>= imm                                            base64    `Arithmetic instructions`_
0xcc    any      0       0x00  dst = (u32)(dst s>> src)                                base32    `Arithmetic instructions`_
0xcd    any      any     0x00  if dst s< src goto +offset                              base64    `Jump instructions`_
0xce    any      any     0x00  if (s32)dst s< (s32)src goto +offset                    base32    `Jump instructions`_
0xcf    any      0       0x00  dst s>>= src                                            base64    `Arithmetic instructions`_
0xd4    0x0      0       0x10  dst = htole16(dst)                                      base32    `Byte swap instructions`_
0xd4    0x0      0       0x20  dst = htole32(dst)                                      base32    `Byte swap instructions`_
0xd4    0x0      0       0x40  dst = htole64(dst)                                      base64    `Byte swap instructions`_
0xd5    0x0      any     any   if dst s<= imm goto +offset                             base64    `Jump instructions`_
0xd6    0x0      any     any   if (s32)dst s<= (s32)imm goto +offset                   base32    `Jump instructions`_
0xd7    0x0      0       0x10  dst = bswap16(dst)                                      base32    `Byte swap instructions`_
0xd7    0x0      0       0x20  dst = bswap32(dst)                                      base32    `Byte swap instructions`_
0xd7    0x0      0       0x40  dst = bswap64(dst)                                      base64    `Byte swap instructions`_
0xdb    any      any     0x00  lock \*(u64 \*)(dst + offset) += src                    atomic64  `Atomic operations`_
0xdb    any      any     0x01  src = atomic_fetch_add_64((u64 \*)(dst + offset), src)  atomic64  `Atomic operations`_
0xdb    any      any     0x40  lock \*(u64 \*)(dst + offset) \|= src                   atomic64  `Atomic operations`_
0xdb    any      any     0x41  src = atomic_fetch_or_64((u64 \*)(dst + offset), src)   atomic64  `Atomic operations`_
0xdb    any      any     0x50  lock \*(u64 \*)(dst + offset) &= src                    atomic64  `Atomic operations`_
0xdb    any      any     0x51  src = atomic_fetch_and_64((u64 \*)(dst + offset), src)  atomic64  `Atomic operations`_
0xdb    any      any     0xa0  lock \*(u64 \*)(dst + offset) ^= src                    atomic64  `Atomic operations`_
0xdb    any      any     0xa1  src = atomic_fetch_xor_64((u64 \*)(dst + offset), src)  atomic64  `Atomic operations`_
0xdb    any      any     0xe1  src = xchg_64((u64 \*)(dst + offset), src)              atomic64  `Atomic operations`_
0xdb    any      any     0xf1  r0 = cmpxchg_64((u64 \*)(dst + offset), r0, src)        atomic64  `Atomic operations`_
0xdc    0x0      0       0x10  dst = htobe16(dst)                                      base32    `Byte swap instructions`_
0xdc    0x0      0       0x20  dst = htobe32(dst)                                      base32    `Byte swap instructions`_
0xdc    0x0      0       0x40  dst = htobe64(dst)                                      base64    `Byte swap instructions`_
0xdd    any      any     0x00  if dst s<= src goto +offset                             base64    `Jump instructions`_
0xde    any      any     0x00  if (s32)dst s<= (s32)src goto +offset                   base32    `Jump instructions`_
======  =======  ======  ====  ======================================================  ========  ========================================
