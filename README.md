# eBPF Standard Documentation

This repository is a working draft of standard eBPF documentation
to be published by the eBPF Foundation in PDF format.

Instruction Set Architecture:

* [Most recent Internet-Draft submitted](https://datatracker.ietf.org/doc/html/draft-thaler-bpf-isa)
* [Current draft PDF](https://github.com/ietf-wg-bpf/ebpf-docs/blob/pdf/instruction-set.pdf).
* [Current Internet-Draft working copy](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ietf-wg-bpf/ebpf-docs/pdf/draft-thaler-bpf-isa.html)

ELF File Format:

* [Most recent Internet-Draft submitted](https://datatracker.ietf.org/doc/html/draft-thaler-bpf-elf)
* [Current Internet-Draft working copy](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ietf-wg-bpf/ebpf-docs/pdf/draft-thaler-bpf-elf.html)

The authoritative sources from which these are built are
in the Linux kernel.org repository, but are not Linux specific.

A GitHub mirror is used, as is done for libbpf and
bpftool, so that other platforms and tools can easily use it.
As such, the documentation uses the subset of RST that GitHub
renders correctly.

The documentation can be IETF RFC style MUST/SHOULD/MAY language
if desired.  It does not currently do so.
