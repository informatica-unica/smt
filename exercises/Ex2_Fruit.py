"""
Ex2.1

Gavina and Gavino go to San Benedetto market to buy apples, bananas, and carrots.
They want to buy exactly 100 fruits, spending exactly 100€.
They want to buy at least 1 apple, 1 banana, and 1 carrot.
1 banana costs 2€ (inflation...)
1 apple costs 1€
1 carrot costs 50c

Ex 2.1.a How many apples, bananas, and carrots can they buy to satisfy the previous conditions?

Ex 2.1.b Is there more than a way to buy the fruit satisfying the previous conditions?

Ex 2.1.c If they decide to buy at least 40 bananas, are they still able to satisfy the previous conditions?

Ex 2.1.d [Hard] Compute how many possible combinations of apples, bananas, and carrots satisfy the initial conditions.
"""


from z3 import *

# Create 3 integer variables
apple, banana, carrot = Ints('apple banana carrot')
solve(apple >= 1,   # at least one apple
      ... ,   # at least one banana
      ... , # at least one carrot
      ... , # exactly 100 fruits overall
      ... # final cost must be 100€
      )


"""
Ex2.1

Saturnina and Saturnino go to San Benedetto market to buy pine nuts, ananas, and limes.
They want to buy exactly 100 fruits, spending exactly 100€.
They want to buy at least pine nut, 1 ananas, and 1 lime.
1 pine nut costs 40€ 
1 ananas costs 1€
1 lime costs 50c

Ex 2.2.a How many pine nuts, ananas, and limes can they buy to satisfy the previous conditions?

Ex 2.2.b Is there more than a way to buy the fruit satisfying the previous conditions?
"""
