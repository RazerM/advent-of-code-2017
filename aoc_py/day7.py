from collections import Counter

import attr
import regex

with open('../input/7.txt') as fp:
    relationships = [l.strip() for l in fp]

d = dict()

re_tree = regex.compile(
    r'''
        (?P<name>\w+)
        \s*
        \(                   # weight is in brackets
            (?P<weight>\d+)
        \)
        (?:
            \s*
            ->
            \s*
            (?P<above>       # First item in above group
                \w+                    
            )
            (?:
                ,\s*         # Each item after first preceded by a comma
                (?P<above>
                    \w+                    
                )
            )*
        )?                   # Optional, some programs have nothing above them
    ''',
    flags=regex.VERBOSE)


@attr.s
class Node:
    name = attr.ib()
    weight = attr.ib(default=None)
    # I started with parent and decided to leave it so I didn't have to
    # find root a different way, so leave both here for laziness.
    parent = attr.ib(default=None)
    children = attr.ib(default=attr.Factory(list))


nodes = dict()


def make_node(nodes, name, weight=None, children=None):
    node = nodes.get(name)
    if node is None:
        node = nodes[name] = Node(name=name)

    if children is not None:
        node.children = children

    if weight is not None:
        node.weight = weight

    return node


for rel in relationships:
    m = re_tree.match(rel)
    name = m.group('name')
    weight = int(m.group('weight'))
    children = m.captures('above')

    make_node(nodes, name=name, weight=weight, children=children)

    for child in children:
        child_node = make_node(nodes, name=child)
        child_node.parent = name


root, = [node for node in nodes.values() if node.parent is None]
print('root node =', root.name)


def different(iterable):
    c = Counter(iterable)
    most_common = c.most_common()

    if len(most_common) > 2:
        raise ValueError('More than one different item')
    elif len(most_common) == 2:
        return most_common[0][0], most_common[1][0]

    return most_common[0][0], None


def traverse(nodes, name):
    node = nodes[name]

    if not node.children:
        return node.weight

    sums = [traverse(nodes, child) for child in node.children]
    common, wrong = different(sums)

    difference = 0 if wrong is None else common - wrong

    if abs(difference) > 0:
        wrong_name = node.children[sums.index(wrong)]
        print(f'Changing {wrong_name} to {nodes[wrong_name].weight + difference}')

    return node.weight + difference + sum(sums)


traverse(nodes, root.name)
