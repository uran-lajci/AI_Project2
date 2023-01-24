"""OR-Tools solution to the N-queens problem."""
import sys
from ortools.constraint_solver import pywrapcp


def main(board_size, blocked_positions):
    # Creates the solver.
    solver = pywrapcp.Solver('n-queens')

    # Creates the variables.
    # The array index is the column, and the value is the row.
    queens = [
        solver.IntVar(0, board_size - 1, f'x{i}') for i in range(board_size)
    ]

    # Creates the constraints.
    # All rows must be different.
    solver.Add(solver.AllDifferent(queens))

    # No two queens can be on the same diagonal.
    solver.Add(solver.AllDifferent([queens[i] + i for i in range(board_size)]))
    solver.Add(solver.AllDifferent([queens[i] - i for i in range(board_size)]))

    for pos in blocked_positions:
        row, col = pos
        solver.Add(queens[col] != row)

    db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND,
                      solver.ASSIGN_MIN_VALUE)

    # Iterates through the solutions, displaying each.
    num_solutions = 0
    solver.NewSearch(db)
    while solver.NextSolution():
        # Displays the solution just computed.
        for i in range(board_size):
            for j in range(board_size):
                if queens[j].Value() == i:
                    # There is a queen in column j, row i.
                    print('Q', end=' ')
                else:
                    print('_', end=' ')
            print()
        print()
        num_solutions += 1
    solver.EndSearch()

    # Statistics.
    print('\nStatistics')
    print(f'  failures: {solver.Failures()}')
    print(f'  branches: {solver.Branches()}')
    print(f'  wall time: {solver.WallTime()} ms')
    print(f'  Solutions found: {num_solutions}')


if __name__ == '__main__':
    # By default, solve the 8x8 problem.
    size = 4
    blocked_positions = [(0,0),(0,1)]
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    main(size, blocked_positions)