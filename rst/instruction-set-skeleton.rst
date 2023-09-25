.. |docName| replace:: draft-thaler-bpf-isa-01
.. |ipr| replace:: trust200902
.. |category| replace:: std
.. |titleAbbr| replace:: eBPF ISA
.. |submissionType| replace:: IETF
.. |author[0].fullname| replace:: Dave Thaler
.. |author[0].role| replace:: editor
.. |author[0].surname| replace:: Thaler
.. |author[0].initials| replace:: D.
.. |author[0].organization| replace:: Microsoft
.. |author[0].email| replace:: dthaler@microsoft.com
.. |author[0].city| replace:: Redmond
.. |author[0].region| replace:: WA
.. |author[0].code| replace:: 98052
.. |author[0].country| replace:: USA
.. |ref[RFC8126].target| replace:: https://www.rfc-editor.org/rfc/rfc8126.html
.. |ref[RFC8126].title| replace:: Guidelines for Writing an IANA Considerations Section in RFCs
.. |ref[RFC8126].type| replace:: normative
.. |ref[RFC8126].seriesInfo.name| replace:: RFC
.. |ref[RFC8126].seriesInfo.value| replace:: 8126
.. header::

.. include:: instruction-set.rst

IANA Considerations
===================

This document proposes a new IANA registry for BPF instructions, as follows:

* Name of the registry: BPF Instruction Set
* Name of the registry group: same as registry name
* Required information for registrations: The values to appear in the entry fields.
* Syntax of registry entries: Each entry has the following fields:

  * opcode: a 1-byte value in hex format indicating the value of the opcode field
  * src: either a value indicating the value of the src field, or "any"
  * imm: either a value indicating the value of the imm field, or "any"
  * offset: either a value indicating the value of the offset field, or "any"
  * description: description of what the instruction does, typically in pseudocode
  * reference: a reference to the defining specification
  * status: Permanent, Provisional, or Historical
* Registration policy (see `RFC 8126 section 4 <https://www.rfc-editor.org/rfc/rfc8126.html#section-4>`_ for details):

  * Permanent: Standards action or IESG Review
  * Provisional: Specification required
  * Historical: Specification required
* Initial registrations: See the Appendix. Instructions other than those listed
  as deprecated are Permanent. Any listed as deprecated are Historical.

Acknowledgements
================

This draft was generated from instruction-set.rst in the Linux
kernel repository, to which a number of other individuals have authored contributions
over time, including Akhil Raj, Will Hawkins, Christoph Hellwig, Jose E. Marchesi, Kosuke Fujimoto,
Shahab Vahedi, Tiezhu Yang, and Zheng Yejian, with review and suggestions by many others including
Alan Jowett, Alexei Starovoitov, Andrii Nakryiko, Daniel Borkmann, David Vernet, Jim Harris,
Quentin Monnet, Song Liu, Shung-Hsi Yu, Stanislav Fomichev, and Yonghong Song.

Appendix
========

.. include:: instruction-set-opcodes.rst
