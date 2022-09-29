# Validation Tools for eBPF Standard

/!\\ These tools (and the standard itself) are works in progress.

## Dependencies

awk, curl, pyelftools

## Setup

```
$ make
```

The command above should create two files. The first one is the RST
documentation for the eBPF ISA, retrieved with `get-from-gh.sh` from the
relevant branch in the GitHub repository, and saved locally as
`instruction-set.rst`.

Then `make` creates the second file by running `docs-to-ops.py` and saving the
output into `instructions.json`, to produce a JSON list of valid instructions
from the RST docs.

## Run

After the list of instructions has been generated, call `ebpf-check.py` to
check an object file. You can pass one or more ELF section names to tell the
script which sections to check in the object file. By default, the script
processes all `TEXT` sections.

```
$ ebpf-check.py -h
usage: ebpf-check.py [-h] [-j] [-s SECTIONS [SECTIONS ...]] [-v] filenames [filenames ...]

Check instructions in provided ELF file and section for compliance with the eBPF ISA specification

positional arguments:
  filenames             input ELF object file

optional arguments:
  -h, --help            show this help message and exit
  -j, --json            JSON output
  -s SECTIONS [SECTIONS ...], --sections SECTIONS [SECTIONS ...]
                        list of ELF section names, defaults to all TEXT sections in file
  -v, --verbose         verbose output
```

## Run on multiple object files

It is possible to run the script on all `TEXT` sections of multiple object
files at once. For example:

```
$ cd cilium/bpf
$ make -j
$ /path/to/ebpf-check.py --all-sections *.o
```
