#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import aocd

is_sample = False
DAY = 3
YEAR = 2019

def submit_1(res):
    print('Part 1', res)
    if not is_sample and not input("skip? "):
        puzzle.answer_a = res


def submit_2(res):
    print('Part 2', res)
    if not is_sample and not input("skip? "):
        puzzle.answer_b = res


def parse_ints(text):
    "All the integers anywhere in text."
    return [int(x) for x in re.findall(r'[-+]?\d+', text)]


def parse_line(line):
    return [(token[0], int(token[1:])) for token in line.split(',')]


DIRMAP = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}
def add_points(a, b):
    return (a[0]+b[0], a[1]+b[1])

def main(A):
    A = A.splitlines()
    A = [parse_line(line) for line in A]
    A, B = A[0], A[1]

    # Solve part 1
    def part1():
        m = {}

        # do first wire
        cur_pos = (0, 0)
        m[cur_pos] = 1

        for instr in A:
            direction, steps = instr
            for _ in range(steps):
                cur_pos = add_points(cur_pos, DIRMAP[direction])
                m[cur_pos] = 1

        # do second wire
        cur_pos = (0, 0)
        intersects = set()

        for instr in B:
            direction, steps = instr
            for _ in range(steps):
                cur_pos = add_points(cur_pos, DIRMAP[direction])
                if cur_pos in m:
                    intersects.add(cur_pos)

        # sort by manhattan
        intersects = sorted(intersects, key=lambda p: abs(p[0]) + abs(p[1]))
        #print('intersects', intersects)

        closest = intersects[0]
        return abs(closest[0]) + abs(closest[1])

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        m = {}

        # do first wire
        cur_pos = (0, 0)
        m[cur_pos] = 1

        num_steps = 0
        for instr in A:
            direction, steps = instr
            for _ in range(steps):
                cur_pos = add_points(cur_pos, DIRMAP[direction])
                num_steps += 1
                m[cur_pos] = num_steps

        # do second wire
        cur_pos = (0, 0)
        intersects = set()

        num_steps = 0
        for instr in B:
            direction, steps = instr
            for _ in range(steps):
                cur_pos = add_points(cur_pos, DIRMAP[direction])
                num_steps += 1
                if cur_pos in m:
                    intersects.add((m[cur_pos] + num_steps, cur_pos))

        # sort by manhattan
        intersects = sorted(intersects)
        #print('intersects', intersects)

        closest = intersects[0]
        return closest[0]

    res = part2()
    submit_2(res)


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1].startswith('s'):
        A = open('sample.txt').read()
        is_sample = True
    else:
        puzzle = aocd.models.Puzzle(day=DAY, year=YEAR)
        A = puzzle.input_data
    main(A)
