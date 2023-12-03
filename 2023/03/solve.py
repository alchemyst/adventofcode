import scipy as sc

from aoc import solution
from aoc.array import read_board, neighbours

import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))

digits = np.zeros_like(board, dtype=bool)
for d in range(10):
    digits |= board == str(d)

periods = board == '.'

symbols = ~(digits | periods)

k = np.ones((3, 3))

neighbourhood = sc.signal.convolve2d(symbols, k, mode='same') >= 1

numbers, _ = sc.ndimage.label(digits, structure=[[0, 0, 0], [1, 1, 1], [0, 0, 0]])

numbers_parsed = {}

s = 0
for group in np.unique(numbers[neighbourhood & (numbers != 0)]):
    n = numbers_parsed[group] = int(''.join(board[numbers == group]))
    s += n

# Part 1
solution(s)

# Part 2

gears = board == '*'

s = 0
for i, j in zip(*np.nonzero(gears)):
    groups = set(neighbours(numbers, i, j, diag=True, values=True)) - {0}
    if len(groups) == 2:
        s += np.prod([numbers_parsed[group] for group in groups])

solution(s)