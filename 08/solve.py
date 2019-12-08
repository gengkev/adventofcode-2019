#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 8
YEAR = 2019


##########################################################################

def main(A):
    # Solve part 1
    def part1():
        WIDTH = 25
        HEIGHT = 6
        LEN = WIDTH * HEIGHT

        layers = [A[i:i+LEN] for i in range(0, len(A), LEN)]
        data = [(Counter(layer)['0'], layer) for layer in layers]
        sol = min(data)
        #print('sol', sol)
        c = Counter(sol[1])
        return c['1'] * c['2']

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        def get_result(layers, i):
            for layer in layers:
                if layer[i] == '2':
                    continue
                else:
                    return layer[i]
            return '2'

        WIDTH = 25
        HEIGHT = 6
        LEN = WIDTH * HEIGHT

        layers = [A[i:i+LEN] for i in range(0, len(A), LEN)]
        out = [get_result(layers, i) for i in range(LEN)]
        out = ''.join(out)

        split = [out[i:i+WIDTH] for i in range(0, LEN, WIDTH)]
        print()
        print('\n'.join(split).replace('0', ' '))
        print()
        return input('What does it say? ')

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
