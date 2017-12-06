from operator import itemgetter

with open('../input/6.txt') as fp:
    banks = [int(x) for x in fp.read().strip().split()]
    print(banks)


seen = {tuple(banks)}
cycles = 0
target = None

while True:
    start, highest = max(enumerate(banks), key=itemgetter(1))
    cycles += 1
    banks[start] = 0
    start += 1

    for i in range(highest):
        banks[(start + i) % len(banks)] += 1
        highest -= 1

    frozen = tuple(banks)

    if target is None:
        if frozen in seen:
            # We're done tracking seen configurations, now switch to finding
            # the start of this loop.
            target = frozen
            cycles = 0
        seen.add(frozen)
    elif target == frozen:
        break

print(cycles)
