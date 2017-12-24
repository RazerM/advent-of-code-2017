from operator import itemgetter

with open('../input/6.txt') as fp:
    banks = [int(x) for x in fp.read().strip().split()]
    print(banks)


seen = {tuple(banks)}
cycles = 0

while True:
    start, highest = max(enumerate(banks), key=itemgetter(1))
    cycles += 1
    banks[start] = 0
    start += 1

    for i in range(highest):
        banks[(start + i) % len(banks)] += 1
        highest -= 1

    frozen = tuple(banks)
    if frozen in seen:
        break

    seen.add(frozen)

print(cycles)
