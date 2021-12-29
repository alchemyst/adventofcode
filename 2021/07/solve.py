import numpy as np
from scipy.optimize import minimize

from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

with open(filename) as f:
    numbers = [int(s) for s in f.read().strip().split(",")]

# # Part 1 - abs distance metric


def distance(x):
    return abs(np.array(numbers) - x).sum()


sol = minimize(distance, np.mean(numbers))
solution(distance(np.round(sol.x)))


# +
# Part 2 - quadratic cost + abs
# -


def cost(x):
    return (x ** 2 + x) / 2


def distance(x):
    return cost(abs(np.array(numbers) - x)).sum()


sol = minimize(distance, np.mean(numbers))

solution(distance(np.round(sol.x)))

# Initially I got the rounding wrong and thought my approach was wrong, so I brute forced it:

# x = np.arange(1, 500)
#
# tries = [(xi, distance(xi)) for xi in x]
#
# tries.sort(key=lambda i: i[1])
#
# tries[0]

# After the fact realisation:
# Part 1 is solved by the median (see https://math.stackexchange.com/questions/113270/the-median-minimizes-the-sum-of-absolute-deviations-the-ell-1-norm)
# Part 2 is solved by the mean (I think, but not sure why).
