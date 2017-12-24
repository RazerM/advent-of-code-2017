from collections import defaultdict
from itertools import count

import attr
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

grammar = r'''
    document = instruction (ws instruction)* EOF
    instruction = set / sub / mul / jnz
    set = "set" ws param ws param
    sub = "sub" ws param ws param
    mul = "mul" ws param ws param
    jnz = "jnz" ws param ws param
    ws = r'\s+'
    param = register / int
    register = r'[a-z]+'
    int = "-"? digit+
    digit = r'[0-9]'
'''

parser = ParserPEG(grammar, root_rule_name='document', skipws=False)


class AssemblyVisitor(PTNodeVisitor):
    def visit_document(self, node, children):
        return children

    def visit_set(self, node, children):
        return Instruction('set', children)

    def visit_sub(self, node, children):
        return Instruction('sub', children)

    def visit_mul(self, node, children):
        return Instruction('mul', children)

    def visit_jnz(self, node, children):
        return Instruction('jnz', children)

    def visit_register(self, node, children):
        return Register(node.value)

    def visit_int(self, node, children):
        return int(''.join(children))

    def visit_ws(self, node, children):
        return


@attr.s
class Instruction:
    keyword = attr.ib()
    args = attr.ib()

    def get_register(self, i):
        return self.args[i].name

    def get_value(self, i, registers):
        x = self.args[i]
        if isinstance(x, Register):
            return registers[x.name]

        return x


@attr.s(cmp=True, frozen=True)
class Register:
    name = attr.ib()


def parse_assembly(assembly):
    parse_tree = parser.parse(assembly)
    return visit_parse_tree(parse_tree, AssemblyVisitor())


def run(instructions, registers):
    i = 0
    num_mul = 0

    while i < len(instructions):
        inst = instructions[i]

        if inst.keyword == 'set':
            reg = inst.get_register(0)
            value = inst.get_value(1, registers)
            registers[reg] = value
        elif inst.keyword == 'sub':
            reg = inst.get_register(0)
            value = inst.get_value(1, registers)
            registers[reg] -= value
        elif inst.keyword == 'mul':
            reg = inst.get_register(0)
            value = inst.get_value(1, registers)
            registers[reg] *= value
            num_mul += 1
        elif inst.keyword == 'jnz':
            value = inst.get_value(0, registers)
            offset = inst.get_value(1, registers)
            if value != 0:
                i += offset - 1
        else:
            raise RuntimeError(inst)

        i += 1

    return num_mul


def part2():
    h = 0
    b = 57 * 100 + 100000
    c = b + 17000

    for i in count():
        if i % 100 == 0:
            print('.', end='', flush=True)

        f = True
        d = 2
        while d != b:
            if b % d == 0:
                f = False
            d += 1
        if not f:
            h += 1
        if b == c:
            break
        b += 17
    print()
    return h


def main():
    with open('../input/23.txt') as fp:
        instrs = parse_assembly(fp.read().strip())

    registers0 = defaultdict(int)
    registers0['a'] = 0

    mul_invoked = run(instrs, registers0)
    print('Part 1:', mul_invoked)
    print('Part 2:', part2())


if __name__ == '__main__':
    main()
