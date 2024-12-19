from z3 import *
from random import *
from collections import deque
import time
from itertools import product
import argparse

from sudoku_utils import gen_sudoku, print_board, print_model

seed(111224)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="")
	parser.add_argument ('--N', type=int, help="Size of the board (4, 9, or 16)", required=True)
	parser.add_argument ('--Blank', type=int, help="Probabiliy of hiding a slot (used for matrix generation) ", required=True)
	parser.add_argument ('--poison_matrix', help='Make the starting matrix unsolvable', action='store_true', required=False, default=False)
	parser.add_argument ('--poison_matrix_mode', type=int, help="1 (two equal numbers in same row) or 2 (unfulfillable square)", required=False, default = 1)
	parser.add_argument ('--try_all_combs', help='Try all possible combinations', action='store_true', required=False, default=False)
	parser.add_argument ('--try_backtracking', help='Try all feasible combinations using backtracking', action='store_true', required=False, default=False)
	parser.add_argument ('--try_smt', help='Try to solve the Sudoku via SMT solving', action='store_true', required=False, default=False)
	parser.add_argument ('--proof', help='Ask z3 to return proof if problem unsat', action='store_true', required=False, default=False)
	
	args = parser.parse_args()
	N = args.N 
	M = int(math.sqrt(N))
	assert(M**2 == N)
	BLANK = args.Blank
	TRY_ALL_COMB = args.try_all_combs
	TRY_BACKTRACKING = args.try_backtracking
	TRY_SMT = args.try_smt
	POISON_MATRIX = args.poison_matrix
	POISON_MATRIX_MODE = args.poison_matrix_mode
	PROOF = args.proof


def is_valid_set(numbers):
    # Check if a set of N numbers (a row, column, or grid) contains only numbers from 1 to N without duplicates
    return sorted(numbers) == list(range(1, N+1))

def is_valid_sudoku(board):
    # Check if the board is a valid Sudoku solution.
    # Check all rows
	for row in board:
		if not is_valid_set(row):
			return False
    # Check all columns
	for col in range(N):
		column = [board[row][col] for row in range(N)]
		if not is_valid_set(column):
			return False
    # Check all MxM subgrids
	for row in range(0, N, M):
		for col in range(0, N, M):
			grid = [board[r][c] for r in range(row, row + M) for c in range(col, col + M)]
			if not is_valid_set(grid):
				return False
    # If all checks pass, it's a valid Sudoku solution
	return True	


def try_all_combinations(board):
	my_board = board
	empty_slots = []
	for r in range(N):
		for c in range(N):
			if board[r][c] == 0:
				empty_slots.append([r,c])
	print("Number of empty slots: ", len(empty_slots))
	for combination in product(range(1, N+1), repeat=len(empty_slots)):
		for i, empty_slot in enumerate(empty_slots):
			slot_row = empty_slot[0]
			slot_col = empty_slot[1]
			my_board[slot_row][slot_col] = combination[i]
		ok = is_valid_sudoku(my_board)
		if ok:
			return my_board
	return False
                    


# Function to check if a number can be placed in a given position
def is_insertion_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    # Check column
    if num in [board[i][col] for i in range(N)]:
        return False
    # Check MxM grid
    start_row, start_col = M * (row // M), M * (col // M)
    for i in range(start_row, start_row + M):
        for j in range(start_col, start_col + M):
            if board[i][j] == num:
                return False
    return True

def try_combinations_backtrack(board):
    empty = deque()
    # Collect empty cells
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                empty.append((r, c))
    # Backtracking algorithm to fill in the grid
    def backtrack():
        if not empty:
            return True  # Puzzle is solved
        row, col = empty.popleft()
        for num in range(1, N+1):
           if is_insertion_valid(board, row, col, num):
                board[row][col] = num
                if backtrack():
                    return True
                board[row][col] = 0  # Reset and try the next number
        empty.appendleft((row, col))  # Backtrack to previous empty cell
        return False
    # Start solving the puzzle
    backtrack()
    return board



def use_smt(board, PROOF):
	if PROOF:
		set_param(proof=True)
	solver = Solver()

	# Integer representation is slower
	#X = [ [ Int("x_%s_%s" % (i, j)) for j in range(N) ] for i in range(N) ]

	X = [ [ BitVec("x_%s_%s" % (i, j), 8) for j in range(N) ] for i in range(N) ]

	# set variables
	for i in range(N):
		for j in range(N):
			solver.add(X[i][j] > 0, X[i][j] <= N)	# Constrain variables to value between 1 and N
			if board[i][j] != 0:
				solver.add(X[i][j] == board[i][j])	# Set variables to pre-existent values

	# all cells in a row are distinct
	for i in range(N):
		vars_in_ith_row = [X[i][j] for j in range(N)]
		solver.add(Distinct(vars_in_ith_row))

	# all cells in a column are distinct
	for i in range(N):
		vars_in_ith_column = [X[j][i] for j in range(N)]
		solver.add(Distinct(vars_in_ith_column))

	# all cells in a box are distinct
	for i in range(M):
		for j in range(M):
			solver.add(Distinct(sum([X[i*M+k][j*M:(j+1)*M] for k in range(M)],[])))

	return solver, X

board = gen_sudoku(M, BLANK, POISON_MATRIX, POISON_MATRIX_MODE)

print_board(board)


if TRY_ALL_COMB:
	solved_board = try_all_combinations(board)
	print("Solution (by trying all possible combinations):")
	if solved_board:
		print_board(solved_board)
	else:
		print("False")

if TRY_BACKTRACKING:
	solved_board = try_combinations_backtrack(board)
	print("Solution (by using backtracking):")
	if solved_board:
		print_board(solved_board)
	else:
		print("False")

if TRY_SMT:	
	solver, X = use_smt(board, PROOF)
	if solver.check()==sat:
		print("Solution (by using SMT):")
		print_model(solver.model(), X)
	else:
		print("UNSAT")
		if PROOF:
			print(solver.proof().children())

