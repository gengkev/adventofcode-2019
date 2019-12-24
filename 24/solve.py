#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 24
YEAR = 2019


##########################################################################

def in_bounds(p):
    return 0 <= p[0] < N and 0 <= p[1] < M

def add_pts(a, b):
    return (a[0]+b[0], a[1]+b[1])

def get_nbr_pts(p):
    DIRS = [(0,-1),(0,1),(-1,0),(1,0)]
    out = []
    for d in DIRS:
        nbr = add_pts(p, d)
        if in_bounds(nbr):
            out.append(nbr)
    return out


def main(A):
    global N, M
    N = len(A)
    M = len(A[0])

    def get(grid, p):
        assert in_bounds(p), '{} {} {}'.format(p, N, M)
        return grid[p[0]][p[1]]

    def get_biodiversity(grid):
        out = 0
        for i in range(N):
            for j in range(M):
                pos = i*M + j
                if get(grid, (i,j)) == '#':
                    out += 2**pos
        return out

    def resolve_pt(grid, p):
        bug_cnt = sum(
            1 if get(grid, nbr) == '#' else 0
            for nbr in get_nbrs(p))

        if get(grid, p) == '#':
            if bug_cnt == 1:
                return '#'
            else:
                return '.'
        else:
            if bug_cnt in (1, 2):
                return '#'
            else:
                return '.'

    get_nbrs = get_nbr_pts

    # Solve part 1
    def part1():
        grid = tuple(A[:])
        prev_layouts = set([grid])
        while True:
            grid = tuple(
                    ''.join(resolve_pt(grid, (i, j)) for j in range(M))
                    for i in range(N))
            if grid in prev_layouts:
                return get_biodiversity(grid)
            prev_layouts.add(grid)


    res = part1()
    submit_1(res)


    def get(grid, p):
        assert in_bounds(p[1]), '{} {} {}'.format(p, N, M)
        return grid[p]

    def get_nbrs(p):
        plev, ppos = p
        out = [
            (plev, nbrpos) for nbrpos in get_nbr_pts(ppos)
            if nbrpos != (2, 2)
        ]

        if ppos[0] == 0:
            out.append((plev-1, (1, 2)))
        if ppos[0] == 4:
            out.append((plev-1, (3, 2)))
        if ppos[1] == 0:
            out.append((plev-1, (2, 1)))
        if ppos[1] == 4:
            out.append((plev-1, (2, 3)))

        if ppos == (1, 2):
            for j in range(5):
                out.append((plev+1, (0, j)))
        if ppos == (3, 2):
            for j in range(5):
                out.append((plev+1, (4, j)))
        if ppos == (2, 1):
            for i in range(5):
                out.append((plev+1, (i, 0)))
        if ppos == (2, 3):
            for i in range(5):
                out.append((plev+1, (i, 4)))

        assert len(out) in (4, 8), '{} {} {}'.format(len(out), p, out)
        return out

    # Solve part 2
    def part2():
        grid = defaultdict(lambda: '.', [
            ((0, (i, j)), '#')
            for i, j in product(range(N), range(M))
            if A[i][j] == '#'
        ])

        ITERS = 10 if is_sample else 200
        for _ in range(ITERS):
            all_nbrs = set()
            for p in grid:
                all_nbrs |= set(get_nbrs(p))

            grid = defaultdict(lambda: '.', [
                (p, '#')
                for p in all_nbrs
                if resolve_pt(grid, p) == '#'
            ])

        return len(grid)


    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    line = line.split()
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    line = [parse_token(x) for x in line]

    # One token per line
    line = line[0]

    return line


def parse_input(A):
    A = A.strip()
    A = A.splitlines()
    A = [parse_line(line) for line in A]

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
