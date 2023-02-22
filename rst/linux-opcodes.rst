======  ====  ===================================================  =============
opcode  imm   description                                          reference
======  ====  ===================================================  =============
0x20    any   dst = ntohl(\*(u32 \*)(R6->data + imm))              `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
0x28    any   dst = ntohs(\*(u16 \*)(R6->data + imm))              `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
0x30    any   dst = (\*(u8 \*)(R6->data + imm))                    `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
0x38    any   dst = ntohll(\*(u64 \*)(R6->data + imm))             `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
0x40    any   dst = ntohl(\*(u32 \*)(R6->data + src + imm))        `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
0x48    any   dst = ntohs(\*(u16 \*)(R6->data + src + imm))        `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
0x50    any   dst = \*(u8 \*)(R6->data + src + imm))               `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
0x58    any   dst = ntohll(\*(u64 \*)(R6->data + src + imm))       `Legacy BPF Packet access instructions <linux-notes.rst#legacy-bpf-packet-access-instructions>`_
======  ====  ===================================================  =============
