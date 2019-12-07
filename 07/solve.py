#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
from functools import partial
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 7
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


def simulate_1(A, phase, do_input, do_output):
    A = A[:]

    phase_given = False
    def my_do_input():
        nonlocal phase_given
        if not phase_given:
            phase_given = True
            return phase
        else:
            return do_input()

    pos = 0
    while pos >= 0:
        pos = do_op(A, pos, my_do_input, do_output)


def simulate(A, pos, phase_given, i, phase, do_input, do_output):
    def my_do_input():
        nonlocal phase_given
        if not phase_given[i]:
            phase_given[i] = True
            return phase
        else:
            return do_input()

    return do_op(A, pos, my_do_input, do_output)


def main(A):
    # Solve part 1
    def part1():

        possibilities = []

        for phase_tup in permutations(range(5)):

            outputs = [0 for _ in range(5)]
            def do_input(i):
                if i == 0:
                    #print('i=', i, 'do_input val=0')
                    return 0
                else:
                    #print('i=', i, 'do_input val=', outputs[i-1])
                    return outputs[i-1]
            def do_output(i, val):
                #print('i=', i, 'do_output val=', val)
                outputs[i] = val

            for i in range(5):
                simulate_1(A, phase_tup[i], partial(do_input, i), partial(do_output, i))

            #print('phase_tup', phase_tup, 'outputs', outputs)
            possibilities.append((outputs[-1], phase_tup))

        print('best', max(possibilities))
        return max(possibilities)[0]


    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        possibilities = []

        for phase_tup in permutations(range(5, 10)):
        #for phase_tup in [(9,8,7,6,5)]:
            phase_given = [False for _ in range(5)]
            outputs = [0 for _ in range(5)]
            local_A = [A[:] for _ in range(5)]
            local_pos = [0 for _ in range(5)]
            local_done = [False for _ in range(5)]
            stop_running = False

            def do_input(i):
                return outputs[i-1]

            def do_output(i, val):
                nonlocal stop_running
                outputs[i] = val
                stop_running = True

            while any(not local_done[j] for j in range(5)):
                for i in range(5):
                    stop_running = False
                    while not stop_running and local_pos[i] >= 0:
                        local_pos[i] = simulate(local_A[i], local_pos[i], phase_given, i, phase_tup[i], partial(do_input, i), partial(do_output, i))
                    if local_pos[i] < 0:
                        local_done[i] = True

            #print('phase_tup', phase_tup, 'outputs', outputs)
            possibilities.append((outputs[-1], phase_tup))

        print('best', max(possibilities))
        return max(possibilities)[0]

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
