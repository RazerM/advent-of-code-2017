from itertools import product

checksum = 0

with open('../input/2.txt') as fp:
    for line in fp:
        row = [int(x) for x in line.split()]

        for x, y in product(row, row):
            quot, rem = divmod(x, y)
            if x != y and rem == 0:
                checksum += quot

print(checksum)
