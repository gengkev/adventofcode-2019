#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import aocd

is_sample = False
DAY = 4
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
    return line
    #return int(line)

def check_1(s):
    for i in range(6-1):
        if s[i] == s[i+1]:
            return True
    return False

def check_2(s):
    for i in range(6-1):
        if s[i] > s[i+1]:
            return False
    return True

def check_3(s):
    match_run = 0
    for i in range(6-1):
        if s[i] == s[i+1]:
            match_run += 1
        else:
            if match_run == 1:
                return True
            match_run = 0
    if match_run == 1:
        return True
    return False

assert check_3('112233')
assert not check_3('123444')
assert check_3('111122')

def main(A):
    A = A.splitlines()
    A = [parse_line(line) for line in A]
    A = A[0].split('-')
    A = list(map(int, A))
    start, end = A
    print(start, end)

    # Solve part 1
    def part1():
        cnt = 0
        for t in range(start, end+1):
            s = str(t)
            a = check_1(s)
            b = check_2(s)
            #print(s, a, b)
            if a and b:
                cnt += 1
        return cnt

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        cnt = 0
        for t in range(start, end+1):
            s = str(t)
            a = check_3(s)
            b = check_2(s)
            #print(s, a, b)
            if a and b:
                cnt += 1
        return cnt

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
