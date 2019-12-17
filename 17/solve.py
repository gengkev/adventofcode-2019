#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 17
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


def add_pts(a, b):
    return (a[0]+b[0], a[1]+b[1])

DIRMAP = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}

def add_dir(p, d):
    return add_pts(p, DIRMAP[d])

def main(A):
    def make_grid(A):
        B = defaultdict(int)
        B.update(enumerate(A))

        grid = []

        def do_input():
            assert False

        def do_output(x):
            grid.append(x)

        # run program
        pos = 0
        while pos >= 0:
            pos = do_op(B, pos, do_input, do_output)

        grid = ''.join(map(chr, grid))
        return grid

    grid = make_grid(A)
    grid = grid.strip().splitlines()
    print('grid:')
    print('\n'.join(grid))

    height = len(grid)
    width = len(grid[0])

    def in_bounds(p):
        return (0 <= p[0] < height) and (0 <= p[1] < width)

    # Solve part 1
    def part1():

        def num_nbrs(p):
            cnt = 0
            for vec in [(0,1),(0,-1),(1,0),(-1,0)]:
                nbr = add_pts(p, vec)
                if in_bounds(nbr):
                    #print(nbr, len(grid), len(grid[0]))
                    c = grid[nbr[0]][nbr[1]]
                    if c in '#^':
                        cnt += 1
            return cnt

        out = 0
        for i in range(height):
            for j in range(width):
                c = grid[i][j]
                if c in '#^' and num_nbrs((i, j)) > 2:
                    out += i * j

        return out

    res = part1()
    submit_1(res)

    def get_robot_init_pos():
        for i in range(height):
            for j in range(width):
                if grid[i][j] == '^':
                    return (i, j)
    robot_init_pos = get_robot_init_pos()
    print('robot init pos', robot_init_pos)

    # Solve part 2
    def part2():
        # empty grid
        egrid = '\n'.join(grid).replace('^', '#').splitlines()
        instrs = []  # manual inspection
        visited = {robot_init_pos}

        rpos = robot_init_pos
        rdir = 0

        def should_move(npos, is_straight):
            return in_bounds(npos) and (npos not in visited or is_straight) and \
                    grid[npos[0]][npos[1]] == '#'

        while True:
            ndir_list = [
                (x % 4, mv_list)
                for (x, mv_list) in [
                    (rdir, ['1']),
                    (rdir+1, ['R', '1']),
                    (rdir+3, ['L', '1']),
                    (rdir+2, ['B', '1']),
                ]
            ]
            for ndir, mv_list in ndir_list:
                npos = add_dir(rpos, ndir)
                if should_move(npos, ndir == rdir):
                    #print('moving to', ndir, npos, mv_list)
                    instrs += mv_list
                    rpos = npos
                    rdir = ndir
                    visited.add(npos)
                    break
            else:
                print('no more moves to be made')
                break

        # marked grid
        print('marked grid:')
        mgrid = [list(row) for row in egrid[:]]
        for (i, j) in visited:
            mgrid[i][j] = '%'
        print('\n'.join(''.join(row) for row in mgrid))

        assert 'B' not in instrs  # backwards?
        cinstrs = []
        acc = 0
        for x in instrs:
            if x == '1':
                acc += 1
            else:
                if acc > 0:
                    cinstrs.append(str(acc))
                    acc = 0
                if x in 'LR':
                    cinstrs.append(x)
                else:
                    assert False
        if acc > 0:
            cinstrs.append(str(acc))
            acc = 0

        print('final move list', ','.join(cinstrs))

        '''
        (Manually deduced)
        Main routine: A,B,A,C,B,A,C,B,A,C
        Function A:   L,6,L,4,R,12
        Function B:   L,6,R,12,R,12,L,8
        Function C:   L,6,L,10,L,10,L,6
        '''

        input_string = [
            'A,B,A,C,B,A,C,B,A,C',
            'L,6,L,4,R,12',
            'L,6,R,12,R,12,L,8',
            'L,6,L,10,L,10,L,6',
            'n',
            '',
        ]
        assert ','.join(cinstrs) == (input_string[0]
                .replace('A', input_string[1])
                .replace('B', input_string[2])
                .replace('C', input_string[3]))
        input_string = '\n'.join(input_string)

        # run the roomba thing
        print('######## BEGINNING PART 2 PROG OUTPUT #########')
        B = defaultdict(int)
        B.update(enumerate(A))

        # update address
        assert B[0] == 1
        B[0] = 2

        input_pos = 0
        def do_input():
            nonlocal input_pos
            input_pos += 1
            return ord(input_string[input_pos - 1])

        output = []
        def do_output(x):
            nonlocal output
            print(chr(x), end='')
            output.append(x)

        # run program
        pos = 0
        while pos >= 0:
            assert type(B) == defaultdict
            pos = do_op(B, pos, do_input, do_output)

        print('######## ENDING PART 2 PROG OUTPUT #########')
        return output[-1]

    res = part2()
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
