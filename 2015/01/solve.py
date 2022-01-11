import numpy as np

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    line = f.read().strip()


# Part 1
solution(line.count('(') - line.count(')'))

# Part 2
changes = np.array([1 if c == '(' else -1 for c in line])
diff = np.cumsum(changes)
index = (diff == -1).nonzero()[0][0] + 1

solution(index)