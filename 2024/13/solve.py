import aoc.parse
from aoc import solution
import pathlib
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

problems = []

# cost function
cost = np.array([3, 1], dtype=int)

# parse input
for chunk in pathlib.Path(filename).read_text().split('\n\n'):
    lines = chunk.splitlines(keepends=False)

    # equality constraints
    coeffs = np.array([list(aoc.parse.all_numbers(line)) for line in lines[:2]], dtype=int).T
    target = np.array(list(aoc.parse.all_numbers(lines[2])), dtype=int)

    problems.append((coeffs, target))

def tokens(coeffs, target):
    move = np.linalg.solve(coeffs, target).round().astype(int)
    if (coeffs @ move == target).all() & (move >= 0).all():
        return cost @ move

    return 0


# Part 1
solution(sum(tokens(coeffs, target) for coeffs, target in problems))

# Part 2
solution(sum(tokens(coeffs, target + 10000000000000) for coeffs, target in problems))
