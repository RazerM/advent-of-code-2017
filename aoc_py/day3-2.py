from collections import defaultdict

import attr

@attr.s(cmp=True, frozen=True)
class Vector:
    x = attr.ib()
    y = attr.ib()

    def go(self, direction):
        return Vector(self.x + direction.x, self.y + direction.y)

assert hash(Vector(1, 3)) == hash((1, 3))

target = 325489

n = 1
side = 1

position = Vector(0, 0)
direction = Vector(1, 0)

memory = defaultdict(int)
memory[position] = n


def get_adjacent_sum(mem, pos):
    return sum(
        mem[Vector(x, y)]
        for x in range(pos.x - 1, pos.x + 2)
        for y in range(pos.y - 1, pos.y + 2)
    )


while n < target:
    for _ in range(2):
        for _ in range(side):
            position = position.go(direction)

            n = get_adjacent_sum(memory, position)

            memory[position] = n

            if n > target:
                print(f'x={position.x}, y={position.y}, n={n}')
                break

        if n > target:
            break

        # Watch out for time beetles
        direction = Vector(-direction.y, direction.x)

    side += 1
