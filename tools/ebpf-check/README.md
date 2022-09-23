# Validation Tools for eBPF Standard

/!\\ These tools (and the standard itself) are works in progress.

## Dependencies

awk, curl, llvm-objdump, pyelftools

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
script which sections to check in the object file.

```
$ ebpf-check.py -h
usage: ebpf-check.py [-h] [--sections SECTIONS] filename

Check instructions in provided ELF file and section for compliance with the eBPF ISA specification

positional arguments:
  filename             input ELF object file

optional arguments:
  -h, --help           show this help message and exit
  --sections SECTIONS  ELF section names
```

## Run on multiple object files

For convenience, `check-obj-in-dir.sh` is provided to validate all `TEXT`
sections in multiple ELF files at once. Example usage:

```
$ cd cilium/bpf
$ make -j
$ /path/to/check-obj-in-dir.sh .
```
