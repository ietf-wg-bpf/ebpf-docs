For reference, the following table lists opcodes in order by value.

======  ===  ====  ===================================================  ========================================
opcode  src  imm   description                                          reference
======  ===  ====  ===================================================  ========================================
0x00    0x0  any   (additional immediate value)                         `64-bit immediate instructions`_
0x04    0x0  any   dst = (u32)((u32)dst + (u32)imm)                     `Arithmetic instructions`_
0x05    0x0  0x00  goto +offset                                         `Jump instructions`_
0x07    0x0  any   dst += imm                                           `Arithmetic instructions`_
0x0c    any  0x00  dst = (u32)((u32)dst + (u32)src)                     `Arithmetic instructions`_
0x0f    any  0x00  dst += src                                           `Arithmetic instructions`_
0x14    0x0  any   dst = (u32)((u32)dst - (u32)imm)                     `Arithmetic instructions`_
0x15    0x0  any   if dst == imm goto +offset                           `Jump instructions`_
0x16    0x0  any   if (u32)dst == imm goto +offset                      `Jump instructions`_
0x17    0x0  any   dst -= imm                                           `Arithmetic instructions`_
0x18    0x0  any   dst = imm64                                          `64-bit immediate instructions`_
0x18    0x1  any   dst = map_by_fd(imm)                                 `64-bit immediate instructions`_
0x18    0x2  any   dst = mva(map_by_fd(imm)) + next_imm                 `64-bit immediate instructions`_
0x18    0x3  any   dst = variable_addr(imm)                             `64-bit immediate instructions`_
0x18    0x4  any   dst = code_addr(imm)                                 `64-bit immediate instructions`_
0x18    0x5  any   dst = map_by_idx(imm)                                `64-bit immediate instructions`_
0x18    0x6  any   dst = mva(map_by_idx(imm)) + next_imm                `64-bit immediate instructions`_
0x1c    any  0x00  dst = (u32)((u32)dst - (u32)src)                     `Arithmetic instructions`_
0x1d    any  0x00  if dst == src goto +offset                           `Jump instructions`_
0x1e    any  0x00  if (u32)dst == (u32)src goto +offset                 `Jump instructions`_
0x1f    any  0x00  dst -= src                                           `Arithmetic instructions`_
0x20    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x24    0x0  any   dst = (u32)(dst \* imm)                              `Arithmetic instructions`_
0x25    0x0  any   if dst > imm goto +offset                            `Jump instructions`_
0x26    0x0  any   if (u32)dst > imm goto +offset                       `Jump instructions`_
0x27    0x0  any   dst \*= imm                                          `Arithmetic instructions`_
0x28    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x2c    any  0x00  dst = (u32)(dst \* src)                              `Arithmetic instructions`_
0x2d    any  0x00  if dst > src goto +offset                            `Jump instructions`_
0x2e    any  0x00  if (u32)dst > (u32)src goto +offset                  `Jump instructions`_
0x2f    any  0x00  dst \*= src                                          `Arithmetic instructions`_
0x30    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x34    0x0  any   dst = (u32)((imm != 0) ? (dst / imm) : 0)            `Arithmetic instructions`_
0x35    0x0  any   if dst >= imm goto +offset                           `Jump instructions`_
0x36    0x0  any   if (u32)dst >= imm goto +offset                      `Jump instructions`_
0x37    0x0  any   dst = (imm != 0) ? (dst / imm) : 0                   `Arithmetic instructions`_
0x38    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x3c    any  0x00  dst = (u32)((imm != 0) ? (dst / src) : 0)            `Arithmetic instructions`_
0x3d    any  0x00  if dst >= src goto +offset                           `Jump instructions`_
0x3e    any  0x00  if (u32)dst >= (u32)src goto +offset                 `Jump instructions`_
0x3f    any  0x00  dst = (src !+ 0) ? (dst / src) : 0                   `Arithmetic instructions`_
0x40    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x44    0x0  any   dst = (u32)(dst \| imm)                              `Arithmetic instructions`_
0x45    0x0  any   if dst & imm goto +offset                            `Jump instructions`_
0x46    0x0  any   if (u32)dst & imm goto +offset                       `Jump instructions`_
0x47    0x0  any   dst \|= imm                                          `Arithmetic instructions`_
0x48    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x4c    any  0x00  dst = (u32)(dst \| src)                              `Arithmetic instructions`_
0x4d    any  0x00  if dst & src goto +offset                            `Jump instructions`_
0x4e    any  0x00  if (u32)dst & (u32)src goto +offset                  `Jump instructions`_
0x4f    any  0x00  dst \|= src                                          `Arithmetic instructions`_
0x50    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x54    0x0  any   dst = (u32)(dst & imm)                               `Arithmetic instructions`_
0x55    0x0  any   if dst != imm goto +offset                           `Jump instructions`_
0x56    0x0  any   if (u32)dst != imm goto +offset                      `Jump instructions`_
0x57    0x0  any   dst &= imm                                           `Arithmetic instructions`_
0x58    any  any   (deprecated, implementation-specific)                `Legacy BPF Packet access instructions`_
0x5c    any  0x00  dst = (u32)(dst & src)                               `Arithmetic instructions`_
0x5d    any  0x00  if dst != src goto +offset                           `Jump instructions`_
0x5e    any  0x00  if (u32)dst != (u32)src goto +offset                 `Jump instructions`_
0x5f    any  0x00  dst &= src                                           `Arithmetic instructions`_
0x61    any  0x00  dst = \*(u32 \*)(src + offset)                       `Load and store instructions`_
0x62    0x0  any   \*(u32 \*)(dst + offset) = imm                       `Load and store instructions`_
0x63    any  0x00  \*(u32 \*)(dst + offset) = src                       `Load and store instructions`_
0x64    0x0  any   dst = (u32)(dst << imm)                              `Arithmetic instructions`_
0x65    0x0  any   if dst s> imm goto +offset                           `Jump instructions`_
0x66    0x0  any   if (s32)dst s> (s32)imm goto +offset                 `Jump instructions`_
0x67    0x0  any   dst <<= imm                                          `Arithmetic instructions`_
0x69    any  0x00  dst = \*(u16 \*)(src + offset)                       `Load and store instructions`_
0x6a    0x0  any   \*(u16 \*)(dst + offset) = imm                       `Load and store instructions`_
0x6b    any  0x00  \*(u16 \*)(dst + offset) = src                       `Load and store instructions`_
0x6c    any  0x00  dst = (u32)(dst << src)                              `Arithmetic instructions`_
0x6d    any  0x00  if dst s> src goto +offset                           `Jump instructions`_
0x6e    any  0x00  if (s32)dst s> (s32)src goto +offset                 `Jump instructions`_
0x6f    any  0x00  dst <<= src                                          `Arithmetic instructions`_
0x71    any  0x00  dst = \*(u8 \*)(src + offset)                        `Load and store instructions`_
0x72    0x0  any   \*(u8 \*)(dst + offset) = imm                        `Load and store instructions`_
0x73    any  0x00  \*(u8 \*)(dst + offset) = src                        `Load and store instructions`_
0x74    0x0  any   dst = (u32)(dst >> imm)                              `Arithmetic instructions`_
0x75    0x0  any   if dst s>= imm goto +offset                          `Jump instructions`_
0x76    0x0  any   if (s32)dst s>= (s32)imm goto +offset                `Jump instructions`_
0x77    0x0  any   dst >>= imm                                          `Arithmetic instructions`_
0x79    any  0x00  dst = \*(u64 \*)(src + offset)                       `Load and store instructions`_
0x7a    0x0  any   \*(u64 \*)(dst + offset) = imm                       `Load and store instructions`_
0x7b    any  0x00  \*(u64 \*)(dst + offset) = src                       `Load and store instructions`_
0x7c    any  0x00  dst = (u32)(dst >> src)                              `Arithmetic instructions`_
0x7d    any  0x00  if dst s>= src goto +offset                          `Jump instructions`_
0x7e    any  0x00  if (s32)dst s>= (s32)src goto +offset                `Jump instructions`_
0x7f    any  0x00  dst >>= src                                          `Arithmetic instructions`_
0x84    0x0  0x00  dst = (u32)-dst                                      `Arithmetic instructions`_
0x85    0x0  any   call helper function imm                             `Helper functions`_
0x85    0x1  any   call PC += offset                                    `eBPF functions`_
0x85    0x2  any   call runtime function imm                            `Runtime functions`_
0x87    0x0  0x00  dst = -dst                                           `Arithmetic instructions`_
0x94    0x0  any   dst = (u32)((imm != 0) ? (dst % imm) : dst)          `Arithmetic instructions`_
0x95    0x0  0x00  return                                               `Jump instructions`_
0x97    0x0  any   dst = (imm != 0) ? (dst % imm) : dst                 `Arithmetic instructions`_
0x9c    any  0x00  dst = (u32)((src != 0) ? (dst % src) : dst)          `Arithmetic instructions`_
0x9f    any  0x00  dst = (src != 0) ? (dst % src) : dst                 `Arithmetic instructions`_
0xa4    0x0  any   dst = (u32)(dst ^ imm)                               `Arithmetic instructions`_
0xa5    0x0  any   if dst < imm goto +offset                            `Jump instructions`_
0xa6    0x0  any   if (u32)dst < imm goto +offset                       `Jump instructions`_
0xa7    0x0  any   dst ^= imm                                           `Arithmetic instructions`_
0xac    any  0x00  dst = (u32)(dst ^ src)                               `Arithmetic instructions`_
0xad    any  0x00  if dst < src goto +offset                            `Jump instructions`_
0xae    any  0x00  if (u32)dst < (u32)src goto +offset                  `Jump instructions`_
0xaf    any  0x00  dst ^= src                                           `Arithmetic instructions`_
0xb4    0x0  any   dst = (u32) imm                                      `Arithmetic instructions`_
0xb5    0x0  any   if dst <= imm goto +offset                           `Jump instructions`_
0xa6    0x0  any   if (u32)dst <= imm goto +offset                      `Jump instructions`_
0xb7    0x0  any   dst = imm                                            `Arithmetic instructions`_
0xbc    any  0x00  dst = (u32) src                                      `Arithmetic instructions`_
0xbd    any  0x00  if dst <= src goto +offset                           `Jump instructions`_
0xbe    any  0x00  if (u32)dst <= (u32)src goto +offset                 `Jump instructions`_
0xbf    any  0x00  dst = src                                            `Arithmetic instructions`_
0xc3    any  0x00  lock \*(u32 \*)(dst + offset) += src                 `Atomic operations`_
0xc3    any  0x01  lock::                                               `Atomic operations`_

                       *(u32 *)(dst + offset) += src
                       src = *(u32 *)(dst + offset)
0xc3    any  0x40  \*(u32 \*)(dst + offset) \|= src                     `Atomic operations`_
0xc3    any  0x41  lock::                                               `Atomic operations`_

                       *(u32 *)(dst + offset) |= src
                       src = *(u32 *)(dst + offset)
0xc3    any  0x50  \*(u32 \*)(dst + offset) &= src                      `Atomic operations`_
0xc3    any  0x51  lock::                                               `Atomic operations`_

                       *(u32 *)(dst + offset) &= src
                       src = *(u32 *)(dst + offset)
0xc3    any  0xa0  \*(u32 \*)(dst + offset) ^= src                      `Atomic operations`_
0xc3    any  0xa1  lock::                                               `Atomic operations`_

                       *(u32 *)(dst + offset) ^= src
                       src = *(u32 *)(dst + offset)
0xc3    any  0xe1  lock::                                               `Atomic operations`_

                       temp = *(u32 *)(dst + offset)
                       *(u32 *)(dst + offset) = src
                       src = temp
0xc3    any  0xf1  lock::                                               `Atomic operations`_

                       temp = *(u32 *)(dst + offset)
                       if *(u32)(dst + offset) == R0
                          *(u32)(dst + offset) = src
                       R0 = temp
0xc4    0x0  any   dst = (u32)(dst s>> imm)                             `Arithmetic instructions`_
0xc5    0x0  any   if dst s< imm goto +offset                           `Jump instructions`_
0xc6    0x0  any   if (s32)dst s< (s32)imm goto +offset                 `Jump instructions`_
0xc7    0x0  any   dst s>>= imm                                         `Arithmetic instructions`_
0xcc    any  0x00  dst = (u32)(dst s>> src)                             `Arithmetic instructions`_
0xcd    any  0x00  if dst s< src goto +offset                           `Jump instructions`_
0xce    any  0x00  if (s32)dst s< (s32)src goto +offset                 `Jump instructions`_
0xcf    any  0x00  dst s>>= src                                         `Arithmetic instructions`_
0xd4    0x0  0x10  dst = htole16(dst)                                   `Byte swap instructions`_
0xd4    0x0  0x20  dst = htole32(dst)                                   `Byte swap instructions`_
0xd4    0x0  0x40  dst = htole64(dst)                                   `Byte swap instructions`_
0xd5    0x0  any   if dst s<= imm goto +offset                          `Jump instructions`_
0xd6    0x0  any   if (s32)dst s<= (s32)imm goto +offset                `Jump instructions`_
0xdb    any  0x00  lock \*(u64 \*)(dst + offset) += src                 `Atomic operations`_
0xdb    any  0x01  lock::                                               `Atomic operations`_

                       *(u64 *)(dst + offset) += src
                       src = *(u64 *)(dst + offset)
0xdb    any  0x40  \*(u64 \*)(dst + offset) \|= src                     `Atomic operations`_
0xdb    any  0x41  lock::                                               `Atomic operations`_

                       *(u64 *)(dst + offset) |= src
                       lock src = *(u64 *)(dst + offset)
0xdb    any  0x50  \*(u64 \*)(dst + offset) &= src                      `Atomic operations`_
0xdb    any  0x51  lock::                                               `Atomic operations`_

                       *(u64 *)(dst + offset) &= src
                       src = *(u64 *)(dst + offset)
0xdb    any  0xa0  \*(u64 \*)(dst + offset) ^= src                      `Atomic operations`_
0xdb    any  0xa1  lock::                                               `Atomic operations`_

                       *(u64 *)(dst + offset) ^= src
                       src = *(u64 *)(dst + offset)
0xdb    any  0xe1  lock::                                               `Atomic operations`_

                       temp = *(u64 *)(dst + offset)
                       *(u64 *)(dst + offset) = src
                       src = temp
0xdb    any  0xf1  lock::                                               `Atomic operations`_

                       temp = *(u64 *)(dst + offset)
                       if *(u64)(dst + offset) == R0
                          *(u64)(dst + offset) = src
                       R0 = temp
0xdc    0x0  0x10  dst = htobe16(dst)                                   `Byte swap instructions`_
0xdc    0x0  0x20  dst = htobe32(dst)                                   `Byte swap instructions`_
0xdc    0x0  0x40  dst = htobe64(dst)                                   `Byte swap instructions`_
0xdd    any  0x00  if dst s<= src goto +offset                          `Jump instructions`_
0xde    any  0x00  if (s32)dst s<= (s32)src goto +offset                `Jump instructions`_
======  ===  ====  ===================================================  ========================================
