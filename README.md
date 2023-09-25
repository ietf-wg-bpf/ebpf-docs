# BPF Standard Documentation

This repository is a working draft of standard BPF documentation
to be published by the [IETF BPF Working Group](https://datatracker.ietf.org/wg/bpf/about/).

Instruction Set Architecture:

* [PDF generated from instruction-set.rst](https://github.com/ietf-wg-bpf/ebpf-docs/blob/generated/instruction-set.pdf).
* [Most recent Internet-Draft submitted](https://datatracker.ietf.org/doc/html/draft-thaler-bpf-isa)
* [Latest Internet-Draft working copy](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ietf-wg-bpf/ebpf-docs/generated/draft-thaler-bpf-isa.html)
* [Diff between latest and most recent submitted](https://author-tools.ietf.org/diff?doc_1=draft-thaler-bpf-isa&url_2=https://raw.githubusercontent.com/ietf-wg-bpf/ebpf-docs/generated/draft-thaler-bpf-isa.txt&wdiff=1)

ELF File Format:

* [Most recent Internet-Draft submitted](https://datatracker.ietf.org/doc/html/draft-thaler-bpf-elf)
* [Latest Internet-Draft working copy](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ietf-wg-bpf/ebpf-docs/generated/draft-thaler-bpf-elf.html)
* [Diff between latest and most recent submitted](https://author-tools.ietf.org/diff?doc_1=draft-thaler-bpf-elf&url_2=https://raw.githubusercontent.com/ietf-wg-bpf/ebpf-docs/pdf/draft-thaler-bpf-elf.txt&wdiff=1)

The authoritative sources from which these are built are
in the Linux kernel.org repository, but are not Linux specific.

A GitHub mirror is used, as is done for libbpf and
bpftool, so that other platforms and tools can easily use it.
As such, the documentation uses the subset of RST that GitHub
renders correctly.

The documentation can use IETF RFC style MUST/SHOULD/MAY language
if desired.  It does not currently do so.
