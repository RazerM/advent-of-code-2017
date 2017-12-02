checksum = 0

with open('../input/2.txt') as fp:
    for line in fp:
        row = [int(x) for x in line.split()]
        checksum += max(row) - min(row)

print(checksum)
