import numpy as np
import scipy.ndimage as ndi

from aoc import solution
from aoc.array import read_board

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))
rows, cols = board.shape

start_i, start_j = (int(v[0]) for v in (board == 'S').nonzero())

board[start_i, start_j] = '.'

# Part 1
def reachable(board, i, j, steps):
    garden = board == '.'
    visited = np.zeros_like(board, dtype=bool)
    visited[i, j] = True
    region = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool)

    stepp = np.arange(1, steps+1)
    lens = []
    for _ in stepp:
        ndi.convolve(visited, region, output=visited, mode='constant', cval=0)
        visited &= garden
        lens.append(visited.sum())

    return stepp, lens


stepp, lens = reachable(board, start_i, start_j, 64)
solution(lens[-1])

# Part 2
assert rows == cols

steps = 600
boards_needed = (steps - rows//2)//rows*2 + 1

big_board = np.tile(board, (boards_needed, boards_needed))

stepp, lens = reachable(big_board, start_i + rows*(boards_needed//2), start_j + rows*(boards_needed//2), steps)

width = rows

target = 26501365

# The repeats follow a quadratic, which looks close enough with numerical methods
start = target % width - 1
x = stepp[start::width]
y = lens[start::width]

# Notice that the second differences are constant
diffs = np.diff(y, 2)
assert len(np.unique(diffs)) == 1

# Fit
poly = np.polyfit(x, y, 2)
pred = np.polyval(poly, stepp[start::width])

# predict
solution(int(np.polyval(poly, target)))