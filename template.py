#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import aocd


is_sample = False
DAY = # TODO: change me
YEAR = 2019


##########################################################################


def main(A):
    # Solve part 1
    def part1():
        return 0

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        return 0

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    # One token per line
    line = parse_token(line)

    # Multiple tokens per line
    #line = line.split()
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    #line = [parse_token(x) for x in line]

    return line


def parse_input(A):
    A = A.strip()

    # One line per input
    A = parse_line(A)

    # Multiple lines per input
    #A = A.splitlines()
    #A = [parse_line(line) for line in A]

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
