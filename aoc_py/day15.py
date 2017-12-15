import re
from itertools import islice


FACTORS = dict(a=16807, b=48271)
LOW16 = (2 ** 16) - 1


def load_data():
    """I suspected part 2 would have a big list of generators so this is
    overly-generic
    """
    starts = dict()

    with open('../input/15.txt') as fp:
        for line in fp:
            match = re.match(r'Generator (\w+) starts with (\d+)', line)
            name, start = match.groups()
            start = int(start)
            starts[name.lower()] = start

    return starts


def generator(start, factor, multiples_of=None):
    current = start

    while True:
        current *= factor
        current %= 2147483647

        if multiples_of is None or current % multiples_of == 0:
            yield current & LOW16


def sum_equal(a, b, *, limit):
    sample = islice(zip(a, b), limit)
    return sum(1 for x, y in sample if x == y)


def part1(starts):
    gen_a = generator(starts['a'], FACTORS['a'])
    gen_b = generator(starts['b'], FACTORS['b'])
    print('Part 1:', sum_equal(gen_a, gen_b, limit=int(40e6)))


def part2(starts):
    gen_a = generator(starts['a'], FACTORS['a'], 4)
    gen_b = generator(starts['b'], FACTORS['b'], 8)
    print('Part 2:', sum_equal(gen_a, gen_b, limit=int(5e6)))


if __name__ == '__main__':
    starts = load_data()
    part1(starts)
    part2(starts)
