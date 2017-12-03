import attr


@attr.s
class Vector:
    x = attr.ib()
    y = attr.ib()


target = 325489

n = 1
side = 1

position = Vector(0, 0)
direction = Vector(1, 0)

while n < target:
    for _ in range(2):
        for _ in range(side):
            position.x += direction.x
            position.y += direction.y
            n += 1

            if n >= target:
                break

        if n >= target:
            break

        # Watch out for time beetles
        direction.x, direction.y = -direction.y, direction.x

    side += 1

print(abs(position.x) + abs(position.y))
