import attr


@attr.s(cmp=True, frozen=True)
class Component:
    a = attr.ib()
    b = attr.ib()

    def compatible(self, n):
        return self.a == n or self.b == n

    def other(self, n):
        assert self.compatible(n)
        if self.a == n:
            return self.b
        elif self.b == n:
            return self.a


def load_components():
    components = []

    with open('../input/24.txt') as fp:
        for line in fp:
            a, b = line.strip().split('/')
            a = int(a)
            b = int(b)
            components.append(Component(a, b))

    return components


def permutations(components, matching):
    """Get all valid permutations of bridges from the components given"""
    items = set(components)
    assert len(items) == len(components), "Does not handle duplicates"

    # Get all components with a port that equals `matching`
    valid = (item for item in items if item.compatible(matching))
    for item in valid:
        sub_items = items - {item}
        target = item.other(matching)

        # Get permutations for each component that can connect to `item`
        for option in permutations(sub_items, target):
            out = [item, *option]
            yield out

        # Include bridges that end at this item
        yield [item]


def main():
    components = load_components()
    all_bridges = permutations(components, matching=0)

    def longest_strongest(b):
        return len(b), sum(b)

    strengths = [[x.a + x.b for x in b] for b in all_bridges]
    strongest = sum(max(strengths, key=sum))
    longest = sum(max(strengths, key=longest_strongest))

    print('Part 1:', strongest)
    print('Part 2:', longest)


if __name__ == '__main__':
    main()
