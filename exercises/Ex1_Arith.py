from z3 import *


"""
Ex 1.1

Write a function that takes as input an integer n
and finds positive integers a, b such that a^2 - b = n.
"""

def diffOfSquares(n_input):
    s = Solver()
    n, a, b = Ints('n a b') # declare variables
    s.add(And(n == n_input,             # z3 variable equal to input variable   
              a > 0 ,                    # a positive
              ... ,                    # b positive
              a**2 - b**2 == n          # condition
              )
        )        
    if s.check() == sat:
        print("sat")
        print(s.model())
    else:
        print("unsat")
        
diffOfSquares(12345)


"""
Ex 1.2 

Write a function that takes as input an integer n
and finds distinct positive integers a, b, c such that a^2 + b^2 - c^2 = n.

def sumDiffOfSquares(n_input):
    ...

sumDiffOfSquares(12345)
"""




"""
Ex 1.3

Write a function that takes as input a positive integer n
and checks whether n is a prime. 
If n is not a prime, the function should print some information 
that proves that n is not a prime.

def isPrime(n_input):

isPrime(12345)
"""


"""
Ex 1.4

Write a function that takes as input two positive integers n, m,
and checks whether a and b can be part of a Pythagorean triple.

def arePartOfPythagorean(n_input, m_input):
    ...

arePartOfPythagorean(12, 35) # expected: sat
arePartOfPythagorean(33, 65) # expected: sat
arePartOfPythagorean(89, 39) # expected: sat
arePartOfPythagorean(89, 139) # expected: unsat
arePartOfPythagorean(45, 824) # expected: unsat
"""
