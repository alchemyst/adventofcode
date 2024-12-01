from aoc import solution
from collections import Counter
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

numbers = np.loadtxt(filename, dtype=int)
lefts = np.sort(numbers[:, 0])
rights = np.sort(numbers[:, 1])

# Part 1
solution(np.abs(lefts - rights).sum())

# Part 2
right_counts = Counter(rights)
solution(sum(right_counts[left] * left for left in lefts))
