#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
from math import gcd, atan2
import math
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 10
YEAR = 2019


##########################################################################

def add_pts(a, b):
    return (a[0]+b[0], a[1]+b[1])

def sub_pts(a, b):
    return (a[0]-b[0], a[1]-b[1])

def taxicab(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def compute_line(a, b):
    diff = (b[0]-a[0], b[1]-a[1])
    g = gcd(diff[0], diff[1])
    d = (diff[0]//g, diff[1]//g)

    out = []
    for i in range(1, g):
        p = add_pts(a, (d[0]*i, d[1]*i))
        out.append(p)

    #print('compute_line', a, b, out)
    return out

def main(A):
    height = len(A)
    width = len(A[0])

    asteroids = []

    for i in range(height):
        for j in range(width):
            if A[i][j] == '#':
                asteroids.append((j, i))

    station_loc = None

    # Solve part 1
    def part1():
        nonlocal station_loc

        all_cnts = {}
        for p in asteroids:
            cnt = 0
            for q in asteroids:
                if p == q:
                    continue
                med = compute_line(p, q)
                inter = set(med) & set(asteroids)
                #print('p', p, 'q', q, 'med', med, 'inter', inter)
                if len(inter) == 0:
                    cnt += 1
            #print('got cnt', p, cnt)
            all_cnts[p] = cnt

        cands = sorted(((cnt, p) for p, cnt in all_cnts.items()), reverse=True)
        cands = list(cands)
        print('best', cands[:4])
        best = cands[0]
        station_loc = best[1]
        return best[0]

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        def calc_deg(p):
            offset = sub_pts(p, station_loc)
            assert offset != (0, 0)
            rad = atan2(-offset[1], offset[0])
            deg = rad * 360 / (2 * math.pi)
            deg = -deg + 90
            while deg < 0:
                deg += 360
            return round(deg, 11)

        degs = [p for p in asteroids if p != station_loc]
        degs = [(calc_deg(p), taxicab(p, station_loc), p) for p in degs]
        degs = sorted(degs)

        degs_left = degs[:]
        num_popped = 0
        while degs_left:
            pos = 0
            last_angle = -1.0
            while pos < len(degs_left):
                if math.isclose(last_angle, degs_left[pos][0]):
                    pos += 1
                    continue
                cur = degs_left[pos]
                degs_left.pop(pos)
                print(num_popped, 'popped', cur)

                last_angle = cur[0]
                num_popped += 1
                if num_popped == 200:
                    print('found 200', cur)
                    res = cur[2]
                    return res[0]*100 + res[1]
        assert False

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
