#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import aocd


is_sample = False
DAY = 5
YEAR = 2019


##########################################################################

def get_value(A, pos, param):
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

    else:
        assert False

def do_op(A, pos, do_input, do_output):
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

    elif op == 99:
        return -1

    print('idk this op', op, pos, A)
    assert False


def main(A):

    # Solve part 1
    def part1():
        B = A[:]
        all_outputs = []

        def do_input():
            return 1

        def do_output(x):
            #print('output', x)
            all_outputs.append(x)

        pos = 0
        while pos >= 0:
            pos = do_op(B, pos, do_input, do_output)

        #print('final B', B)
        print('all_outputs', all_outputs)
        assert all(x == 0 for x in all_outputs[:-1])
        return all_outputs[-1]

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        B = A[:]
        all_outputs = []

        def do_input():
            return 5

        def do_output(x):
            #print('output', x)
            all_outputs.append(x)

        pos = 0
        while pos >= 0:
            pos = do_op(B, pos, do_input, do_output)

        #print('final B', B)
        print('all_outputs', all_outputs)
        assert len(all_outputs) == 1
        return all_outputs[-1]

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    x = int(x)
    return x


def parse_line(line):
    # One token per line
    #line = parse_token(line)

    # Multiple tokens per line
    line = line.split(',')
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    line = [parse_token(x) for x in line]

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
