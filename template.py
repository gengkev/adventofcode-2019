#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import aocd

is_sample = False
DAY = # TODO: change me
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
    #return line.split()
    #return parse_ints(line)
    #return line
    #return int(line)


def main(A):
    A = A.splitlines()
    A = [parse_line(line) for line in A]

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


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1].startswith('s'):
        A = open('sample.txt').read()
        is_sample = True
    else:
        puzzle = aocd.models.Puzzle(day=DAY, year=YEAR)
        A = puzzle.input_data
    main(A)
