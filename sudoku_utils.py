from z3 import *
from random import *
from collections import deque
import time
from itertools import product

seed(111224)


# Valid Sudokus

b0_2 = [
    [2, 4,  1, 3],
	[1, 3,  4, 2 ],
	[4, 2,  3, 1],
	[3, 1,  2, 4]
]

b0_3s = [
	[1,2,3,4,5,6,7,8,9],
	[4,5,6,7,8,9,1,2,3],
	[7,8,9,1,2,3,4,5,6],
	[2,3,4,5,6,7,8,9,1],
	[5,6,7,8,9,1,2,3,4],
	[8,9,1,2,3,4,5,6,7],
	[3,4,5,6,7,8,9,1,2],
	[6,7,8,9,1,2,3,4,5],
	[9,1,2,3,4,5,6,7,8]
]
b0_3 = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8]
]

b0_4 = [
    [11, 6, 8, 15, 14, 2, 16, 3, 5, 10, 12, 7, 1, 4, 9, 13],
    [2, 10, 1, 16, 4, 13, 7, 9, 15, 3, 8, 6, 14, 12, 5, 11],
    [14, 13, 7, 9, 12, 5, 6, 10, 2, 11, 4, 1, 16, 3, 15, 8],
    [12, 5, 3, 4, 1, 11, 15, 8, 14, 13, 16, 9, 10, 2, 7, 6],
    [1, 4, 13, 10, 9, 8, 12, 7, 6, 16, 11, 15, 5, 14, 2, 3],
    [9, 11, 5, 2, 13, 15, 10, 16, 3, 4, 14, 8, 7, 6, 1, 12],
    [16, 14, 12, 7, 11, 3, 1, 6, 10, 5, 9, 2, 4, 8, 13, 15],
    [15, 8, 6, 3, 5, 4, 14, 2, 13, 1, 7, 12, 9, 10, 11, 16],
    [7, 9, 10, 8, 3, 14, 5, 11, 16, 15, 6, 4, 13, 1, 12, 2],
    [6, 16, 14, 11, 2, 12, 9, 15, 8, 7, 1, 13, 3, 5, 10, 4],
    [3, 1, 15, 12, 16, 10, 4, 13, 9, 2, 5, 11, 8, 7, 6, 14],
    [5, 2, 4, 13, 6, 7, 8, 1, 12, 14, 3, 10, 11, 15, 16, 9],
    [4, 3, 2, 1, 7, 16, 13, 5, 11, 12, 15, 14, 6, 9, 8, 10],
    [10, 15, 16, 6, 8, 1, 2, 14, 7, 9, 13, 3, 12, 11, 4, 5],
    [8, 7, 11, 5, 15, 9, 3, 12, 4, 6, 10, 16, 2, 13, 14, 1],
    [13, 12, 9, 14, 10, 6, 11, 4, 1, 8, 2, 5, 15, 16, 3, 7]
]

b0_5 = [
    [24, 22, 18, 13, 16, 2, 11, 15, 1, 4, 25, 10, 19, 8, 14, 17, 6, 23, 7, 5, 12, 3, 20, 9, 21],
    [10, 8, 19, 14, 4, 22, 9, 6, 7, 25, 21, 3, 11, 1, 13, 15, 12, 20, 18, 2, 5, 23, 24, 17, 16],
    [5, 15, 9, 11, 2, 10, 17, 14, 12, 19, 18, 22, 23, 20, 24, 21, 1, 4, 3, 16, 8, 6, 7, 13, 25],
    [25, 23, 3, 12, 6, 16, 21, 20, 13, 18, 9, 15, 7, 17, 5, 8, 24, 22, 10, 14, 11, 2, 1, 19, 4],
    [1, 7, 20, 21, 17, 8, 24, 5, 23, 3, 16, 4, 6, 12, 2, 11, 9, 13, 25, 19, 15, 10, 18, 14, 22],
    [4, 25, 21, 23, 8, 1, 14, 3, 18, 7, 2, 24, 5, 13, 17, 10, 20, 11, 9, 6, 16, 19, 12, 22, 15],
    [19, 18, 17, 2, 22, 20, 12, 25, 9, 11, 14, 7, 8, 16, 1, 23, 21, 15, 24, 3, 10, 13, 6, 4, 5],
    [14, 16, 24, 15, 12, 5, 2, 23, 21, 10, 6, 19, 25, 3, 11, 4, 8, 18, 13, 22, 17, 20, 9, 1, 7],
    [13, 6, 7, 5, 9, 24, 16, 17, 4, 22, 10, 20, 15, 21, 12, 14, 2, 1, 19, 25, 3, 11, 23, 18, 8],
    [20, 11, 1, 10, 3, 13, 6, 19, 8, 15, 22, 9, 4, 18, 23, 16, 7, 5, 12, 17, 21, 24, 14, 25, 2],
    [11, 10, 5, 7, 14, 4, 23, 8, 19, 1, 24, 17, 2, 15, 9, 12, 13, 25, 6, 21, 18, 22, 16, 3, 20],
    [16, 1, 13, 9, 18, 14, 25, 24, 2, 6, 7, 12, 10, 4, 22, 3, 15, 8, 17, 20, 19, 5, 11, 21, 23],
    [8, 2, 15, 17, 21, 7, 13, 22, 20, 5, 11, 23, 18, 6, 3, 24, 19, 16, 4, 9, 25, 1, 10, 12, 14],
    [22, 12, 6, 24, 23, 9, 3, 11, 17, 21, 20, 25, 16, 5, 19, 1, 18, 7, 14, 10, 4, 15, 2, 8, 13],
    [3, 19, 4, 25, 20, 18, 15, 10, 16, 12, 1, 8, 13, 14, 21, 22, 11, 2, 5, 23, 24, 7, 17, 6, 9],
    [9, 5, 23, 16, 10, 11, 7, 4, 24, 17, 12, 6, 1, 22, 25, 18, 14, 3, 20, 13, 2, 21, 8, 15, 19],
    [6, 3, 2, 19, 25, 15, 5, 12, 14, 8, 4, 13, 17, 10, 20, 7, 23, 21, 1, 24, 9, 16, 22, 11, 18],
    [18, 13, 14, 1, 11, 19, 10, 2, 22, 16, 23, 5, 21, 24, 15, 9, 4, 6, 8, 12, 7, 25, 3, 20, 17],
    [17, 21, 8, 4, 15, 23, 20, 18, 3, 13, 19, 14, 9, 2, 7, 25, 22, 10, 16, 11, 6, 12, 5, 24, 1],
    [12, 24, 22, 20, 7, 25, 1, 21, 6, 9, 8, 18, 3, 11, 16, 5, 17, 19, 2, 15, 14, 4, 13, 23, 10],
    [2, 17, 12, 8, 5, 21, 22, 13, 11, 23, 3, 16, 20, 9, 10, 6, 25, 14, 15, 4, 1, 18, 19, 7, 24],
    [21, 14, 16, 3, 24, 6, 8, 7, 10, 20, 13, 1, 12, 25, 4, 19, 5, 9, 22, 18, 23, 17, 15, 2, 11],
    [23, 4, 11, 6, 1, 3, 19, 16, 15, 14, 17, 2, 22, 7, 18, 20, 10, 24, 21, 8, 13, 9, 25, 5, 12],
    [15, 9, 10, 22, 19, 12, 18, 1, 25, 2, 5, 21, 24, 23, 8, 13, 3, 17, 11, 7, 20, 14, 4, 16, 6],
    [7, 20, 25, 18, 13, 17, 4, 9, 5, 24, 15, 11, 14, 19, 6, 2, 16, 12, 23, 1, 22, 8, 21, 10, 3]
]

b0_6 = [
    [1, 2, 3, 4, 5, 6,  7, 8, 9, 10, 11, 12,  13, 14, 15, 16, 17, 18,  19, 20, 21, 22, 23, 24,  25, 26, 27, 28, 29, 30,  31, 32, 33, 34, 35, 36],
    [7, 8, 9, 10, 11, 12,  13, 14, 15, 16, 17, 18,  19, 20, 21, 22, 23, 24,  25, 26, 27, 28, 29, 30,  31, 32, 33, 34, 35, 36,  1, 2, 3, 4, 5, 6],
    [13, 14, 15, 16, 17, 18,  19, 20, 21, 22, 23, 24,  25, 26, 27, 28, 29, 30,  31, 32, 33, 34, 35, 36,  1, 2, 3, 4, 5, 6,  7, 8, 9, 10, 11, 12],
    [19, 20, 21, 22, 23, 24,  25, 26, 27, 28, 29, 30,  31, 32, 33, 34, 35, 36,  1, 2, 3, 4, 5, 6,  7, 8, 9, 10, 11, 12,  13, 14, 15, 16, 17, 18],
    [25, 26, 27, 28, 29, 30,  31, 32, 33, 34, 35, 36,  1, 2, 3, 4, 5, 6,  7, 8, 9, 10, 11, 12,  13, 14, 15, 16, 17, 18,  19, 20, 21, 22, 23, 24],
    [35, 34, 33, 32, 36, 31,  1, 3, 4, 6, 2, 5,  9, 7, 10, 12, 8, 11,  17, 14, 16, 15, 13, 18,  24, 23, 20, 19, 22, 21,  28, 30, 29, 25, 26, 27],
    [3, 15, 2, 1, 4, 14,  28, 10, 30, 13, 22, 26,  20, 36, 34, 5, 24, 12,  32, 19, 29, 25, 8, 9,  18, 35, 21, 23, 31, 17,  16, 33, 6, 7, 27, 11],
    [27, 9, 18, 21, 31, 16,  23, 25, 2, 12, 36, 7,  32, 11, 35, 6, 28, 19,  30, 15, 4, 24, 33, 14,  20, 1, 8, 13, 3, 5,  17, 10, 22, 26, 29, 34],
    [32, 5, 11, 33, 22, 29,  4, 9, 35, 24, 19, 6,  14, 1, 16, 21, 31, 27,  23, 10, 2, 18, 17, 20,  12, 36, 26, 7, 30, 34,  3, 15, 25, 8, 13, 28],
    [28, 24, 25, 23, 34, 7,  33, 18, 5, 29, 20, 11,  3, 22, 13, 8, 30, 17,  26, 16, 6, 35, 36, 1, 10, 9, 4, 15, 27,  32, 12, 19, 2, 14, 31, 21],
    [12, 36, 26, 20, 6, 19,  27, 15, 34, 8, 21, 17,  4, 18, 2, 25, 10, 9,  11, 28, 31, 13, 3, 7,  33, 22, 29, 14, 16, 24,  30, 5, 23, 35, 32, 1],
    [30, 13, 8, 17, 35, 10,  32, 16, 1, 3, 14, 31,  7, 23, 29, 26, 33, 15,  21, 12, 22, 27, 34, 5,  19, 6, 28, 25, 2, 11,  24, 18, 4, 36, 20, 9],
    [8, 32, 24, 2, 28, 33,  15, 7, 36, 21, 26, 1,  23, 3, 25, 17, 20, 31,  29, 34, 30, 9, 6, 13,  14, 11, 35, 18, 19, 27,  10, 22, 16, 5, 12, 4],
    [21, 23, 30, 29, 16, 34,  22, 24, 18, 32, 12, 14,  2, 5, 4, 27, 15, 1,  8, 11, 35, 36, 19, 26,  6, 17, 10, 31, 33, 13,  20, 9, 7, 3, 28, 25],
    [36, 25, 13, 7, 26, 17,  35, 11, 31, 2, 27, 28,  33, 10, 12, 24, 14, 32,  22, 1, 20, 5, 4, 15,  8, 16, 23, 3, 21, 9,  18, 6, 30, 29, 34, 19],
    [9, 19, 22, 6, 3, 4,  34, 30, 13, 23, 5, 33,  16, 28, 18, 29, 7, 35,  12, 21, 10, 14, 31, 27,  32, 20, 25, 36, 1, 15,  2, 26, 17, 11, 24, 8],
    [14, 1, 20, 35, 27, 15,  10, 17, 8, 9, 16, 3,  26, 30, 11, 19, 6, 22,  28, 18, 24, 23, 25, 2,  4, 29, 12, 5, 34, 7,  21, 13, 36, 32, 33, 31],
    [10, 31, 12, 11, 18, 5,  6, 29, 20, 19, 25, 4,  21, 8, 9, 36, 34, 13,  33, 7, 17, 16, 32, 3,  2, 24, 22, 30, 26, 28,  15, 27, 35, 23, 1, 14],
    [17, 33, 29, 8, 19, 28,  18, 13, 24, 36, 7, 27,  11, 16, 1, 35, 22, 14,  2, 23, 5, 21, 26, 32,  30, 12, 6, 20, 15, 4,  25, 34, 10, 31, 9, 3],
    [31, 27, 35, 14, 20, 3,  17, 5, 11, 25, 6, 23,  34, 13, 30, 18, 26, 10,  9, 4, 19, 8, 24, 16,  21, 7, 36, 29, 28, 2,  33, 12, 32, 1, 22, 15],
    [11, 10, 6, 36, 15, 26,  9, 21, 19, 1, 28, 29,  24, 12, 32, 23, 2, 3,  27, 35, 25, 33, 7, 22,  5, 31, 34, 17, 18, 16,  14, 4, 8, 13, 30, 20],
    [34, 16, 7, 18, 24, 22,  30, 12, 32, 35, 4, 15,  5, 29, 17, 33, 21, 25,  20, 6, 13, 3, 14, 31,  27, 10, 1, 8, 9, 19,  23, 11, 26, 28, 36, 2],
    [2, 21, 4, 9, 12, 32,  26, 22, 3, 20, 31, 16,  15, 27, 28, 7, 36, 8,  10, 30, 34, 1, 18, 29,  11, 13, 14, 33, 23, 25,  5, 35, 24, 6, 19, 17],
    [5, 30, 1, 25, 13, 23,  8, 2, 14, 33, 10, 34,  6, 31, 19, 9, 4, 20,  36, 17, 15, 11, 12, 28,  35, 3, 32, 22, 24, 26,  29, 16, 27, 21, 18, 7],
    [20, 18, 19, 31, 10, 11,  21, 23, 22, 7, 34, 13,  8, 25, 6, 3, 27, 5,  16, 36, 28, 26, 9, 4,  29, 33, 17, 2, 12, 14,  35, 24, 1, 30, 15, 32],
    [24, 4, 23, 3, 32, 9,  12, 27, 26, 30, 15, 2,  17, 34, 7, 10, 11, 28,  13, 29, 18, 31, 22, 21,  16, 25, 5, 35, 6, 1,  8, 36, 19, 20, 14, 33],
    [26, 6, 36, 30, 8, 2,  20, 35, 17, 11, 18, 25,  29, 9, 22, 32, 13, 4,  5, 27, 14, 19, 1, 33,  23, 15, 7, 24, 10, 3,  34, 31, 28, 12, 21, 16],
    [22, 17, 34, 5, 25, 35,  36, 1, 16, 4, 32, 19,  18, 33, 20, 14, 12, 2,  6, 24, 7, 30, 15, 23,  28, 27, 31, 21, 13, 8,  26, 3, 11, 9, 10, 29],
    [15, 29, 28, 13, 7, 21,  5, 33, 6, 14, 8, 10,  30, 24, 26, 31, 1, 16,  35, 3, 11, 12, 2, 17,  9, 34, 19, 32, 36, 20,  4, 23, 18, 27, 25, 22],
    [16, 12, 14, 27, 33, 1,  24, 28, 29, 31, 3, 9,  35, 21, 36, 15, 19, 23,  34, 25, 32, 20, 10, 8,  26, 30, 18, 11, 4, 22,  6, 7, 13, 17, 2, 5],
    [23, 35, 32, 24, 2, 13,  29, 36, 10, 26, 33, 20,  28, 6, 8, 1, 25, 7,  4, 5, 12, 17, 27, 11,  15, 19, 16, 9, 14, 31,  22, 21, 34, 18, 3, 30],
    [18, 28, 10, 19, 21, 20,  3, 6, 12, 5, 30, 35,  27, 15, 31, 2, 9, 34,  24, 22, 36, 32, 16, 25,  17, 4, 13, 1, 7, 23,  11, 29, 14, 33, 8, 26],
    [33, 11, 31, 12, 1, 8,  16, 4, 28, 15, 24, 22,  10, 35, 14, 30, 32, 21,  3, 13, 26, 7, 20, 34,  36, 18, 2, 27, 25, 29,  9, 17, 5, 19, 6, 23],
    [29, 3, 5, 15, 30, 36,  14, 19, 25, 17, 9, 32,  22, 4, 24, 20, 16, 26,  18, 33, 23, 6, 28, 35,  34, 21, 11, 12, 8, 10,  27, 1, 31, 2, 7, 13],
    [6, 22, 16, 34, 14, 25,  2, 31, 7, 27, 13, 8,  36, 17, 23, 11, 18, 33,  15, 9, 1, 29, 21, 19,  3, 5, 30, 26, 20, 35,  32, 28, 12, 24, 4, 10],
    [4, 7, 17, 26, 9, 27,  11, 34, 23, 18, 1, 21,  12, 19, 5, 13, 3, 29,  14, 31, 8, 2, 30, 10,  22, 28, 24, 6, 32, 33,  36, 25, 20, 15, 16, 35]
]


def get_correct_matrix(M):
	assert(M in [2,3,4,5,6])
	if M == 2:
		return b0_2
	elif M == 3:
		return b0_3
	elif M == 4:
		return b0_4
	elif M == 5:
		return b0_5
	elif M == 6:
		return b0_6
	else:
		assert(False)


def gen_sudoku(M, p, poison_matrix = False, poison_matrix_mode = -1): 
	b0 = get_correct_matrix(M)

	N = M*M
	b = [ [ 0 for j in range(N) ] for i in range(N) ]

	for i in range(N):
		for j in range(N):
			r = randint(1,100)
			if (p<r):
				b[i][j] = b0[i][j]
	if poison_matrix:
		assert (poison_matrix_mode in [1,2])
		if poison_matrix_mode == 1:
			b[-1][-1] = 9
			b[-1][-2] = 9
		else:
			for i in range(1, M):
				b[i-1][i-1] = 9
				b[-i][-i] = 9
			b[M*(M-1)][M-1] = 1
	return b
	
def print_board(b):
	N = len(b)
	M = math.sqrt(N)
	for i in range(N):
		for j in range(N):
			print(b[i][j] if b[i][j]!=0 else "-",end=" ")
			if (j+1)%M == 0:
				print('\t',end="")
		if (i+1)%M == 0:
			print('')
		print()	
	print()

def print_model(model, X):
	N = len(X)
	M = math.sqrt(N)
	for i in range(N):
		for j in range(N):
			print(model.eval(X[i][j]),end=" ")
			if (j+1)%M == 0:
				print(' ',end="")
		if (i+1)%M == 0:
			print('')
		print()	
