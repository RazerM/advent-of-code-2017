from binascii import hexlify
from functools import reduce
from itertools import zip_longest
from operator import xor


def coalesce(*args):
    try:
        return next(a for a in args if a is not None)
    except StopIteration:
        raise ValueError('All args are None') from None


def slice_as_range(s, collection):
    start = coalesce(s.start, 0)
    stop = coalesce(s.stop, len(collection))
    step = coalesce(s.step, 1)

    return range(start, stop, step)


class CycleList(list):
    """A list where slicing wraps around to start for
    numbers greater than the length
    """
    def __setitem__(self, key, value):
        if isinstance(key, slice):
            r = slice_as_range(key, self)
            value = list(value)

            if len(value) != len(r):
                raise NotImplementedError("Didn't need it, so not implemented.")

            for i, v in zip(r, value):
                super().__setitem__(i % len(self), v)
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key):
        if isinstance(key, slice):
            r = slice_as_range(key, self)
            # super() doesn't work here, hmmm
            return [list.__getitem__(self, i % len(self)) for i in r]

        return super().__getitem__(key)


def sparse_hash(lengths, rounds=1):
    pos = 0
    skip = 0
    nums = CycleList(range(256))

    for _ in range(rounds):
        for length in lengths:
            end = pos + length
            nums[pos:end] = reversed(nums[pos:end])
            pos += length + skip
            skip += 1

    return nums


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def dense_hash(nums):
    return [reduce(xor, c) for c in grouper(nums, 16)]


with open('../input/10.txt') as fp:
    input = fp.read().strip()
    part1_lengths = [int(x) for x in input.split(',')]
    part2_lengths = [ord(c) for c in input] + [17, 31, 73, 47, 23]


def part1():
    nums = sparse_hash(part1_lengths)
    return nums[0] * nums[1]


def part2():
    nums = sparse_hash(part2_lengths, rounds=64)
    hash = dense_hash(nums)
    return hexlify(bytes(hash)).decode('utf-8')


print('Part 1:', part1())
print('Part 2:', part2())
