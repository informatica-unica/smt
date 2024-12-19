"""
Ex4

Classical lupo, capra, cavoli problem (see: https://it.wikipedia.org/wiki/Problema_del_lupo,_della_capra_e_dei_cavoli)

Use SMT-based Model checking to find a successfull strategy.

"""


from z3 import *

def printModel(m):
    m_sorted = sorted ([(d, m[d]) for d in m], key = lambda x: str(x[0]))
    print(*m_sorted,sep='\n')

Max_Step = 30

# True iff lupo is on the other side of the river
lupo = [Bool("lupo_%s" % (i)) for i in range(Max_Step)]
...

s = Solver()

Action = Datatype('Method')
Action.declare('move_lupo')
Action.declare('...')
Action = Action.create()

action = [Const("f_%s" % (i), Action) for i in range(Max_Step+1)]

initial_state = And(
    Not(lupo[0]),   # Lupo is not on the other side
    ...
)

s.add(initial_state)

def no_changes(lupo_now, lupo_next, ...):
    return And(     lupo_next == lupo_now, 
                    ...
                    )

def move_lupo(lupo_now, lupo_next, ...):
    return If(... ,   # check that contadino is on the same side of lupo
               # if yes, lupo can be moved
               And( ...
                    ),
                # if no, the action fails and no-one moves 
                no_changes(...)
                )


for i in range(1, Max_Step-1):
    next_state = Or(
        And(action[i] == move_lupo(...) , ...),
        ... 
    )
    s.add(next_state)

    # Lupo cannot stay with capra unless contadino is present
    s.add(...)
    # Capra cannot stay with cavoli unless contadino is present
    s.add(...)

    # Property to verify
    res = s.check(And(...) )    # lupo, capra, and cavoli are all on the other side
    print(f"\nStep {i}: ",res)
    if res == sat:
        model = s.model()
        printModel(model)
        break
    else:
        print("Unsat")