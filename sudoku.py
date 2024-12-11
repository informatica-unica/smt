from z3 import *
from random import *

N = 9 # size of the board
M = 3 # size and number of the boxes

# a valid Sudoku
b0 = [
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

def gen_sudoku(p): # p = percentage of blank
	b = [ [ 0 for j in range(N) ] for i in range(N) ]

	for i in range(N):
		for j in range(N):
			r = randint(1,100)
			if (p<r):
				b[i][j] = b0[i][j]
	return b
	
# b = [
# 	[0,0,3,0,0,2,4,1,0],
# 	[2,0,4,0,0,5,0,0,0],
# 	[0,1,0,0,7,4,0,2,8],
# 	[3,0,0,4,9,0,1,5,0],
# 	[0,0,7,0,1,0,0,0,6],
# 	[9,0,0,7,5,3,0,8,0],
# 	[8,4,0,0,0,0,6,0,0],
# 	[5,0,0,0,4,0,0,3,1],
# 	[1,3,6,0,2,0,5,0,0]
# 	]

def print_board(b):
	for i in range(N):
		for j in range(N):
			print(b[i][j] if b[i][j]!=0 else "-",end=" ")
		print()	

def print_model(m):
	for i in range(N):
		for j in range(N):
			print(m.eval(X[i][j]),end=" ")
		print()	

# ("," if j<len(b[i])-1 else "")

s = Solver()

b = gen_sudoku(90)

print_board(b)
print()

X = [ [ Int("x_%s_%s" % (i, j)) for j in range(N) ] for i in range(N) ]

# set variables

for i in range(N):
	for j in range(N):
		s.add(X[i][j]>0,X[i][j]<=N)
		if b[i][j]!=0:
			s.add(X[i][j]==b[i][j])

# all cells in a row are distinct
for i in range(N):
	for j in range(N):
		for h in range(j+1,N):
			s.add(X[i][j]!=X[i][h])

# all cells in a column are distinct
for j in range(N):
	for i in range(N):
		for h in range(i+1,N):
			s.add(X[i][j]!=X[h][j])

# all cells in a box are distinct

for i in range(M):
	for j in range(M):
		s.add(Distinct(X[i*M][j*M:(j+1)*M] + \
					   X[i*M+1][j*M:(j+1)*M] + \
					   X[i*M+2][j*M:(j+1)*M]))
	
if s.check()==sat:
	print_model(s.model())
else:
	print("UNSAT")
