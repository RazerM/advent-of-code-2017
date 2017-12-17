import string
from collections import deque
from itertools import takewhile

import attr
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

grammar = '''
    moves = move ("," move)*
    move = spin / exchange / partner
    spin = "s" int
    exchange = "x" int sep int
    partner = "p" program sep program
    program = r'[a-z]+'
    int = digit+
    digit = r'[0-9]'
    sep = "/"
'''

parser = ParserPEG(grammar, root_rule_name='moves', skipws=False)


def get_letters(until):
    # Yes, this is gratuitous
    return takewhile(lambda x: x <= until, string.ascii_lowercase)


@attr.s
class Spin:
    num = attr.ib()

    def apply(self, l):
        l.rotate(self.num)


@attr.s
class Exchange:
    pos1 = attr.ib()
    pos2 = attr.ib()

    def apply(self, l):
        l[self.pos1], l[self.pos2] = l[self.pos2], l[self.pos1]


@attr.s
class Partner:
    prog1 = attr.ib()
    prog2 = attr.ib()

    def apply(self, l):
        pos1 = l.index(self.prog1)
        pos2 = l.index(self.prog2)
        l[pos1], l[pos2] = l[pos2], l[pos1]


class MoveVisitor(PTNodeVisitor):
    def visit_moves(self, node, children):
        return children

    def visit_move(self, node, children):
        move, = children
        return move

    def visit_spin(self, node, children):
        return Spin(*children)

    def visit_exchange(self, node, children):
        return Exchange(*children)

    def visit_partner(self, node, children):
        return Partner(*children)

    def visit_int(self, node, children):
        return int(''.join(children))


def parse_stream(moves):
    parse_tree = parser.parse(moves)
    return visit_parse_tree(parse_tree, MoveVisitor())


def main():
    with open('../input/16.txt') as fp:
        moves = parse_stream(fp.read().strip())

    letters = deque(get_letters(until='p'))

    seen = {''.join(letters)}
    i = 0
    rounds = int(1e9)
    found_cycle = False

    while i < rounds:
        if i == 1:
            print('Part 1:', ''.join(letters))
        for move in moves:
            move.apply(letters)

        if not found_cycle:
            key = ''.join(letters)
            if key in seen:
                found_cycle = True
                new_i = rounds - rounds % (i + 1)

                if new_i > i:
                    i = new_i
                    continue

            seen.add(key)
        i += 1

    print('Part 2:', ''.join(letters))


if __name__ == '__main__':
    main()
