#!/usr/bin/env python3

import argparse
import json
import os
import re

__hex = '0[xX][0-9a-fA-F]+'
HEX_RE = re.compile(__hex)
OP_RE = re.compile(f'^({__hex})\s+(any|{__hex})\s+(any|{__hex})\s+(.*\S)\s+`(.*)`_$')

class OpNotFound(BaseException):
    pass

def hex_to_dec(val):
    is_hex = HEX_RE.match(val)
    return int(val, 16) if is_hex else val

class Parser(object):
    def __init__(self, filename):
        self.reader = open(filename, 'r')
        self.line = ''
        self.ops = []

    def seek_to(self, target, help_message):
        self.reader.seek(0)
        offset = self.reader.read().find(target)
        if offset == -1:
            raise Exception(help_message)
        self.reader.seek(offset)
        self.reader.readline()
        self.line = self.reader.readline()

    def parse_line(self):
        capture = OP_RE.match(self.line)
        if not capture:
            raise OpNotFound

        insn = {
            'opc' : hex_to_dec(capture.group(1)),
            'src' : hex_to_dec(capture.group(2)),
            'imm' : hex_to_dec(capture.group(3))
            'dsc' : capture.group(4),
            'cat' : capture.group(5),
        }

        # Descriptions spans multiple lines.
        # Parse them, and seek back when meeting next instruction.
        if insn['dsc'] == 'lock::':
            while True:
                pos = self.reader.tell()
                line = self.reader.readline()
                if not line:
                    break
                if line == '\n':
                    continue
                capture = OP_RE.match(line)
                if not capture:
                    insn['dsc'] += '; ' + line.strip()
                else:
                    self.reader.seek(pos)
                    break

        self.ops.append(insn)

    def run(self):
        self.seek_to('Appendix',
                     'Could not find "Appendix" section')

        p = re.compile('^0[xX]')
        while True:
            self.line = self.reader.readline()
            if not self.line:
                break
            is_op = p.match(self.line)
            if not is_op:
                continue
            self.parse_line()

        self.reader.close()

    def print(self):
        print(json.dumps(self.ops, indent=2))

if __name__ == '__main__':
    input = os.path.join(os.getcwd(), 'instruction-set.rst')

    description='Convert eBPF ISA doc to a list of existing instructions (JSON)'
    argParser = argparse.ArgumentParser(description=description)
    if (os.path.isfile(input)):
        argParser.add_argument('--filename', help='input file', default=input)
    else:
        argParser.add_argument('--filename', help='input file')
    args = argParser.parse_args()

    # Parse file.
    parser = Parser(args.filename)
    parser.run()

    # Print formatted output to standard output.
    parser.print()
