#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 20
YEAR = 2019


##########################################################################


ALL_DIRS = [(0,1),(0,-1),(1,0),(-1,0)]

def main(A):
    N = len(A)
    M = len(A[0])

    def add_pts(a, b):
        return (a[0]+b[0], a[1]+b[1])

    def in_range(p):
        return (0 <= p[0] < N) and (0 <= p[1] < M)

    def get_nbrs(p):
        out = []
        for d in dirs:
            nbr = add_pts(p, d)
            if in_range(nbr):
                out.append(nbr)
        return out

    def get(p):
        return A[p[0]][p[1]]

    def get_adj_tag(p):
        assert get(p) == '.'
        for d in ALL_DIRS:
            nbr = add_pts(p, d)
            if get(nbr).isalpha():
                nbr2 = add_pts(nbr, d)
                assert in_range(nbr2)
                assert get(nbr2).isalpha()

                # get letters in right order
                arr = [get(nbr), get(nbr2)]
                if d in [(0,-1),(-1,0)]:
                    arr = arr[::-1]

                # if we can take another step, this is inner
                is_inner = (in_range(add_pts(nbr2, d)))

                return (''.join(arr), is_inner)
        return (None, None)

    # Build up tag maps...
    tag_map = {}
    tag_rev = defaultdict(list)
    inner_rev = {}
    outer_rev = {}
    for p in product(range(N), range(M)):
        if get(p) != '.':
            continue
        tag, is_inner = get_adj_tag(p)
        if tag is not None:
            print('found tag', p, tag, is_inner)
            tag_map[p] = tag
            tag_rev[tag].append(p)
            if is_inner:
                assert tag not in inner_rev
                inner_rev[tag] = p
            else:
                assert tag not in outer_rev
                outer_rev[tag] = p

    # Sanity check (2 is for AA, ZZ)
    assert len(inner_rev) == len(outer_rev) - 2

    # Solve part 1
    def part1():
        # Build nbr_map
        nbr_map = defaultdict(list)
        for p in product(range(N), range(M)):
            if get(p) != '.':
                continue
            for d in ALL_DIRS:
                nbr = add_pts(p, d)
                if in_range(nbr) and get(nbr) == '.':
                    nbr_map[p].append(nbr)
            if p in tag_map:
                tag = tag_map[p]
                if len(tag_rev[tag]) > 1:
                    nbr_map[p] += [nbr for nbr in tag_rev[tag] if nbr != p]

        # Perform BFS
        start = tag_rev['AA'][0]
        end = tag_rev['ZZ'][0]

        dist = {}
        queue = deque()

        dist[start] = 0
        queue.append(start)

        while queue:
            cur = queue.popleft()
            for nbr in nbr_map[cur]:
                assert get(nbr) == '.'
                if nbr not in dist:
                    dist[nbr] = dist[cur]+1
                    queue.append(nbr)

        return dist[end]

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        # Build nbr_map
        # Second argument indicates level diff!!
        nbr_map = defaultdict(list)
        for p in product(range(N), range(M)):
            if get(p) != '.':
                continue
            for d in ALL_DIRS:
                nbr = add_pts(p, d)
                if in_range(nbr) and get(nbr) == '.':
                    nbr_map[p].append((nbr, 0))

            if p in tag_map:
                tag = tag_map[p]
                if outer_rev[tag] == p:
                    # this is outer
                    if tag not in ['AA', 'ZZ']:
                        nbr = inner_rev[tag]
                        nbr_map[p].append((nbr, -1))
                elif inner_rev[tag] == p:
                    # this is inner
                    nbr = outer_rev[tag]
                    nbr_map[p].append((nbr, 1))
                else:
                    assert False

        # Perform BFS
        start = (outer_rev['AA'], 0)
        end = (outer_rev['ZZ'], 0)

        dist = {}
        prev = {}
        queue = deque()

        dist[start] = 0
        queue.append(start)

        done = False
        while queue and not done:
            cur = queue.popleft()
            for nbr in nbr_map[cur[0]]:
                # add level values
                nbr = (nbr[0], cur[1]+nbr[1])
                # new level cant be negative
                if nbr[1] < 0:
                    continue
                assert get(nbr[0]) == '.'
                if nbr not in dist:
                    dist[nbr] = dist[cur]+1
                    prev[nbr] = cur
                    queue.append(nbr)
                    if nbr == end:
                        done = True

        '''
        print('printing path')
        c = end
        while c in prev:
            c = prev[c]
            print(c)
        '''

        return dist[end]

    res = part2()
    submit_2(res)


##########################################################################


def parse_line(line):
    return line


def parse_input(A):
    A = A.strip('\n')
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
