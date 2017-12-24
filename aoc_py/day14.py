from itertools import chain, product
from queue import Queue

import numpy as np

from day10 import knot_hash


def disk_state(key):
    for row in range(128):
        s = f'{key}-{row}'
        hash = knot_hash(s)
        values = (int(c, 16) for c in hash)
        bin_row = chain.from_iterable(f'{b:04b}' for b in values)
        bool_row = (bool(int(b)) for b in bin_row)
        yield bool_row


def part1(key):
    squares = sum(sum(row) for row in disk_state(key))
    print('Part 1:', squares)


def get_grid(state):
    grid = []
    for row in state:
        grid.append(''.join('#' if x else '.' for x in row))
    return grid


def get_num_grid(state):
    return np.array([[int(x) for x in row] for row in state])


def flood(grid, pos, replacement, target=1):
    if grid[pos] == replacement or grid[pos] != target:
        return False

    queue = Queue()

    def flood_node(pos):
        if grid[pos] == target:
            grid[pos] = replacement
            queue.put(pos)

    nrows, ncols = grid.shape

    grid[pos] = replacement
    queue.put(pos)
    while True:
        pos = queue.get()

        if pos[0] > 0:
            north = pos[0] - 1, pos[1]
            flood_node(north)
        if pos[0] < nrows - 1:
            south = pos[0] + 1, pos[1]
            flood_node(south)
        if pos[1] > 0:
            west = pos[0], pos[1] - 1
            flood_node(west)
        if pos[1] < ncols - 1:
            east = pos[0], pos[1] + 1
            flood_node(east)

        if queue.empty():
            break

    return True


def part2(key):
    state = list(disk_state(key))

    grid = get_num_grid(state)
    nrows, ncols = grid.shape

    replacement = replacement_start = 2

    for row, col in product(range(nrows), range(ncols)):
        replaced = flood(grid, (row, col), replacement)
        if replaced:
            replacement += 1

    print('Part 2:', replacement - replacement_start)


if __name__ == '__main__':
    key = 'hfdlxzhv'
    part1(key)
    part2(key)
