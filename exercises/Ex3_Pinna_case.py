"""
Ex3 [Author: Massimo Bartoletti]

An atrocious crime was committed last night at the Science Palace: 
Prof. Pinna was found dead in a pool of blood. The police,
after a throughout inspection, has come to the following conclusions:
1. If the murder was committed after midnight, then the crime scene
cannot be the Batcave, or Prof. Scateni is innocent.
2. If Prof. Scateni is guilty, then the murder weapon is a 3D printer.
3. If the murder weapon is a 3D printer and the murder was committed
in the Batcave, then the time of the murder is after midnight.
Assume that the police eventually discovers that the murder was committed in the Batcave. 
After knowing this fact, can we infer that Prof. Scateni is innocent?
"""

from z3 import *

# M = the murder was committed after midnight;
M = Bool('M')

# B = the crime scene is the Batcave;
B = Bool('B')

# I = Prof. Scateni is innocent;
...

# P = the murder weapon is a 3D printer.
...

s = Solver()

# 1) M => not B or I
s.add(Implies(M,Or(Not(B),I)))

# 2) not I => P
# ...

# 3) ...
# ...

# assert B

if ... :
    print("Prof. Scateni is innocent")
else:
    print("Prof. Scateni could be guilty")
    print(s.model())    
