.. contents::
.. sectnum::

====================================
eBPF ELF Profile Specification, v1.0
====================================

The Executable and Linking Format (ELF) is specified in
Tool Interface Standard (TIS), "Executable and Linking Format (ELF) Specification, Version 1.2", May 1995, https://refspecs.linuxbase.org/elf/elf.pdf.

This document specifies version 1.0 of the eBPF profile for ELF files.

Documentation conventions
=========================

All integer fields are unsigned.

TEXT Sections
=============

`eBPF programs <instruction-set.rst#instruction-encoding>`_ are stored in TEXT sections.
A TEXT section can contain multiple eBPF programs, each with a different program name
which is stored as a function in a TEXT section.  The ".text" section can be empty if
eBPF programs are stored in other TEXT sections.

This specification does not mandate any particular convention for TEXT section names,
as there are multiple different conventions in use today, including:

* Prefix Convention: The section name is prefixed with a string that
  identifies the program type, so that the program type of any programs in the section
  can be determined by finding the longest substring match across all program type prefixes.

* Exact Match Convention: The section name is a string that identifies the program type
  of any programs in the section.

* Arbitrary Convention: The section name can be anything and the program type of any
  programs in the section must be determined without consulting the section name.

DATA Sections
=============

BTF Map Templates
--------------------

BTF eBPF map templates are stored in a DATA section named ".maps".
The number of map templates in a section can be determined by counting the
number of symbols in the ".symtab" section that point into the ".maps" section.

TODO: add format description here

Legacy Map Templates
--------------------

Legacy eBPF map templates are stored in DATA sections named "maps" or matching
"maps/<map-name>".  Each such section can contain 0 or more map templates.
The number of map templates in a section can be determined by counting the
number of symbols in the ".symtab" section that point into that maps section.

The size of a map template can be calculated as:

``(size of maps section) / (count of map templates in that section)``

The format of a map template is as follows:

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------------------------------------------------------+
    |                             Type                              |
    +---------------------------------------------------------------+
    |                           Key Size                            |
    +---------------------------------------------------------------+
    |                          Value Size                           |
    +---------------------------------------------------------------+
    |                          Max Entries                          |
    +---------------------------------------------------------------+
    |                        Inner Map Index                        |
    +---------------------------------------------------------------+
    |                                                               |
    |                    Platform-specific data                     |
    |                        (variable size)                        |
    |                                                               |
    +---------------------------------------------------------------+

Type
  An integer identifying the map type.  Its value and meaning are platform-specific.

Key Size
  Size in bytes of keys in the map, if any.

Value Size
  Size in bytes of values in the map, if any.

Max Entries
  Maximum number of entries in the map, if the map type has a maximum.

Inner Map Index
  If the map type is one whose values contain ids of other maps, then the inner
  map index must be set to the 0-based index of another map template in the section.
  The referenced map template is used to enforce that any maps must match it
  for their ids to be allowed as values of this map.  If the map type is not
  one whose values contain ids of other maps, this must be set to 0.

Platform-specific data
  This field and its size is up to the runtime platform to define.

Other Sections
==============

============  ================================
section name  reference
============  ================================
license       `Program License`_
version       `Runtime Version restriction`_
.BTF          `Type and String Data`_
.BTF.ext      `Function and Line Information`_
============  ================================


Program License
---------------

A runtime can optionally restrict what program types and/or helper functions
can be used based on what license the eBPF program is under.  This information
can be placed into the ELF file in a section named "license" whose contents
is a null-terminated SPDX license expression as specified in Annex D of
ISO/IEC 5962:2021, "Information technology -- SPDX® Specification V2.",
https://www.iso.org/standard/81870.html.

Runtime Version restriction
---------------------------

A runtime can optionally restrict whether an eBPF program can load based
on what runtime version it was designed to interact with.  This information
can be placed into the ELF file in a section named "version" containing
a 4-byte version identifier whose use is runtime-specific.

Type and String Data
--------------------

The optional ".BTF" section contains type and string data. 

The section starts with the following header:

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-------------------------------+-------------------------------+
    |              Magic            |    Version    |     Flags     |
    +-------------------------------+---------------+---------------+
    |                         Header Length                         |
    +---------------------------------------------------------------+
    |                       Type data offset                        |
    +---------------------------------------------------------------+
    |                       Type data length                        |
    +---------------------------------------------------------------+
    |                      String data offset                       |
    +---------------------------------------------------------------+
    |                      String data length                       |
    +---------------------------------------------------------------+

Magic
  Must be set to 0xeB9F, which can be used by a parser to determine whether multi-byte fields
  are in little-endian or big-endian byte order.

Version
  Must be set to 1 (0x01).

Flags
  Must be set to 0.

Header Length
  Must be set to 24 (0x00000018).

Type data offset
  Offset in bytes relative to the end of the header.

Type data length
  Size in bytes of the type data.  Must be set to 8 (0x00000008).

String data offset
  Offset in bytes, relative to the end of the header, of the
  start of the `String data`_.

String data length
  Size in bytes of the `String data`_.  Must be set to 16 (0x00000010).

String data
~~~~~~~~~~~

The string data contains a concatenation of null-terminated UTF-8 strings,

Function and Line Information
-----------------------------

The optional ".BTF.ext" section contains source line information for the first eBPF instruction
for each source line.

The section starts with the following header:

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-------------------------------+-------------------------------+
    |              Magic            |    Version    |     Flags     |
    +-------------------------------+---------------+---------------+
    |                         Header Length                         |
    +---------------------------------------------------------------+
    |                     Function info offset                      |
    +---------------------------------------------------------------+
    |                     Function info length                      |
    +---------------------------------------------------------------+
    |                       Line info offset                        |
    +---------------------------------------------------------------+
    |                       Line info length                        |
    +---------------------------------------------------------------+
    |                                                               |
    |                    Platform-specific data                     |
    |                        (variable size)                        |
    |                                                               |
    +---------------------------------------------------------------+

Magic
  Must be set to 0xeB9F, which can be used by a parser to determine whether multi-byte fields
  are in little-endian or big-endian byte order.

Version
  Must be set to 1 (0x01).

Flags
  Must be set to 0.

Header Length
  Must be set to 24 (0x00000018) or 32 (0x00000020).

Function info offset
  Offset in bytes past the end of the header, of the start of the `Function information`_.

Function info length
  Size in bytes of the `Function information`_.  Must be set to 8 (0x00000008).

Line info offset
  Offset in bytes past the end of the header, of the start of the `Line Information`_.

Line info length
  Size in bytes of the `Line Information`_.  Must be set to 16 (0x00000010).

Platform-specific data
  This field and its size is up to the runtime platform to define.

Function information
~~~~~~~~~~~~~~~~~~~~

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------------------------------------------------------+
    |                     Function record size                      |
    +---------------------------------------------------------------+
    |                                                               |
    |                       Function info 1                         |
    |                                                               |
    +---------------------------------------------------------------+
    |                              ...                              |
    +---------------------------------------------------------------+
    |                                                               |
    |                       Function info N                         |
    |                                                               |
    +---------------------------------------------------------------+

Function record size
  Size in bytes of each function record contained in an `Info block`_.
  Must be set to 8 (0x00000008).

Function info 1..N
  A set of `Info block`_ data blobs, as many as will fit in the size given
  as the "Function info length", where each record within an info block is
  formatted as shown under `Function Record`_ below.

Info block
~~~~~~~~~~

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------------------------------------------------------+
    |                     Section name offset                       |
    +---------------------------------------------------------------+
    |                         Record count                          |
    +---------------------------------------------------------------+
    |                                                               |
    |                           Record 1                            |
    |                                                               |
    +---------------------------------------------------------------+
    |                   ...                                         |
    +---------------------------------------------------------------+
    |                                                               |
    |                           Record N                            |
    |                                                               |
    +---------------------------------------------------------------+

Section name offset
  Offset in bytes of the section name within the `String data`_.

Record count
  Number of records that follow.  Must be greater than 0.

Record 1..N
  A series of records.

Function Record
~~~~~~~~~~~~~~~

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------------------------------------------------------+
    |                     Instruction offset                        |
    +---------------------------------------------------------------+
    |                           Type id                             |
    +---------------------------------------------------------------+

Instruction offset
  Offset in bytes from the start of the section whose name is
  given by "Section name offset".  Must be 0 for Record 1, and
  for subsequent records it must be greater than the instruction offset
  of the previous record.

Type id
  TODO: Add a definition of this field.

Line Information
~~~~~~~~~~~~~~~~

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------------------------------------------------------+
    |                        Line record size                       |
    +---------------------------------------------------------------+
    |                                                               |
    |                          Line info 1                          |
    |                                                               |
    +---------------------------------------------------------------+
    |                              ...                              |
    +---------------------------------------------------------------+
    |                                                               |
    |                          Line info N                          |
    |                                                               |
    +---------------------------------------------------------------+

Line record size
  Size in bytes of each line record in an `Info block`_.  Must be set to 16 (0x00000010).

Line info 1..N
  A set of `Info block`_ data blobs, as many as will fit in the size given as the "Line info length",
  where each record within an info block is formatted as shown under `Line Record`_ below.

Line Record
~~~~~~~~~~~

.. code-block::

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +---------------------------------------------------------------+
    |                      Instruction offset                       |
    +---------------------------------------------------------------+
    |                       File name offset                        |
    +---------------------------------------------------------------+
    |                      Source line offset                       |
    +---------------------------------------------------------------+
    |                Line number and column number                  |
    +---------------------------------------------------------------+

Instruction offset
  0-based instruction index into the eBPF program contained
  in the section whose name is referenced in the `Info block`_.

File name offset
  Offset in bytes of the file name within the `String data`_.

Source line offset
  Offset in bytes of the source line within the `String data`_.

Line number and column number
  The line and column number value, computed as
  ``(line number << 10) | (column number)``.
