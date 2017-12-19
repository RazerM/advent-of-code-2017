import string

import numpy as np

with open('../input/19.txt') as fp:
    lines = list(fp)


pos = np.array([lines[0].index('|'), 0])
direction = np.array([0, 1])
N = np.array([0, -1])
E = np.array([1, 0])
S = np.array([0, 1])
W = np.array([-1, 0])


def get_char(pos):
    try:
        return lines[pos[1]][pos[0]]
    except IndexError:
        return None


def change_direction(pos, direction):
    up = pos + N
    right = pos + E
    down = pos + S
    left = pos + W

    been = pos - direction

    if get_char(up) == '|' and np.any(up != been):
        direction[:] = N
    elif get_char(right) == '-' and np.any(right != been):
        direction[:] = E
    elif get_char(down) == '|' and np.any(down != been):
        direction[:] = S
    elif get_char(left) == '-' and np.any(left != been):
        direction[:] = W


found = []
steps = 0

while True:
    char = get_char(pos)
    if char in {'|', '-'}:
        pass
    elif char == '+':
        change_direction(pos, direction)
    elif char in string.ascii_uppercase:
        found.append(char)
    else:
        break
    pos += direction
    steps += 1

print('Part 1:', ''.join(found))
print('Part 2:', steps)
