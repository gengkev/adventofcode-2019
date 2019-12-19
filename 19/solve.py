#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 19
YEAR = 2019


##########################################################################

relative_base = 0

def get_value(A, pos, param):
    global relative_base
    val = A[pos]
    param_modes = val // 100

    param_mode = (param_modes // 10**param) % 10
    idx = pos + 1 + param

    # position mode
    if param_mode == 0:
        return A[idx]

    # immediate mode
    elif param_mode == 1:
        return idx

    # relative mode
    elif param_mode == 2:
        return A[idx] + relative_base

    else:
        assert False


def do_op(A, pos, do_input, do_output):
    global relative_base
    val = A[pos]
    op = val % 100
    #print('do_op: pos = {}, val = {}'.format(pos, val))

    if op == 1:
        x, y, z = [
            get_value(A, pos, i)
            for i in range(3)
        ]
        A[z] = A[x] + A[y]
        return pos + 4

    elif op == 2:
        x, y, z = [
            get_value(A, pos, i)
            for i in range(3)
        ]
        A[z] = A[x] * A[y]
        return pos + 4

    elif op == 3:
        x = get_value(A, pos, 0)
        A[x] = do_input()
        return pos + 2

    elif op == 4:
        x = get_value(A, pos, 0)
        do_output(A[x])
        return pos + 2

    elif op == 5:
        x, y = get_value(A, pos, 0), get_value(A, pos, 1)
        if A[x] != 0:
            return A[y]
        return pos + 3

    elif op == 6:
        x, y = get_value(A, pos, 0), get_value(A, pos, 1)
        if A[x] == 0:
            return A[y]
        return pos + 3

    elif op == 7:
        x, y, z = [
            get_value(A, pos, i)
            for i in range(3)
        ]
        A[z] = int(A[x] < A[y])
        return pos + 4

    elif op == 8:
        x, y, z = [
            get_value(A, pos, i)
            for i in range(3)
        ]
        A[z] = int(A[x] == A[y])
        return pos + 4

    elif op == 9:
        x = get_value(A, pos, 0)
        relative_base += A[x]
        #print('relative_base is now', relative_base)
        return pos + 2

    elif op == 99:
        return -1

    print('idk this op', op, pos, A)
    assert False



def main(A):

    def test_coords(p):
        B = defaultdict(int)
        B.update(enumerate(A))
        inp = list(p)
        idx = 0
        def do_input():
            nonlocal idx
            idx += 1
            return inp[idx-1]

        out = None
        def do_output(x):
            nonlocal out
            out = x

        pos = 0
        while pos >= 0:
            pos = do_op(B, pos, do_input, do_output)
        return out

    # Solve part 1
    def part1():

        cnt = 0
        grid = [['.' for _ in range(50)] for _ in range(50)]
        for i in range(50):
            for j in range(50):
                res = test_coords((i, j))
                if res:
                    grid[i][j] = '#'
                    cnt += 1

        print('grid:')
        print('\n'.join(''.join(row) for row in grid))
        return cnt

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():

        in_beam = defaultdict(list)
        in_beam_vert = defaultdict(list)
        for i in range(10):
            for j in range(15):
                if test_coords((i, j)):
                    in_beam[i].append(j)
                    in_beam_vert[j].append(i)

        row = 9
        while True:
            row += 1
            start_col = in_beam[row-1][0]
            seen_in_beam = False

            col = start_col
            while True:
                res = test_coords((row, col))
                if res:
                    seen_in_beam = True
                    in_beam[row].append(col)
                    in_beam_vert[col].append(row)
                if not res and seen_in_beam:
                    break
                col += 1

            #print('row', row, 'len', len(in_beam[row]))
            if len(in_beam[row]) >= 100:
                first_col = in_beam[row][0]
                right_col = first_col + 99
                if len(in_beam_vert[right_col]) >= 100:
                    print('bottom right:', row, right_col)
                    print('top left:', row-99, first_col)
                    return (row-99)*10000 + first_col

    # Alternate solution that is probably a lot faster
    def part2_alt():

        # Find first in-beam for each of first 10 rows
        first_in_row = dict()
        for i in range(10):
            for j in range(15):
                if test_coords((i, j)):
                    first_in_row[i] = j
                    break

        # Extend the first_in_row further
        row = 9
        while True:
            row += 1
            start_col = first_in_row[row-1]

            # Move col right until in beam
            col = start_col
            while not test_coords((row, col)):
                col += 1
            first_in_row[row] = col

            # (row, col) is bottom left corner, which works
            # Check bottom-right and top-right corners
            br_row, br_col = row, col + 99
            tr_row, tr_col = row - 99, col + 99
            if br_row >= 100 and br_col >= 100 and tr_row >= 100 and tr_col >= 100:
                if test_coords((br_row, br_col)) and test_coords((tr_row, tr_col)):
                    # Output top left corner
                    tl_row, tl_col = row - 99, col
                    print('bottom right:', br_row, br_col)
                    print('top left:', tl_row, tl_col)
                    return (tl_row)*10000 + tl_col

    #res = part2()
    res = part2_alt()
    submit_2(res)


##########################################################################


def parse_token(x):
    x = int(x)
    return x


def parse_line(line):
    line = line.split(',')
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    line = [parse_token(x) for x in line]

    return line


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = [parse_line(line) for line in A]

    # One line per input
    A = A[0]

    return A


##########################################################################


def submit_1(res):
    print('Part 1', res)
    if not is_sample and not input("skip? "):
        puzzle.answer_a = res


def submit_2(res):
    print('Part 2', res)
    if not is_sample and not input("skip? "):
        puzzle.answer_b = res


##########################################################################


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1].startswith('s'):
        A = open('sample.txt').read()
        is_sample = True
    else:
        puzzle = aocd.models.Puzzle(day=DAY, year=YEAR)
        A = puzzle.input_data
    main(parse_input(A))
