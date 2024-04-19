.. |docName| replace:: draft-ietf-bpf-isa-02
.. |ipr| replace:: trust200902
.. |category| replace:: std
.. |titleAbbr| replace:: BPF ISA
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

This document defines an IANA sub-registry for BPF instruction conformance groups, as follows:

* Name of the registry: BPF Instruction Conformance Groups
* Name of the registry group: BPF Instructions
* Required information for registrations: See `BPF Instruction Conformance Group Registration Template`_
* Syntax of registry entries: Each entry has the following fields: name, description, includes, excludes,
  status, and reference. See `BPF Instruction Conformance Group Registration Template`_ for more details.
* Registration policy (see `RFC 8126 section 4 <https://www.rfc-editor.org/rfc/rfc8126.html#section-4>`_ for details):

  * Permanent: Standards action or IESG Approval
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

BPF Instruction Conformance Group Registration Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This template describes the fields that must be supplied in a registration request
suitable for adding to the registry:

Name:
  Alphanumeric label indicating the name of the conformance group.

Description:
  Brief description of the conformance group.

Includes:
  Any other conformance groups that are included from this group.

Excludes:
  Any other conformance groups that are excluded from this group.

Status:
  This reflects the status requested and must be one of 'Permanent',
  'Provisional', or 'Historical'.

Contact:
  Person (including contact information) to contact for further information.

Change controller:
  Organization or person (often the author), including contact information,
  authoried to change this.

Reference:
  A reference to the defining specification.
  Include full citations for all referenced documents.
  Registration requests for 'Provisional' registration can be
  included in an Internet-Draft; when the documents expire or are
  approved for publication as an RFC, the registration will be
  updated.

BPF Instruction Set Registry
----------------------------

This document proposes a new IANA registry for BPF instructions, as follows:

* Name of the registry: BPF Instruction Set
* Name of the registry group: BPF Instructions
* Required information for registrations: See `BPF Instruction Registration Template`_
* Syntax of registry entries: Each entry has the following fields: opcode, src, imm, offset, description,
  groups, and reference. See `BPF Instruction Registration Template`_ for more details.
* Registration policy: New instructions require a new entry in the conformance group
  sub-registry and the same registration policies apply.
* Initial registrations: See the Appendix. Instructions other than those listed
  as deprecated are Permanent. Any listed as deprecated are Historical.

BPF Instruction Registration Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This template describes the fields that must be supplied in a registration request
suitable for adding to the registry:

Opcode:
  A 1-byte value in hex format indicating the value of the opcode field

Src:
  Either a numeric value indicating the value of the src field, or "any"

Imm:
  Either a value indicating the value of the imm field, or "any"

Offset:
  Either a numeric value indicating the value of the offset field, or "any"

Description:
  Description of what the instruction does, typically in pseudocode

Groups:
  A list of one or more comma-separated conformance groups to which the instruction belongs

Contact:
  Person (including contact information) to contact for further information.

Change controller:
  Organization or person (often the author), including contact information,
  authoried to change this.

Reference:
  A reference to the defining specification.
  Include full citations for all referenced documents.
  Registration requests for 'Provisional' registration can be
  included in an Internet-Draft; when the documents expire or are
  approved for publication as an RFC, the registration will be
  updated.

Adding instructions
-------------------
A specification may add additional instructions to the BPF Instruction Set registry.
Once a conformance group is registered with a set of instructions,
no further instructions can be added to that conformance group. A specification
should instead create a new conformance group that includes the original conformance group,
plus any newly added instructions.  Inclusion of the original conformance group is done
via the "includes" column of the BPF Instruction Conformance Group Registry, and inclusion
of newly added instructions is done via the "groups" column of the BPF Instruction Set Registry.

For example, consider an existing hypothetical group called "example" with two instructions in it.
One might add two more instructions by first adding an "examplev2" group to the
BPF Instruction Conformance Group Registry as follows:

=============  =================================  ========  ========  =========
name           description                        includes  excludes  status
=============  =================================  ========  ========  =========
example        Original example instructions      -         -         Permanent
examplev2      Newer set of example instructions  example   -         Permanent
=============  =================================  ========  ========  =========

And then adding the new instructions into the BPF Instruction Set Registry as follows:

======  ===  =================================  =============
opcode  ...  description                        groups
======  ===  =================================  =============
aaa     ...  Original example instruction 1     example
bbb     ...  Original example instruction 2     example
ccc     ...  Added example instruction 3        examplev2
ddd     ...  Added example instruction 4        examplev2
======  ===  =================================  =============

Supporting the "examplev2" group thus requires supporting all four example instructions.

Deprecating instructions
------------------------
Deprecating instructions that are part of an existing conformance group can be done by defining a
new conformance group for the newly deprecated instructions, and defining a new conformance group
that supersedes the existing conformance group containing the instructions, where the new conformance
group includes the existing one and excludes the deprecated instruction group.

For example, if deprecating an instruction in an existing hypothetical group called "example", two new groups
("legacyexample" and "examplev2") might be registered in the BPF Instruction Conformance Group
Registry as follows:

=============  =============================  ========  =============  ===========
name           description                    includes  excludes       status
=============  =============================  ========  =============  ===========
example        Original example instructions  -         -              Permanent
legacyexample  Legacy example instructions    -         -              Historical
examplev2      Example instructions           example   legacyexample  Permanent
=============  =============================  ========  =============  ===========

The BPF Instruction Set Registry entries for the deprecated instructions would then be updated
to add "legacyexample" to the set of groups for those instructions, as follows:

======  ===  =================================  ======================
opcode  ...  description                        groups
======  ===  =================================  ======================
aaa     ...  Good original instruction 1        example
bbb     ...  Good original instruction 2        example
ccc     ...  Bad original instruction 3         example, legacyexample
ddd     ...  Bad original instruction 4         example, legacyexample
======  ===  =================================  ======================

Finally, updated implementations that dropped support for the deprecated instructions
would then be able to claim conformance to "examplev2" rather than "example".

Change Control
--------------

Registrations can be updated in a registry by the same mechanism as
required for an initial registration.  In cases where the original
definition of an entry is contained in an IESG-approved document,
update of the specification also requires IESG approval.

'Provisional' registrations can be updated by the original registrant
or anyone designated by the original registrant.  In addition, the
IESG can reassign responsibility for a 'Provisional' registration
or can request specific changes to an entry.
This will enable changes to be made to entries where the original
registrant is out of contact or unwilling or unable to make changes.

Transition from 'Provisional' to 'Permanent' status can be requested
and approved in the same manner as a new 'Permanent' registration.
Transition from 'Permanent' to 'Historical' status requires IESG
approval.  Transition from 'Provisional' to 'Historical' can be
requested by anyone authorized to update the 'Provisional'
registration.

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
