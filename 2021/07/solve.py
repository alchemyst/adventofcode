#!/usr/bin/env python
debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    numbers = [int(s) for s in f.read().strip().split(',')]

print(len(numbers))

import numpy as np


# # Part 1 - abs distance metric

def distance(x):
    return abs(np.array(numbers) - x).sum()


from scipy.optimize import minimize

sol = minimize(distance, np.mean(numbers))
sol

print("Part 1", distance(np.round(sol.x)))


# +
# Part 2 - quadratic cost + abs
# -

def cost(x):
    return (x**2 + x)/2


def distance(x):
    return cost(abs(np.array(numbers) - x)).sum()


sol = minimize(distance, np.mean(numbers))
sol

print("Part 2:", distance(np.round(sol.x)))

# Initially I got the rounding wrong and thought my approach was wrong, so I brute forced it:

x = np.arange(1, 500)

tries = [(xi, distance(xi)) for xi in x]

tries.sort(key=lambda i: i[1])

tries[0]
