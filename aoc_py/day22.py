from collections import defaultdict

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3


def load_grid():
    with open('../input/22.txt') as fp:
        initial_grid = [
            [INFECTED if c == '#' else CLEAN for c in l.strip()]
            for l in fp
        ]

    grid = defaultdict(int)

    width = len(initial_grid[0])
    height = len(initial_grid)

    # positive axes are right and down
    for y, row in enumerate(initial_grid, start=-(height // 2)):
        for x, infected in enumerate(row, start=-(width // 2)):
            grid[(x, y)] = infected

    return grid


def turn_left(dir):
    return dir[1], -dir[0]


def turn_right(dir):
    return -dir[1], dir[0]


def reverse(dir):
    return -dir[0], -dir[1]


def part1(grid):
    pos = 0, 0
    dir = 0, -1

    infected = 0

    for i in range(10000):
        state = grid[pos]
        if state:
            grid[pos] = CLEAN
            dir = turn_right(dir)
        else:
            infected += 1
            grid[pos] = INFECTED
            dir = turn_left(dir)

        pos = pos[0] + dir[0], pos[1] + dir[1]

    return infected


def part2(grid):
    pos = 0, 0
    dir = 0, -1

    infected = 0

    for i in range(10000000):
        state = grid[pos]
        if state == CLEAN:
            dir = turn_left(dir)
            grid[pos] = WEAKENED
        elif state == WEAKENED:
            infected += 1
            grid[pos] = INFECTED
        elif state == INFECTED:
            dir = turn_right(dir)
            grid[pos] = FLAGGED
        elif state == FLAGGED:
            dir = reverse(dir)
            grid[pos] = CLEAN
        else:
            raise ValueError(state)

        pos = pos[0] + dir[0], pos[1] + dir[1]

    return infected


if __name__ == '__main__':
    grid = load_grid()
    print('Part 1:', part1(grid.copy()))
    print('Part 2:', part2(grid.copy()))
