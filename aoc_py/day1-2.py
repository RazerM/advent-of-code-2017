with open('../input/1.txt') as fp:
    data = [int(x) for x in fp.read().strip()]

step = len(data) // 2
total = 0

for i, v in enumerate(data):
    n = i + step
    if n >= len(data):
        n -= len(data)

    if v == data[n]:
        total += v

print(total)
