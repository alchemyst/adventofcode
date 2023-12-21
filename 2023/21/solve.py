from functools import cache

import numpy as np
from matplotlib import pyplot as plt

from aoc import solution
from aoc.array import read_board, neighbours

debug = True
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))
rows, cols = board.shape

start_i, start_j = (int(v[0]) for v in (board == 'S').nonzero())

board[start_i, start_j] = '.'

# Part 1
@cache
def reachable(i, j, steps):
    if steps == 0:
        return {(i, j)}

    result = set()
    for ni, nj in neighbours(board, i, j):
        if board[ni, nj] == '.':
            result.update(reachable(ni, nj, steps - 1))
    return result

# Part 2
directions = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)

reachable_cache = {}
def reachable_mod(i, j, steps):
    key = (i, j, steps)

    if key in reachable_cache:
        return reachable_cache[key]

    if steps == 0:
        result = {(i, j)}
    else:
        result = set()
        for di, dj in directions:
            new_i = i + di
            new_j = j + dj
            if board[new_i % rows, new_j % cols] == '.':
                result.update(reachable_mod(new_i, new_j, steps - 1))

    reachable_cache[key] = result
    return result

# from tqdm.auto import tqdm
#
# stepp = np.arange(30, 90+1)
# lens = []
# for steps in tqdm(stepp):
#     r = reachable_mod(start_i, start_j, steps)
#     lens.append(len(r))
#
#
# plt.semilogy(stepp[1:], np.diff(lens))
# plt.show()

r = reachable_mod(start_i, start_j, 50)

solution(len(r))