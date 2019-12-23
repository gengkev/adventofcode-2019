#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 23
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

    # relative mode
    elif param_mode == 2:
        return A[idx] + A['relative_base']

    else:
        assert False


def do_op(A, pos, do_input, do_output):
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
        A['relative_base'] += A[x]
        return pos + 2

    elif op == 99:
        return -1

    print('idk this op', op, pos, A)
    assert False


##########################################################################

class NetworkNode:
    def __init__(self, A, in_queues, i):
        self.in_queues = in_queues
        self.i = i

        self.state = defaultdict(int)
        self.state.update(enumerate(A))
        self.state['relative_base'] = 0

        self.idle = False
        self.pos = 0
        self.partial_in = [i]
        self.partial_out = []

    def do_input(self):
        if self.partial_in:
            self.idle = False
            return self.partial_in.pop(0)
        if self.in_queues[self.i]:
            self.idle = False
            self.partial_in += self.in_queues[self.i].pop(0)
            return self.partial_in.pop(0)
        self.idle = True
        return -1

    def do_output(self, out):
        self.partial_out.append(out)
        assert len(self.partial_out) <= 3
        if len(self.partial_out) == 3:
            dest, x, y = self.partial_out
            self.in_queues[dest].append((x, y))
            self.partial_out = []

    def is_done(self):
        return self.pos < 0

    def step(self):
        if self.is_done():
            return
        self.pos = do_op(self.state, self.pos, self.do_input, self.do_output)


def main(A):

    # Solve part 1
    def part1():
        in_queues = defaultdict(list)
        nodes = [NetworkNode(A, in_queues, i) for i in range(50)]

        while True:
            for i in range(50):
                nodes[i].step()

            if in_queues[255]:
                print(in_queues[255])
                x, y = in_queues[255].pop()
                return y

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        in_queues = defaultdict(list)
        nodes = [NetworkNode(A, in_queues, i) for i in range(50)]

        nat_pkt_y = set()
        while True:
            for i in range(50):
                nodes[i].step()

            if in_queues[255]:
                # Only retain last packet received
                if len(in_queues[255]) > 1:
                    in_queues[255] = [in_queues[255][-1]]

                if all(node.idle for node in nodes):
                    pkt = in_queues[255].pop()
                    in_queues[0].append(pkt)
                    print('nat sending packet to address 0:', pkt)
                    x, y = pkt
                    if y in nat_pkt_y:
                        return y
                    nat_pkt_y.add(y)

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
