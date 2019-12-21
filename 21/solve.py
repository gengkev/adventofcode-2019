#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 21
YEAR = 2019


##########################################################################

relative_base = 0

def get_value(A, pos, param):
    global relative_base
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

    # relative mode
    elif param_mode == 2:
        return A[idx] + relative_base

    else:
        assert False


def do_op(A, pos, do_input, do_output):
    global relative_base
    val = A[pos]
    op = val % 100

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

    elif op == 9:
        x = get_value(A, pos, 0)
        relative_base += A[x]
        return pos + 2

    elif op == 99:
        return -1

    print('idk this op', op, pos, A)
    assert False


##########################################################################


def main(A):

    def run_program(inp):
        B = defaultdict(int)
        B.update(enumerate(A))

        idx = 0
        def do_input():
            nonlocal idx
            idx += 1
            return inp[idx-1]

        out = None
        def do_output(x):
            nonlocal out
            if x >= 128:
                print('GOT RESULT', x)
                out = x
            else:
                print(chr(x), end='')

        pos = 0
        while pos >= 0:
            pos = do_op(B, pos, do_input, do_output)

        return out


    # Solve part 1
    def part1():
        INSTRS = [
            'NOT C J',
            'AND D J',

            'NOT A T',
            'OR T J',

            'WALK',
            '',
        ]

        inp = list(map(ord, '\n'.join(INSTRS)))
        return run_program(inp)

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        '''
        INSTRS = [
            #'NOT C J',
            #'NOT F T',
            #'AND T J',

            #'NOT B T',
            #'OR T J',

            #'NOT E T',
            #'AND T J',

            #'NOT A T',
            #'OR T J',

            #'NOT C T',
            #'AND D T',
            #'OR T J',

            # =========

            # CG
            'NOT C T',
            'NOT T J',
            'AND G J',


            # + F
            #'OR F J',

            # + CF
            'NOT C T',
            'NOT T T',
            'AND F T',
            'OR T J',

            'AND B J',

            # + EI
            'NOT I T',
            'NOT T T',
            'AND E T',
            'OR T J',

            'AND A J',
            'NOT J J',

            'RUN',
            '',
        ]
        '''

        INSTRS = [
            # We should have a reason to jump
            # not(B) + not(C)
            'NOT B T',
            'NOT C J',
            'OR T J',

            # We need to have a valid move after landing at D
            # * (E + H)
            'NOT E T',
            'NOT T T',
            'OR H T',
            'AND T J',

            # Only jump if we will land
            # * D
            'AND D J',

            # We must jump if A isn't present
            # + not(A)
            'NOT A T',
            'OR T J',

            'RUN',
            ''
        ]

        inp = list(map(ord, '\n'.join(INSTRS)))
        return run_program(inp)

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
