from collections import deque


def spinlock(steps, loops, after):
    buffer = deque([0])
    position = 0

    for i in range(1, loops + 1):
        position += steps
        position %= len(buffer)

        buffer.insert(position + 1, i)

        position += 1

    return buffer[buffer.index(after) + 1]


def spinlock_zero(steps, loops):
    position = 0
    after0 = None

    for i in range(1, loops + 1):
        position += steps
        position %= i  # i == buffer length

        if position == 0:
            after0 = i

        position += 1

    return after0


if __name__ == '__main__':
    steps = 335
    print('Part 1:', spinlock(steps, loops=2017, after=2017))
    print('Part 2:', spinlock_zero(steps, loops=int(50e6)))


