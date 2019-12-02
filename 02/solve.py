#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import aocd

is_sample = False
DAY = 2
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
    return parse_ints(line)


def main(A):
    A = A.splitlines()
    A = [parse_line(line) for line in A]
    A = A[0]
    initial_A = A[:]
    print('initial_A', initial_A)

    def do_op(pos):
        op = A[pos]
        if op == 1:
            x, y, z = A[pos+1], A[pos+2], A[pos+3]
            A[z] = A[x] + A[y]
            return False
        elif op == 2:
            x, y, z = A[pos+1], A[pos+2], A[pos+3]
            A[z] = A[x] * A[y]
            return False
        elif op == 99:
            return True
        print('idk this op', op, pos, A)
        assert False

    # Solve part 1
    def part1():
        if not is_sample:
            A[1] = 12
            A[2] = 2
        pos = 0
        while not do_op(pos):
            pos += 4
        return A[0]

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        nonlocal A  # WHY
        for i in range(0, 100):
            for j in range(0, 100):
                A = initial_A[:]
                A[1] = i
                A[2] = j
                pos = 0
                while not do_op(pos):
                    pos += 4
                if A[0] == 19690720:
                    return 100 * i + j
        assert False

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
