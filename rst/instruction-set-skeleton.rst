.. |docName| replace:: draft-ietf-bpf-isa-03
.. |ipr| replace:: trust200902
.. |category| replace:: std
.. |titleAbbr| replace:: BPF ISA
.. |abstract| replace:: eBPF (which is no longer an acronym for anything), also commonly referred to as BPF, is a technology with origins in the Linux kernel that can run untrusted programs in a privileged context such as an operating system kernel. This document specifies the BPF instruction set architecture (ISA).
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
.. |ref[RFC2119].title| replace:: Key words for use in RFCs to Indicate Requirement Levels
.. |ref[RFC2119].author[0].fullname| replace:: S. Bradner
.. |ref[RFC2119].author[0].initials| replace:: S.
.. |ref[RFC2119].author[0].surname| replace:: Bradner
.. |ref[RFC2119].type| replace:: normative
.. |ref[RFC2119].seriesInfo.name| replace:: BCP
.. |ref[RFC2119].seriesInfo.value| replace:: 14
.. |ref[RFC2119].seriesInfo.name| replace:: RFC
.. |ref[RFC2119].seriesInfo.value| replace:: 2119
.. |ref[RFC2119].seriesInfo.name| replace:: DOI
.. |ref[RFC2119].seriesInfo.value| replace:: 10.17487/RFC2119
.. |ref[RFC2119].target| replace:: https://www.rfc-editor.org/info/rfc2119
.. |ref[RFC2119].date.month| replace:: March
.. |ref[RFC2119].date.year| replace:: 1997
.. |ref[RFC8126].target| replace:: https://www.rfc-editor.org/rfc/rfc8126.html
.. |ref[RFC8126].title| replace:: Guidelines for Writing an IANA Considerations Section in RFCs
.. |ref[RFC8126].author[0].fullname| replace:: M. Cotton
.. |ref[RFC8126].author[0].initials| replace:: M.
.. |ref[RFC8126].author[0].surname| replace:: Cotton
.. |ref[RFC8126].author[1].fullname| replace:: B. Leiba
.. |ref[RFC8126].author[1].initials| replace:: B.
.. |ref[RFC8126].author[1].surname| replace:: Leiba
.. |ref[RFC8126].author[2].fullname| replace:: T. Narten
.. |ref[RFC8126].author[2].initials| replace:: T.
.. |ref[RFC8126].author[2].surname| replace:: Narten
.. |ref[RFC8126].type| replace:: normative
.. |ref[RFC8126].seriesInfo.name| replace:: BCP
.. |ref[RFC8126].seriesInfo.value| replace:: 26
.. |ref[RFC8126].seriesInfo.name| replace:: RFC
.. |ref[RFC8126].seriesInfo.value| replace:: 8126
.. |ref[RFC8126].seriesInfo.name| replace:: DOI
.. |ref[RFC8126].seriesInfo.value| replace:: 10.17487/RFC8126
.. |ref[RFC8126].date.month| replace:: June
.. |ref[RFC8126].date.year| replace:: 2017
.. |ref[LINUX].target| replace:: https://www.kernel.org/doc/html/latest/bpf/verifier.html
.. |ref[LINUX].title| replace:: eBPF verifier
.. |ref[LINUX].type| replace:: informative
.. |ref[PREVAIL].target| replace:: https://pldi19.sigplan.org/details/pldi-2019-papers/44/Simple-and-Precise-Static-Analysis-of-Untrusted-Linux-Kernel-Extensions
.. |ref[PREVAIL].title| replace:: Simple and Precise Static Analysis of Untrusted Linux Kernel Extensions
.. |ref[PREVAIL].type| replace:: informative
.. |ref[PREVAIL].author[0].fullname| replace:: E. Gershuni
.. |ref[PREVAIL].author[0].initials| replace:: E.
.. |ref[PREVAIL].author[0].surname| replace:: Gershuni
.. |ref[PREVAIL].author[1].fullname| replace:: N. Amit
.. |ref[PREVAIL].author[1].initials| replace:: N.
.. |ref[PREVAIL].author[1].surname| replace:: Amit
.. |ref[PREVAIL].author[2].fullname| replace:: A. Gurfinkel
.. |ref[PREVAIL].author[2].initials| replace:: A.
.. |ref[PREVAIL].author[2].surname| replace:: Gurfinkel
.. |ref[PREVAIL].author[3].fullname| replace:: N. Narodytska
.. |ref[PREVAIL].author[3].initials| replace:: N.
.. |ref[PREVAIL].author[3].surname| replace:: Narodytska
.. |ref[PREVAIL].author[4].fullname| replace:: J. Navas
.. |ref[PREVAIL].author[4].initials| replace:: J.
.. |ref[PREVAIL].author[4].surname| replace:: Navas
.. |ref[PREVAIL].author[5].fullname| replace:: N. Rinetzky
.. |ref[PREVAIL].author[5].initials| replace:: N.
.. |ref[PREVAIL].author[5].surname| replace:: Rinetzky
.. |ref[PREVAIL].author[6].fullname| replace:: L. Ryzhyk
.. |ref[PREVAIL].author[6].initials| replace:: L.
.. |ref[PREVAIL].author[6].surname| replace:: Ryzhyk
.. |ref[PREVAIL].author[7].fullname| replace:: M. Sagiv
.. |ref[PREVAIL].author[7].initials| replace:: M.
.. |ref[PREVAIL].author[7].surname| replace:: Sagiv
.. |ref[PREVAIL].date.month| replace:: June
.. |ref[PREVAIL].date.year| replace:: 2019
.. |ref[PREVAIL].seriesInfo.name| replace:: DOI
.. |ref[PREVAIL].seriesInfo.value| replace:: 10.1145/3314221.3314590
.. header::

.. include:: instruction-set.rst

Security Considerations
=======================

BPF programs could use BPF instructions to do malicious things with memory, CPU, networking,
or other system resources.  This is not fundamentally different from any other type of
software that may run on a device.  Execution environments should be carefully designed
to only run BPF programs that are trusted and verified, and sandboxing and privilege level
separation are key strategies for limiting security and abuse impact.  For example, BPF
verifiers are well-known and widely deployed and are responsible for ensuring that BPF programs
will terminate within a reasonable time, only interact with memory in safe ways, adhere to
platform-specified API contracts, and don't use instructions with undefined behavior.
This level of verification can often provide a stronger level
of security assurance than for other software and operating system code.
While the details are out of scope of this document,
`Linux <https://www.kernel.org/doc/html/latest/bpf/verifier.html>`_ and
`PREVAIL <https://pldi19.sigplan.org/details/pldi-2019-papers/44/Simple-and-Precise-Static-Analysis-of-Untrusted-Linux-Kernel-Extensions>`_ do provide many details.  Future IETF work will document verifier expectations
and building blocks for allowing safe execution of untrusted BPF programs.

Executing programs using the BPF instruction set also requires either an interpreter or a compiler
to translate them to hardware processor native instructions. In general, interpreters are considered a
source of insecurity (e.g., gadgets susceptible to side-channel attacks due to speculative execution)
whenever one is used in the same memory address space as data with confidentiality
concerns.  As such, use of a compiler is recommended instead.  Compilers should be audited
carefully for vulnerabilities to ensure that compilation of a trusted and verified BPF program
to native processor instructions does not introduce vulnerabilities.

Exposing functionality via BPF extends the interface between the component executing the BPF program and the
component submitting it. Careful consideration of what functionality is exposed and how
that impacts the security properties desired is required.

IANA Considerations
===================

This document defines two registries.

BPF Instruction Conformance Group Registry
------------------------------------------

This document defines an IANA registry for BPF instruction conformance groups, as follows:

* Name of the registry: BPF Instruction Conformance Groups
* Name of the registry group: BPF Instructions
* Required information for registrations: See `BPF Instruction Conformance Group Registration Template`_
* Syntax of registry entries: Each entry has the following fields: name, description, includes, excludes,
  status, and reference. See `BPF Instruction Conformance Group Registration Template`_ for more details.
* Registration policy (see `RFC 8126 section 4 <https://www.rfc-editor.org/rfc/rfc8126.html#section-4>`_ for details):

  * Permanent: Standards action or IESG Approval
  * Provisional: Specification required
  * Historical: Specification required

Initial entries in this registry are as follows:

.. table:: Initial conformance groups

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
  Any other conformance groups that are included by this group.

Excludes:
  Any other conformance groups that are excluded by this group.

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
  registry and the same registration policies apply.
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

.. table:: Conformance group example for addition

  =============  =================================  ========  ========  =========
  name           description                        includes  excludes  status
  =============  =================================  ========  ========  =========
  example        Original example instructions      -         -         Permanent
  examplev2      Newer set of example instructions  example   -         Permanent
  =============  =================================  ========  ========  =========

And then adding the new instructions into the BPF Instruction Set Registry as follows:

.. table:: Instruction addition example

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

.. table:: Conformance group example for deprecation

  =============  =============================  ========  =============  ===========
  name           description                    includes  excludes       status
  =============  =============================  ========  =============  ===========
  example        Original example instructions  -         -              Permanent
  legacyexample  Legacy example instructions    -         -              Historical
  examplev2      Example instructions           example   legacyexample  Permanent
  =============  =============================  ========  =============  ===========

The BPF Instruction Set Registry entries for the deprecated instructions would then be updated
to add "legacyexample" to the set of groups for those instructions, as follows:

.. table:: Instruction deprecation example

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
Quentin Monnet, Song Liu, Shung-Hsi Yu, Stanislav Fomichev, Watson Ladd, and Yonghong Song.

Appendix
========

.. include:: instruction-set-opcodes.rst
