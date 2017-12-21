import numpy as np
from boltons.iterutils import chunked_iter


def string_to_grid(square):
    return tuple(tuple(row) for row in square.split('/'))


def grid_to_string(square):
    return '/'.join(''.join(row) for row in square)


def as_tuple_grid(square):
    return tuple(tuple(r) for r in square)


def grid_permutations(square):
    yield square
    yield as_tuple_grid(np.flipud(square).tolist())
    for i in range(1, 4):
        square = np.rot90(square, k=i)
        yield as_tuple_grid(square.tolist())
        yield as_tuple_grid(np.flipud(square).tolist())


def enhance(pattern, rules, n):
    size = len(pattern)

    # square_rows becomes a list of lists of grids
    square_rows = []
    # split pattern into rows
    for rows in chunked_iter(pattern, n):
        squares = [[] for _ in range(size // n)]

        for row in rows:
            # split rows into columns, appending each row to the correct square
            # in the list we created above
            for i, c in enumerate(chunked_iter(row, n)):
                squares[i].append(c)

        square_rows.append(squares)

    # now enhance each square that we created above
    for y, squares in enumerate(square_rows):
        for x, square in enumerate(as_tuple_grid(s) for s in squares):
            square_rows[y][x] = rules[square]

    # convert square_rows back into a normal grid
    out = []

    for squares in square_rows:
        rows = ['' for _ in range(len(squares[0]))]
        for square in squares:
            for i, row in enumerate(square):
                rows[i] += ''.join(row)

        out.extend(tuple(r) for r in rows)

    return tuple(out)


def load_rules():
    rules = dict()

    with open('../input/21.txt') as fp:
        for line in fp:
            input_, output = line.strip().split(' => ')
            rules[string_to_grid(input_)] = string_to_grid(output)

    for rule, output in list(rules.items()):
        for grid in grid_permutations(rule):
            rules[grid] = output

    return rules


def main():
    pattern = string_to_grid('.#./..#/###')
    rules = load_rules()

    for i in range(18):
        size = len(pattern)

        if size % 2 == 0:
            pattern = enhance(pattern, rules, 2)
        elif size % 3 == 0:
            pattern = enhance(pattern, rules, 3)

        if i == 4:
            print('Part 1:', grid_to_string(pattern).count('#'))
        elif i == 17:
            print('Part 2:', grid_to_string(pattern).count('#'))


if __name__ == '__main__':
    main()
