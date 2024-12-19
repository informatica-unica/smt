from z3 import *

def printModel(m):
    m_sorted = sorted ([(d, m[d]) for d in m], key = lambda x: str(x[0]))
    print(*m_sorted,sep='\n')

SMALL_CAPACITY = 3
BIG_CAPACITY = 5
DESIRED_CAPACITY = 4

Max_Step = 20

small = [Int("small_%s" % (i)) for i in range(Max_Step)]
big = [Int("big_%s" % (i)) for i in range(Max_Step)]

s = Solver()

Action = Datatype('Method')
Action.declare('fill_small')
Action.declare('fill_big')
Action.declare('empty_small')
Action.declare('empty_big')
Action.declare('pour_small_into_big')
Action.declare('pour_big_into_small')
Action = Action.create()

action = [Const("f_%s" % (i), Action) for i in range(Max_Step+1)]

initial_state = And(
    small[0] == 0,
    big[0] == 0
)

s.add(initial_state)

def fill_small(small_now, small_next, big_now, big_next):
    return And(
        small_next == SMALL_CAPACITY,
        big_next == big_now
        )

def fill_big(small_now, small_next, big_now, big_next):
    return And(
        small_next == small_now,
        big_next == BIG_CAPACITY
        )


def empty_small(small_now, small_next, big_now, big_next):
    return And(
        small_next == 0,
        big_next == big_now
        )

def empty_big(small_now, small_next, big_now, big_next):
    return And(
        small_next == small_now,
        big_next == 0
        )

def pour_small_into_big(small_now, small_next, big_now, big_next):
    return If(small_now + big_now <= BIG_CAPACITY,
            And(
                small_next == 0,
                big_next == big_now + small_now
            ),  
            And(
                small_next == small_now - (BIG_CAPACITY - big_now),
                big_next == BIG_CAPACITY
            )
           )

def pour_big_into_small(small_now, small_next, big_now, big_next):
    return If(small_now + big_now <= SMALL_CAPACITY,
            And(
                small_next == small_now + big_now,
                big_next == 0,
            ),  
            And(
                small_next == SMALL_CAPACITY,
                big_next == big_now - (SMALL_CAPACITY - small_now),
            )
           )


for i in range(1, Max_Step-1):
    next_state = Or(
        And(action[i] == Action.fill_small , fill_small(small[i-1], small[i], big[i-1], big[i])),
        And(action[i] == Action.fill_big , fill_big(small[i-1], small[i], big[i-1], big[i])),
        And(action[i] == Action.empty_small , empty_small(small[i-1], small[i], big[i-1], big[i])),
        And(action[i] == Action.empty_big , empty_big(small[i-1], small[i], big[i-1], big[i])),
        And(action[i] == Action.pour_small_into_big , pour_small_into_big(small[i-1], small[i], big[i-1], big[i])),
        And(action[i] == Action.pour_big_into_small , pour_big_into_small(small[i-1], small[i], big[i-1], big[i])),
    )
    s.add(next_state)

    # Property to verify
    res = s.check(Or(small[i] == DESIRED_CAPACITY, big[i]==DESIRED_CAPACITY) )

    print(f"\nStep {i}: ",res)
    if res == sat:
        model = s.model()
        printModel(model)
        break