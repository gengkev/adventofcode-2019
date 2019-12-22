#!/usr/bin/env python3

import re
import sys
from collections import Counter, defaultdict, deque
from itertools import permutations, combinations, product
import itertools
import aocd

is_sample = False
DAY = 22
YEAR = 2019


############################################################################
# Matrix operations
############################################################################

def mat_identity(N):
    return [[1 if i == j else 0 for j in range(N)] for i in range(N)]


def mat_mult(A, B):
    N = len(A)
    M = len(B[0])

    L = len(A[0])
    assert L == len(B)

    C = [[0 for _ in range(M)] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            acc = sum(A[i][k] * B[k][j] for k in range(L))
            C[i][j] = acc % MOD

    return C


# https://www.hackerearth.com/practice/notes/matrix-exponentiation-1/
def mat_pow(A, exp):
    res = mat_identity(len(A))
    while exp > 0:
        if exp % 2 == 1:
            res = mat_mult(res, A)
        A = mat_mult(A, A)
        exp //= 2
    return res


############################################################################
# COWBASIC functionality
############################################################################

# Parse a COWBASIC program
# Returns a list of instructions, and a list of all variable names
def parse_prog(text):
    prog = []
    varnames = set()

    for lineno, line in enumerate(text.splitlines()):
        if not line:
            continue

        # begin loop
        if 'MOO {' in line:
            n = int(line.rstrip('MOO {').strip())
            prog.append(('loop', n))

        # end loop
        elif '}' in line:
            prog.append(('endloop',))

        # assignment
        elif '=' in line:
            lhs, rhs = line.split('=')
            lhs = lhs.strip()
            rhs = rhs.replace('+', '').replace('(', '').replace(')', '').split()
            prog.append(('assign', lhs, rhs))
            varnames.add(lhs)

        # return
        elif 'RETURN' in line:
            rhs = line.lstrip('RETURN').strip()
            prog.append(('return', rhs))

        else:
            raise ValueError('could not parse line: {}'.format(line))

    return prog, list(sorted(varnames))


# Perform a pairwise sum of two vectors
def sumvec(A, B):
    return [(a + b) % MOD for a, b in zip(A, B)]


# Convert a list of 'assign' or 'mat' commands to a matrix
def seq_to_mat(prog, varnames, varmap):
    N = len(varnames) + 1
    mat = mat_identity(N)

    for cmd in prog:
        # Matrix multiply command (LEFT multiply)
        if cmd[0] == 'mat':
            mat = mat_mult(cmd[1], mat)

        # Assignment command
        elif cmd[0] == 'assign':
            lhs, rhs = cmd[1], cmd[2]
            rvec = [0 for _ in range(N)]

            for name in rhs:
                if name.isnumeric():
                    # Add a constant integer
                    rvec[N-1] += int(name)
                else:
                    # Add a variable
                    rvec = sumvec(rvec, mat[varmap[name]])

            mat[varmap[lhs]] = rvec

        else:
            raise ValueError('bad command in seq_to_mat: {}'.format(cmd))

    return mat


# Simplify a COWBASIC program
# Returns a linear program with no loop commands
def transform_program(raw_prog, varnames, varmap):
    prog = []
    stack = []

    for lineno, cmd in enumerate(raw_prog):
        if cmd[0] == 'loop':
            # Save the current list of commands for later
            stack.append((prog, cmd[1]))
            prog = []

        elif cmd[0] == 'endloop':
            prog_, n = stack.pop()

            # Convert the inner program to a matrix
            mat = seq_to_mat(prog, varnames, varmap)

            # Perform matrix exponentiation to execute the loop n times
            mat = mat_pow(mat, n)

            # Loop is replaced with a matrix multiplication
            prog_.append(('mat', mat))
            prog = prog_

        else:
            prog.append(cmd)

    return prog


# Runs a COWBASIC program and returns its output
def run_program(text):
    prog, varnames = parse_prog(text)

    # Create a reverse mapping of variables to positions
    varmap = {name: i for i, name in enumerate(varnames)}

    # Simplify program by eliminating all loop commands
    simple_prog = transform_program(prog, varnames, varmap)

    # Convert all but last command into a matrix
    mat = seq_to_mat(simple_prog[:-1], varnames, varmap)

    # The last (return) command extracts a particular variable
    return_cmd = simple_prog[-1]
    assert return_cmd[0] == 'return'
    retindex = varmap[return_cmd[1]]
    return mat[retindex][-1] % MOD


############################################################################
# Slam Shuffle functionality
############################################################################

def main(A):
    NCARDS = 10 if is_sample else 10007
    cards = list(range(NCARDS))  # index 0 is top

    # Solve part 2
    def part2():
        global MOD
        MOD = 119315717514047
        REP = 101741582076661

        ###################################################
        # Compute ax+b for fwd transform
        a = 1
        b = 0

        for line in A:
            tokens, integers = line
            if tokens[0] == 'cut':
                k = integers[0]
                b -= k
            elif tokens[0:3] == ['deal', 'with', 'increment']:
                k = integers[0]
                a *= k
                b *= k
            elif tokens[0:4] == ['deal', 'into', 'new', 'stack']:
                a *= -1
                b = -b - 1
            else:
                assert False

        a = a % MOD
        b = b % MOD

        ###################################################
        # Compute inverse
        inv_a = pow(a, MOD-2, MOD)
        inv_b = ((-b) * inv_a) % MOD

        ###################################################
        # Write a COWBASIC program to execute
        # "x = inv_a * x + inv_b" REP number of times

        cowbasic_prog = [
            'x = 2020',
            'invb = {}'.format(inv_b),
            '{} MOO {{'.format(REP),
            '  xpow = x',
            '  xinva = 0',
        ]

        # Use repeated addition to compute "xinva = inva * x"
        t = inv_a
        while t > 0:
            if t % 2 == 1:
                cowbasic_prog.append('  xinva = ( xinva ) + ( xpow )')
            cowbasic_prog.append('  xpow = ( xpow ) + ( xpow )')
            t //= 2

        cowbasic_prog += [
            '  x = ( xinva ) + ( invb )',
            '}',
            'RETURN x',
        ]

        cowbasic_prog = '\n'.join(cowbasic_prog)
        print('COWBASIC program:')
        print(cowbasic_prog)
        return run_program(cowbasic_prog)


    res = part2()
    submit_2(res)


##########################################################################


def parse_line(line):
    integers = re.findall(r'[-+]?\d+', line)
    integers = list(map(int, integers))
    tokens = line.split()
    return (tokens, integers)


def parse_input(A):
    A = A.strip()
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
