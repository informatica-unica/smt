# Symbolic AI and SMT solving

Symbolic AI is an approach to Artificial Intelligence that uses deductive reasoning to produce exact and explainable results to well-defined problems, compared to sub-symbolic methods (e.g. machine learning, deep NNs, LLMs, etc.), which use statistical learning to tackle a wide variety of tasks (possibly vaguely defined) to produce plausible answers (which can however be incorrect and that are usually not explainable). Integration between symbolic and sub-symbolic methods is a hot topic in AI.

SMT solvers are tools that can be used to reason about and rigorously solve different kinds of problems, involving arithmetic, arrays, bit vectors, etc. They are used in industrial applications for several tasks, such as program verification, planning, testing, etc. 

In this lesson, we introduce z3, an efficient and user-friendly  SMT solver developed by Microsoft. We will compare it to both user-written algorithms and LLMs on a simple task such as solving a Sudoku. We will also see how to use z3 to solve the Die Hard jug puzzle (a model checking problem). 

Finally, we will give a few exercises to experiment with the tool.


## Requirements

Install z3 Python APIs through pip: 
```pip3 install z3-solver```
