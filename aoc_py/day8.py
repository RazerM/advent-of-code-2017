import operator
import re

from collections import defaultdict

with open('../input/8.txt') as fp:
    instructions = [l.strip() for l in fp]

registers = defaultdict(int)

re_instruction = re.compile(
    r'''
        (?P<register1>\w+)
        \s+
        (?P<instruction>\w+)
        \s+
        (?P<value1>-?\d+)
        \s+
        if
        \s+
        (?P<register2>\w+)
        \s+
        (?P<comparison><=|<|==|>|>=|!=)
        \s+
        (?P<value2>-?\d+)
    ''',
    flags=re.VERBOSE
)


comparisons = {
    '<=': operator.le,
    '<': operator.lt,
    '==': operator.eq,
    '>': operator.gt,
    '>=': operator.ge,
    '!=': operator.ne,
}

functions = {
    'inc': lambda a, b: a + b,
    'dec': lambda a, b: a - b,
}


def check(register, comparison, value):
    reg_value = registers[register]
    return comparisons[comparison](reg_value, value)


def operate(register, instruction, value):
    reg_value = registers[register]
    registers[register] = functions[instruction](reg_value, value)


highest_ever = 0

for instruction in instructions:
    match = re_instruction.match(instruction)
    d = match.groupdict()

    if check(d['register2'], d['comparison'], int(d['value2'])):
        operate(d['register1'], d['instruction'], int(d['value1']))

    highest_ever = max(highest_ever, max(registers.values()))

print('Part 1:', max(registers.values()))
print('Part 2:', highest_ever)

