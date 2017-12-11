import numpy as np

# Use cube coordinates
# https://www.redblobgames.com/grids/hexagons/#coordinates
dirmap = {
    'n': np.array([0, 1, -1]),
    's': np.array([0, -1, 1]),
    'ne': np.array([1, 0, -1]),
    'sw': np.array([-1, 0, 1]),
    'se': np.array([1, -1, 0]),
    'nw': np.array([-1, 1, 0]),
}


with open('../input/11.txt') as fp:
    directions = [dirmap[d] for d in fp.read().strip().split(',')]


def hex_distance(a, b):
    c = a - b
    return max(c.min(), c.max(), key=abs)


pos = np.array([0, 0, 0])
target = np.array([0, 0, 0])
max_dist = 0

for dir in directions:
    pos += dir
    max_dist = max(max_dist, hex_distance(pos, target))


print('Part 1:', hex_distance(pos, target))
print('Part 2:', max_dist)
