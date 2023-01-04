'''Magic Square

https://en.wikipedia.org/wiki/Magic_square

A magic square is a n * n square grid filled with distinct positive integers in
the range 1, 2, ..., n^2 such that each cell contains a different integer and
the sum of the integers in each row, column, and diagonal is equal.

'''

# Reference: https://github.com/HaoDong96/ECE653_QA/blob/0e31227a78be659fba1b25178ed94f9df9ed7dc8/a2-HaoDong96/a2q3/magic_square.py

from z3 import Solver, sat, unsat
from z3 import *

def solve_magic_square(n, r, c, val):
    solver = Solver()

    # CREATE CONSTRAINTS AND LOAD STORE THEM IN THE SOLVER

    # initial an nxn square
    square = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(Int("x_%s_%s" % (i, j)))
        square.append(row)
   
    # each cell has a distinct number
    all_numbers = []
    for i in range(n):
        for j in range(n):
            all_numbers.append(square[i][j])
    solver.add(Distinct(all_numbers))

    # each interger from 1 to n^2
    for i in range(n):
        for j in range(n):
            solver.add(square[i][j]>=1)
            solver.add(square[i][j]<=pow(n,2))


    # row sum
    for i in range(n):
        for j in range(i+1,n):
            solver.add(Sum(square[i])==Sum(square[j]))

    # column sum
    solver.add([Sum([square[i][j] for i in range(n)]) == Sum(square[0]) for j in range(n)])

    # diagonal sum
    solver.add([Sum([square[i][i] for i in range(n)]) == Sum(square[0])])
    solver.add([Sum([square[i][n - i - 1] for i in range(n)]) == Sum(square[0])])

    # initialize square[r][c] = val
    solver.add([square[r][c] == val])

    # CREATE CONSTRAINTS AND LOAD STORE THEM IN THE SOLVER

    if solver.check() == sat:
        mod = solver.model()
        res = []

        # CREATE RESULT MAGIC SQUARE BASED ON THE MODEL FROM THE SOLVER
        res = [[mod.evaluate(square[i][j]).as_long() for j in range(n)] for i in range(n)]
        return res
    else:
        return None


def print_square(square):
    '''
    Prints a magic square as a square on the console
    '''
    n = len(square)

    assert n > 0
    for i in range(n):
        assert len(square[i]) == n

    for i in range(n):
        line = []
        for j in range(n):
            line.append(str(square[i][j]))
        print('\t'.join(line))


def puzzle(n, r, c, val):
    res = solve_magic_square(n, r, c, val)
    if res is None:
        print('No solution!')
    else:
        print('Solution:')
        print_square(res)


if __name__ == '__main__':
    n = 3
    r = 1
    c = 1
    val = 5
    puzzle(n, r, c, val)
