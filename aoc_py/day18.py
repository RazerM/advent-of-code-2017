import asyncio
from collections import defaultdict
from itertools import count

import attr
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

grammar = r'''
    document = instruction (ws instruction)* EOF
    instruction = snd / set / add / mul / mod / rcv / jgz
    snd = "snd" ws param
    set = "set" ws param ws param
    add = "add" ws param ws param
    mul = "mul" ws param ws param
    mod = "mod" ws param ws param
    rcv = "rcv" ws param
    jgz = "jgz" ws param ws param
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

    def visit_snd(self, node, children):
        return Instruction('snd', children)

    def visit_set(self, node, children):
        return Instruction('set', children)

    def visit_add(self, node, children):
        return Instruction('add', children)

    def visit_mul(self, node, children):
        return Instruction('mul', children)

    def visit_mod(self, node, children):
        return Instruction('mod', children)

    def visit_rcv(self, node, children):
        return Instruction('rcv', children)

    def visit_jgz(self, node, children):
        return Instruction('jgz', children)

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


with open('../input/18.txt') as fp:
    instructions = parse_assembly(fp.read().strip())


async def run(registers, q_rcv, q_snd, wait_rcv, wait_snd):
    i = 0
    num_sent = 0

    while i < len(instructions):
        inst = instructions[i]

        if inst.keyword == 'snd':
            value = inst.get_value(0, registers)
            await q_snd.put(value)
            num_sent += 1
        elif inst.keyword == 'set':
            reg = inst.get_register(0)
            value = inst.get_value(1, registers)
            registers[reg] = value
        elif inst.keyword == 'add':
            reg = inst.get_register(0)
            value = inst.get_value(1, registers)
            registers[reg] += value
        elif inst.keyword == 'mul':
            reg = inst.get_register(0)
            value = inst.get_value(1, registers)
            registers[reg] *= value
        elif inst.keyword == 'mod':
            reg = inst.get_register(0)
            value = inst.get_value(1, registers)
            registers[reg] %= value
        elif inst.keyword == 'rcv':
            reg = inst.get_register(0)
            wait_rcv.set()

            deadlock = False

            while True:
                # Both queues being empty is necessary but not sufficient to
                # detect deadlock. The other task must also be waiting on our
                # queue, so check for the wait_snd event.

                if wait_snd.is_set() and q_snd.empty() and q_rcv.empty():
                    deadlock = True
                    break

                try:
                    received = q_rcv.get_nowait()
                except asyncio.QueueEmpty:
                    # yield to event loop
                    await asyncio.sleep(0)
                else:
                    registers[reg] = received
                    wait_rcv.clear()
                    break

            if deadlock:
                break
        elif inst.keyword == 'jgz':
            value = inst.get_value(0, registers)
            offset = inst.get_value(1, registers)
            if value > 0:
                i += offset - 1

        i += 1

    return num_sent


async def main():
    pid = iter(count())
    registers0 = defaultdict(int)
    registers1 = defaultdict(int)

    registers0['p'] = next(pid)
    registers1['p'] = next(pid)

    q0 = asyncio.Queue()
    q1 = asyncio.Queue()

    wait0 = asyncio.Event()
    wait1 = asyncio.Event()

    task0 = asyncio.ensure_future(
        run(registers0, q_rcv=q0, q_snd=q1, wait_rcv=wait0, wait_snd=wait1))
    task1 = asyncio.ensure_future(
        run(registers1, q_rcv=q1, q_snd=q0, wait_rcv=wait1, wait_snd=wait0))

    _, sent1 = await asyncio.gather(task0, task1)

    print('Part 2:', sent1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
