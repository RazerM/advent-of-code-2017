from collections import defaultdict

import attr


@attr.s
class Write:
    value = attr.ib()


@attr.s
class Move:
    direction = attr.ib()


@attr.s
class Continue:
    state = attr.ib()


states = {
    'A': [
        [
            Write(1),
            Move('right'),
            Continue('B'),
        ],
        [
            Write(0),
            Move('left'),
            Continue('B'),
        ]
    ],
    'B': [
        [
            Write(1),
            Move('left'),
            Continue('C'),
        ],
        [
            Write(0),
            Move('right'),
            Continue('E'),
        ]
    ],
    'C': [
        [
            Write(1),
            Move('right'),
            Continue('E'),
        ],
        [
            Write(0),
            Move('left'),
            Continue('D'),
        ]
    ],
    'D': [
        [
            Write(1),
            Move('left'),
            Continue('A'),
        ],
        [
            Write(1),
            Move('left'),
            Continue('A'),
        ]
    ],
    'E': [
        [
            Write(0),
            Move('right'),
            Continue('A'),
        ],
        [
            Write(0),
            Move('right'),
            Continue('F'),
        ]
    ],
    'F': [
        [
            Write(1),
            Move('right'),
            Continue('E'),
        ],
        [
            Write(1),
            Move('right'),
            Continue('A'),
        ]
    ],
}

state = 'A'
steps = 12683008

pos = 0
tape = defaultdict(int)

for _ in range(steps):
    instrs = states[state][tape[pos]]

    for instr in instrs:
        if isinstance(instr, Write):
            tape[pos] = instr.value
        elif isinstance(instr, Move):
            if instr.direction == 'left':
                pos -= 1
            else:
                pos += 1
        elif isinstance(instr, Continue):
            state = instr.state

print(sum(tape.values()))
