checksum = 0

with open('../input/2.txt') as fp:
    for line in fp:
        it = iter((int(x) for x in line.split()))
        n_min = n_max = next(it)

        for n in it:
            n_min = min([n, n_min])
            n_max = max([n, n_max])
        checksum += n_max - n_min

print(checksum)
