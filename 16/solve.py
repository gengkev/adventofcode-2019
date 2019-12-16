#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

flatten = itertools.chain.from_iterable


is_sample = False
DAY = 16
YEAR = 2019


##########################################################################


BASE_PATTERN = [0, 1, 0, -1]

def calc_output(A, out_pos, start_at=0):
    out = 0
    for i in range(start_at, len(A)):
        x = A[i]
        out += x * BASE_PATTERN[((i+1)//(out_pos+1)) % 4]
    return abs(out)%10

def main(A):
    # Solve part 1
    def part1():
        B = A[:]
        for i in range(100):
            B = [calc_output(B, j) for j in range(len(B))]
        return ''.join(map(str, B[:8]))

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        msg_offset = int(''.join(map(str, A[:7])))
        print('msg_offset', msg_offset)

        B = A[:] * 10000

        # crucial to the trick :/
        assert msg_offset > len(B) // 2

        # temp array to swap with B
        C = [0 for _ in range(len(B))]

        for i in range(100):
            #print('i', i, B[-16:])
            acc = 0
            for j in reversed(range(msg_offset, len(B))):
                acc = abs(acc + B[j]) % 10
                C[j] = acc
            B, C = C, B

        res = B[msg_offset:msg_offset+8]
        print('res', res)
        return int(''.join(map(str, res)))

        '''
        cache = {}
        def get_val(t, offset):
            if (t, offset) in cache:
                return cache[(t, offset)]

            if t == 0:
                return B[offset]

            out = 0
            for j in range(offset+1, len(B)):
                if ((j+1)//(offset+1)) % 2 == 0:
                    continue
                k = BASE_PATTERN[((j+1)//(offset+1)) % 4]
                assert k != 0
                out += k * get_val(t-1, j)

            out = abs(out)%10
            cache[(t, offset)] = out
            return out

        res = []
        for i in range(msg_offset, msg_offset+8):
            print('i', i)
            res.append(get_val(99, i))
        print(res)
        print(''.join(map(str, res)))
        '''


        '''
        required = [set() for _ in range(100)]
        for i in range(8):
            required[99].add(msg_offset + i)

        for i in reversed(range(1, 100)):
            print('loop iteration', i, required[i])
            assert required[i]
            for r in required[i]:
                for j in range(len(B)):
                    if ((j+1)//(r+1)) % 2 == 0:
                        continue
                    k = BASE_PATTERN[((j+1)//(r+1)) % 4]
                    assert k != 0
                    required[i-1].add(j)

        print('required[0]', len(required[0]))
        '''

        '''
        for i in range(100):
            print('iter', i)
            B = [
                (calc_output(B, j, msg_offset+i) if j >= msg_offset+i else 0)
                for j in range(len(B))
            ]
        return ''.join(map(str, B[msg_offset:msg_offset+8]))
        '''

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    x = int(x)
    return x


def parse_line(line):
    #line = line.split()
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
