#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import aocd


is_sample = False
DAY = 6
YEAR = 2019


##########################################################################


def main(A):
    total_objs = set()
    for a, b in A:
        total_objs.add(a)
        total_objs.add(b)

    orbits = defaultdict(set)
    for a, b in A:
        # b orbits a
        orbits[b].add(a)

    # Solve part 1
    def part1():
        cnt = 0
        for obj in total_objs:
            everyone = set()
            frontier = set(orbits[obj])
            while frontier:
                everyone |= frontier
                next_frontier = []
                for x in frontier:
                    next_frontier += orbits[x]
                frontier = set(next_frontier)
            cnt += len(everyone)

        return cnt

    res = part1()
    submit_1(res)

    # Solve part 2
    def part2():
        orbit_dists = defaultdict(dict)
        for obj in total_objs:
            frontier = set(orbits[obj])
            iters = 0

            while frontier:
                for x in frontier:
                    if x in orbit_dists[obj]: continue
                    orbit_dists[obj][x] = iters

                iters += 1

                next_frontier = []
                for x in frontier:
                    next_frontier += orbits[x]
                frontier = set(next_frontier)

        candidates = set(orbit_dists['YOU']) & set(orbit_dists['SAN'])
        best_answer = min(
            orbit_dists['YOU'][x] + orbit_dists['SAN'][x]
            for x in candidates)

        print('YOU', orbit_dists['YOU'])
        print('SAN', orbit_dists['SAN'])

        return best_answer

    res = part2()
    submit_2(res)


##########################################################################


def parse_token(x):
    #x = int(x)
    return x


def parse_line(line):
    # One token per line
    #line = parse_token(line)

    # Multiple tokens per line
    line = line.split(')')
    #line = re.findall(r'\d+', line)
    #line = re.findall(r'[-+]?\d+', line)
    #line = [parse_token(x) for x in line]

    return line


def parse_input(A):
    A = A.strip()

    # One line per input
    #A = parse_line(A)

    # Multiple lines per input
    A = A.splitlines()
    A = [parse_line(line) for line in A]

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
