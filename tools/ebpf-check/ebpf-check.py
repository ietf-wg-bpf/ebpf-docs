#!/usr/bin/env python3

import argparse
import json
import os
import sys

import json

from elftools.elf.elffile import ELFFile

OPS_JON = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                       'instructions.json')

class ISA(object):
    def __init__(self):
        file = open(OPS_JON, 'r')
        self.ops = json.load(file)
        file.close()

def get_insn(insn):
    if sys.byteorder == 'little':
        return {
            'opc': insn[0],
            'dst': insn[1] & 0x0f,
            'src': (insn[1] & 0xf0) >> 4,
            'off': insn[2] + (insn[3] << 8),
            'imm': insn[4] + (insn[5] << 8) + (insn[6] << 16) + (insn[7] << 24)
        }
    else:
        return {
            'opc': insn[7],
            'dst': (insn[6] & 0xf0) >> 4,
            'src': insn[6] & 0x0f,
            'off': insn[5] + (insn[4] << 8),
            'imm': insn[3] + (insn[2] << 8) + (insn[1] << 16) + (insn[0] << 24)
        }

def process_insn(isa, prev_insn_data, insn_data, next_insn_data,
                 filename, section_name, insn_nb):
    is_valid = False
    insn = get_insn(insn_data)

    for op in isa.ops:
        if op['opc'] == insn['opc']:
            if op['src'] != 'any' and op['src'] != insn['src']:
                continue
            if op['imm'] != 'any' and op['imm'] != insn['imm']:
                continue
            is_valid = True
            break

    if not is_valid:
        print(f'{filename}:{section_name}:{insn_nb}:{insn}: Not a valid instruction')
        return is_valid

    # Check that 0x18 is 16-bytes long and followed by a 0x00 opcode
    if insn['opc'] == 0x18:
        next_insn = get_insn(next_insn_data)
        if not next_insn:
            print(f'{filename}:{section_name}:{insn_nb}:{insn}: 0x18 misses its second half-instruction')
            is_valid = False
        if next_insn['opc'] != 0x00:
            print(f'{filename}:{section_name}:{insn_nb}:{insn}: 0x18 not followed by 0x00 second half-instruction')
            is_valid = False

    # Check that 0x00 opcode is preceeded by 0x18
    if insn['opc'] == 0x00:
        prev_insn = get_insn(prev_insn_data)
        if prev_insn['opc'] != 0x18:
            print(f'{filename}:{section_name}:{insn_nb}:{insn}: 0x00 not preceeded by 0x18 first half-instruction')
            is_valid = False

    return is_valid

def process_section(isa, section, filename):
    insn_size = 8
    if section.data_size % insn_size:
        raise Exception(f'Data length in section {section.name} is not a multiple of {insn_size} bytes')

    is_valid = True
    insn = {}
    next_insn = section.data()[0:insn_size]
    for i in range(section.data_size // insn_size - 1):
        prev_insn = insn
        insn = next_insn
        if i == (section.data_size // insn_size - 1):
            next_insn = {}
        else:
            next_insn = section.data()[(i+1)*insn_size:(i+2)*insn_size]
        if not process_insn(isa, prev_insn, insn, next_insn,
                            filename, section.name, i):
            is_valid = False

    return is_valid

def process_file(isa, filename, section_names):
    is_valid = True
    with open(filename, 'rb') as f:
        elffile = ELFFile(f)
        for section_name in section_names.split(','):
            section = elffile.get_section_by_name(section_name)
            if not section:
                raise Exception(f'File {filename}: section "{section_name}" not found!')
            if not process_section(isa, section, filename):
                is_valid = False

        f.close()

    return is_valid

if __name__ == '__main__':
    description='Check instructions in provided ELF file and section for compliance with the eBPF ISA specification'
    argParser = argparse.ArgumentParser(description=description)
    argParser.add_argument('filename', help='input ELF object file')
    argParser.add_argument('--sections', help='Comma-separated list of ELF section names',
                           default='.text')
    args = argParser.parse_args()

    isa = ISA()
    if not process_file(isa, args.filename, args.sections):
        sys.exit(1)
