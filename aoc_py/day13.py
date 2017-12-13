from collections import OrderedDict
from itertools import count

data = OrderedDict()

with open('../input/13.txt') as fp:
    for line in fp:
        depth, range_ = line.strip().split(': ')
        data[int(depth)] = int(range_)


# input file is ordered, but let's not rely on that
layer_severity = OrderedDict(sorted(data.items(), key=lambda t: t[0]))


def attempt_passthrough(delay=0, fast_finish=False):
    caught = False
    severity = 0

    for depth, range_ in layer_severity.items():
        time = depth + delay

        # scanner returns to top every 2(x-1) steps
        if time % (2 * range_ - 2) == 0:
            caught = True
            severity += depth * range_
            if fast_finish:
                # severity not valid if we break early
                severity = None
                break

    return caught, severity


def part1():
    caught, severity = attempt_passthrough()
    assert caught
    print('Part 1:', severity)


def part2():
    for delay in count():
        caught, _ = attempt_passthrough(delay, fast_finish=True)

        if not caught:
            print('Part 2:', delay)
            break

part1()
part2()
