with open('../input/5.txt') as fp:
    instructions = [int(x) for x in fp.readlines()]


pos = 0
steps = 0

while 0 <= pos < len(instructions):
    jump = instructions[pos]
    instructions[pos] += 1
    pos += jump
    steps += 1

print(steps)
