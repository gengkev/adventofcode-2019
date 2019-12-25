#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd


def subsets(s):
    for cardinality in range(len(s) + 1):
        yield from combinations(s, cardinality)


is_sample = False
DAY = 25
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


class Intcode:
    def __init__(self, A, get_input):
        self.state = defaultdict(int)
        self.state.update(enumerate(A))
        self.state['relative_base'] = 0

        self.pos = 0
        self.partial_in = []
        self.partial_out = []
        self.get_input = get_input

    def do_input(self):
        while not self.partial_in:
            self.partial_in += self.get_input()
        return self.partial_in.pop(0)

    def do_output(self, out):
        self.partial_out.append(out)

    def is_done(self):
        return self.pos < 0

    def step(self):
        if self.is_done():
            return
        self.pos = do_op(self.state, self.pos, self.do_input, self.do_output)


##########################################################################


def main(A):

    # Solve part 1
    def part1():
        '''
        def get_input():
            print()
            s = input('REQUEST FOR INPUT> ').strip() + '\n'
            return list(map(ord, s))

        x = Intcode(A, get_input)
        while not x.is_done():
            x.step()
            if x.partial_out:
                print(''.join(map(chr, x.partial_out)), end='')
                x.partial_out.clear()
        '''

        ITEMS = [
            'mutex',
            'ornament',
            'astrolabe',
            'semiconductor',
            'dehydrated water',
            'shell',
            'sand',
            'klein bottle',
        ]

        MOVES = [
            'east',
            'take klein bottle',

            'east',
            'take semiconductor',

            'west', 'north', 'north', 'north',
            'take dehydrated water',

            'south', 'south', 'south', 'west', 'north',
            'take sand',

            'north', 'north',
            'take astrolabe',

            'south', 'south', 'west', 'west',
            'take mutex',

            'east', 'east', 'south', 'west', 'north',
            'take shell',

            'south', 'south', 'west',
            'take ornament',

            'west', 'south',
            'inv',
        ]

        MOVES += [
            'drop {}'.format(item)
            for item in ITEMS
        ]

        subset_iter = subsets(ITEMS)
        done = False

        def get_input():
            nonlocal done
            if done:
                s = input('REQUEST FOR INPUT> ').strip() + '\n'
                return list(map(ord, s))

            print()
            try:
                items = next(subset_iter)
            except StopIteration:
                print('ITERATION IS OVER')
                done = True
                return []

            print('trying to go with', items)
            out = []
            for item in items:
                out.append('take {}'.format(item))
            out.append('south')
            for item in items:
                out.append('drop {}'.format(item))
            s = '\n'.join(out) + '\n'
            print('sending in string')
            print(s)
            return list(map(ord, s))


        x = Intcode(A, get_input)
        x.partial_in += list(map(ord, '\n'.join(MOVES) + '\n'))
        total_out = []
        while not x.is_done():
            x.step()
            if x.partial_out:
                total_out += map(chr, x.partial_out)
                print(''.join(map(chr, x.partial_out)), end='')
                x.partial_out.clear()

        total_out_s = ''.join(total_out)
        return re.search(r'typing (\d+)', total_out_s).group(1)

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        pass

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
