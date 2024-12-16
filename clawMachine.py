#
# clawMachine.py
#
# From 13th day of Advent of Code 2024
# https://adventofcode.com/2024/day/13
#
# For each machine, you have the following information:
# - How many cells the A button moves the claw in the X and Y axis [buttonA]
# - How many cells the B button moves the claw in the X and Y axis [buttonB]
# - The X and Y coordinates of the prize [prize]
#
# It costs 3 tokens to push the A button and 1 token to push the B button.
#
# What is the smallest number of tokens you would have to spend
# to win as many prizes as possible?
#
# Z3 solution by dalps
#
from z3 import *
from collections import namedtuple
from pyparsing import *

Point = namedtuple("Point", ["x", "y"])
Machine = namedtuple("Machine", ["buttonA", "buttonB", "prize"])

integer = Word(nums)
movement = Suppress("Button " + (Literal("A") ^ Literal("B")) +
                    ": X+") + integer("x") + Suppress(", Y+") + integer("y")
prize = Suppress("Prize: X=") + integer("px") + \
    Suppress(", Y=") + integer("py")
expr = Group(movement("a") + movement("b") + prize("p"))
p = OneOrMore(expr)

machines = p.parseFile("clawMachine.txt")

def solve(prizeShift=0):
  totalCost = 0   # Accumulate tokens spent on all machines

  for m in machines:
    m = Machine(buttonA=Point(int(m["a"][0]), int(m["a"][1])),
                buttonB=Point(int(m["b"][0]), int(m["b"][1])),
                prize=Point(int(m["p"][0]), int(m["p"][1])))

    costA = Int("costA")
    costB = Int("costB")
    c = IntVal(prizeShift)

    s = Solver()

    s.add(m.buttonA.x * costA + m.buttonB.x * costB == m.prize.x + c)
    s.add(m.buttonA.y * costA + m.buttonB.y * costB == m.prize.y + c)

    print("Printing the assertions...")
    for c in s.assertions():
      print(c)

    print("Solving constraints in the solver s...")
    print(s.check())

    if s.check() == sat:
      # The prize can be reached, but at what cost?
      # Let's extract the token expense from the model.
      # [as_long()] converts a Z3 Integer to a regular integer

      mdl = s.model()

      machineCost = mdl[costA].as_long() * 3 + mdl[costB].as_long()
      totalCost += machineCost

      print("Traversing model...")
      for d in mdl.decls():
        print("%s = %s" % (d.name(), mdl[d]))

    print("---")

  return totalCost


solve1 = solve()
solve2 = solve(10000000000000)

print(solve1, solve2)
