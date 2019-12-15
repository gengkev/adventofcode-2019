#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 15
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

    elif op == 9:
        x = get_value(A, pos, 0)
        relative_base += A[x]
        #print('relative_base is now', relative_base)
        return pos + 2

    elif op == 99:
        return -1

    print('idk this op', op, pos, A)
    assert False


CACHE = {}

def test_step_list(A, step_list):
    pos = 0

    for k in reversed(range(1, len(step_list)-1)):
        t = tuple(step_list[:k])
        if t in CACHE:
            A, pos = CACHE[t]
            step_list = step_list[k:]
            break

    assert len(step_list) > 0
    A = A[:]
    i = 0
    j = 0
    res = None

    def do_input():
        nonlocal i
        i += 1
        return step_list[i-1]

    def do_output(x):
        nonlocal res, j
        if j == len(step_list) - 1:
            res = x
        else:
            assert x == 1 or x == 2, "step_list {}, i is {}, j is {}, actually x is {}".format(step_list, i, j,  x)
        j += 1
        assert i == j

    while pos >= 0 and res is None:
        pos = do_op(A, pos, do_input, do_output)

    if res == 1 and len(step_list) % 3 == 0:
        CACHE[tuple(step_list)] = (A[:], pos)
    #print('test_step_list', step_list, res)
    return res


DIRMAP = {
    1: (0, -1),  # N
    2: (0,  1),  # S
    3: (-1, 0),  # W
    4: ( 1, 0),  # E
}

def add_pts(a, b):
    return (a[0]+b[0], a[1]+b[1])

def main(A):
    oxygen_system = None
    oxygen_system_path = None

    # Solve part 1
    def part1():
        nonlocal oxygen_system, oxygen_system_path

        paths = {(0, 0): []}
        q = deque([(0, 0)])

        while q:
            nxt = q.popleft()
            path = paths[nxt]
            #print('nxt', nxt, path)

            for choix in [1,2,3,4]:
                nbr = add_pts(nxt, DIRMAP[choix])
                if nbr in paths:
                    continue

                r = test_step_list(A, path + [choix])
                if r == 2:
                    print('found')
                    print('oxygen system located at', nbr)
                    oxygen_system = nbr
                    oxygen_system_path = path + [choix]
                    return len(path)+1
                if r == 1:
                    paths[nbr] = path + [choix]
                    q.append(nbr)

        return None


    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():

        paths = {oxygen_system: []}
        q = deque([oxygen_system])

        while q:
            nxt = q.popleft()
            path = paths[nxt]
            #print('nxt', nxt, path)

            for choix in [1,2,3,4]:
                nbr = add_pts(nxt, DIRMAP[choix])
                if nbr in paths:
                    continue

                r = test_step_list(A, oxygen_system_path + path + [choix])
                if r == 1 or r == 2:
                    paths[nbr] = path + [choix]
                    q.append(nbr)

        print('done with queue')
        res = max(len(v) for v in paths.values())
        return res

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
