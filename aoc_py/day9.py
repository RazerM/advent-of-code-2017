import attr
import pytest
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

grammar = '''
    document = group EOF
    group = "{" (content ("," content)*)? "}"
    content = garbage / group
    garbage = "<" garbage_character* ">"
    garbage_character = !(">" / "!") char / "!" cancelled
    cancelled = char
    char = r'.'
'''


@attr.s
class Garbage:
    contents = attr.ib()


@attr.s
class Group:
    children = attr.ib()

    def calculate_score(self, depth=1):
        return depth + sum(
            c.calculate_score(depth + 1)
            for c in self.children
            if isinstance(c, Group)
        )

    def count_garbage(self):
        total = 0
        for child in self.children:
            if isinstance(child, Group):
                total += child.count_garbage()
            elif isinstance(child, Garbage):
                total += len(child.contents)
        return total


class StreamVisitor(PTNodeVisitor):
    def visit_group(self, node, children):
        return Group(children=children)

    def visit_garbage(self, node, children):
        return Garbage(''.join(children))

    def visit_cancelled(self, node, children):
        return None


parser = ParserPEG(grammar, root_rule_name='document', skipws=False)


def parse_stream(characters):
    parse_tree = parser.parse(characters)
    return visit_parse_tree(parse_tree, StreamVisitor())


@pytest.mark.parametrize('stream, score', [
    ('{}', 1),
    ('{{{}}}', 6),
    ('{{},{}}', 5),
    ('{{{},{},{{}}}}', 16),
    ('{<a>,<a>,<a>,<a>}', 1),
    ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
])
def test_score(stream, score):
    group = parse_stream(stream)
    assert group.calculate_score() == score


@pytest.mark.parametrize('stream, count', [
    ('{<>}', 0),
    ('{< >}', 1),
    ('{<random characters>}', 17),
    ('{<<<<>}', 3),
    ('{<{!>}>}', 2),
    ('{<!!>}', 0),
    ('{<!!!>>}', 0),
    ('{<{o"i!a,<{i<a>}', 10),
])
def test_count_garbage(stream, count):
    group = parse_stream(stream)
    print(group)
    assert group.count_garbage() == count


if __name__ == '__main__':
    with open('../input/9.txt') as fp:
        characters = fp.read().strip()

    day9 = parse_stream(characters)
    print('Score:', day9.calculate_score())
    print('Garbage count:', day9.count_garbage())
