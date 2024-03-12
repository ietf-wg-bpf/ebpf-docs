.. |docName| replace:: draft-ietf-bpf-isa-01
.. |ipr| replace:: trust200902
.. |category| replace:: std
.. |titleAbbr| replace:: (e)BPF ISA
.. |submissionType| replace:: IETF
.. |author[0].fullname| replace:: Dave Thaler
.. |author[0].role| replace:: editor
.. |author[0].surname| replace:: Thaler
.. |author[0].initials| replace:: D.
.. |author[0].email| replace:: dave.thaler.ietf@gmail.com
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

This document defines two sub-registries.

BPF Instruction Conformance Group Registry
------------------------------------------

This document defines a IANA sub-registry for BPF instruction conformance groups, as follows:

* Name of the registry: BPF Instruction Conformance Groups
* Name of the registry group: BPF Instructions
* Required information for registrations: The values to appear in the entry fields.
* Syntax of registry entries: Each entry has the following fields:

  * name: alphanumeric label indicating the name of the conformance group
  * description: brief description of the conformance group
  * includes: any other conformance groups that are included from this group
  * excludes: any other conformance groups that are excluded from this group.
  * status: Permanent, Provisional, or Historical
  * reference: a reference to the defining specification
* Registration policy (see `RFC 8126 section 4 <https://www.rfc-editor.org/rfc/rfc8126.html#section-4>`_ for details):

  * Permanent: Standards action or IESG Review
  * Provisional: Specification required
  * Historical: Specification required

Initial entries in this sub-registry are as follows:

========  ==========================  ========  ========  ===========  ===============================================
name      description                 includes  excludes  status       reference
========  ==========================  ========  ========  ===========  ===============================================
atomic32  32-bit atomic instructions  -         -         Permanent    RFCXXX `Atomic operations`_
atomic64  64-bit atomic instructions  atomic32  -         Permanent    RFCXXX `Atomic operations`_
base32    32-bit base instructions    -         -         Permanent    RFCXXX
base64    64-bit base instructions    base32    -         Permanent    RFCXXX
divmul32  32-bit division and modulo  -         -         Permanent    RFCXXX `Arithmetic instructions`_
divmul64  64-bit division and modulo  divmul32  -         Permanent    RFCXXX `Arithmetic instructions`_
packet    Legacy packet instructions  -         -         Historical   RFCXXX `Legacy BPF Packet access instructions`_
========  ==========================  ========  ========  ===========  ===============================================

NOTE TO RFC-EDITOR: Upon publication, please replace RFCXXX above with reference to this document.

Adding instructions
~~~~~~~~~~~~~~~~~~~
A specification may add additional instructions to the BPF Instruction Set registry.
Once a conformance group is registered with a set of instructions,
no further instructions can be added to that conformance group. A specification
should instead create a new conformance group that includes the original conformance group,
plus any newly added instructions.  Inclusion of the original conformance group is done
via the "includes" column of the BPF Instruction Conformance Group Registry, and inclusion
of newly added instructions is done via the "groups" column of the BPF Instruction Set Registry.

Deprecating instructions
~~~~~~~~~~~~~~~~~~~~~~~~
Deprecating instructions that are part of an existing conformance group can be done by defining a
new conformance group for the newly deprecated instructions, and defining a new conformance group
to supercede the existing conformance group containing the instructions, where the new conformance
group includes the existing one and excludes the deprecated instruction group.

For example, if deprecating an instruction in an existing hypothetical group called "example", two new groups
might be registered:

=============  ===========================  ========  =============  ===========  ===========
name           description                  includes  excludes       status       reference
=============  ===========================  ========  =============  ===========  ===========
legacyexample  Legacy example instructions  -         -              Historical   (reference)
examplev2      Example instructions         example   legacyexample  Permanent    (reference)
=============  ===========================  ========  =============  ===========  ===========

The BPF Instruction Set entries for the deprecated instructions would then be updated 
to add "legacyexample" to the set of groups for those instructions.

Finally, updated implementations that dropped support for the deprecated instructions
would then be able to claim conformance to "examplev2" rather than "example".

BPF Instruction Set Registry
----------------------------

This document proposes a new IANA registry for BPF instructions, as follows:

* Name of the registry: BPF Instruction Set
* Name of the registry group: BPF Instructions
* Required information for registrations: The values to appear in the entry fields.
* Syntax of registry entries: Each entry has the following fields:

  * opcode: a 1-byte value in hex format indicating the value of the opcode field
  * src: either a value indicating the value of the src field, or "any"
  * imm: either a value indicating the value of the imm field, or "any"
  * offset: either a value indicating the value of the offset field, or "any"
  * description: description of what the instruction does, typically in pseudocode
  * groups: a list of one or more comma-separated conformance groups to which the instruction belongs
  * reference: a reference to the defining specification
* Registration policy: New instructions require a new entry in the conformance group
  sub-registry and the same registration policies apply.
* Initial registrations: See the Appendix. Instructions other than those listed
  as deprecated are Permanent. Any listed as deprecated are Historical.

Acknowledgements
================

This draft was generated from instruction-set.rst in the Linux
kernel repository, to which a number of other individuals have authored contributions
over time, including Akhil Raj, Alexei Starovoitov, Brendan Jackman, Christoph Hellwig, Daniel Borkmann,
Ilya Leoshkevich, Jiong Wang, Jose E. Marchesi, Kosuke Fujimoto,
Shahab Vahedi, Tiezhu Yang, Will Hawkins, and Zheng Yejian, with review and suggestions by many others including
Alan Jowett, Andrii Nakryiko, David Vernet, Jim Harris,
Quentin Monnet, Song Liu, Shung-Hsi Yu, Stanislav Fomichev, and Yonghong Song.

Appendix
========

.. include:: instruction-set-opcodes.rst
