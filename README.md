# eBPF Standard Documentation

This repository is a working draft of standard eBPF documentation
to be published by the eBPF Foundation in PDF format.

Instruction Set Architecture:

* [Current draft PDF](https://github.com/ebpffoundation/ebpf-docs/blob/pdf/instruction-set.pdf).
* [Current Internet-Draft working copy](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ebpffoundation/ebpf-docs/pdf/draft-thaler-bpf-isa.html)

ELF File Format:

* [Current Internet-Draft working copy](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ebpffoundation/ebpf-docs/pdf/draft-thaler-bpf-elf.html)

The authoritative source from which these are built is expected to be
in the Linux kernel.org repository, but not be Linux specific.

A GitHub mirror should be used, as is presently done for libbpf and
bpftool, so that other platforms and tools can easily use it.
As such, the documentation uses the subset of RST that GitHub
renders correctly.

The documentation can be IETF RFC style MUST/SHOULD/MAY language
if desired.  It does not currently do so.
