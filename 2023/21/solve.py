import numpy as np
from matplotlib import pyplot as plt

from aoc import solution
from aoc.array import read_board, neighbours

import pickle
import pathlib

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))
rows, cols = board.shape

start_i, start_j = (int(v[0]) for v in (board == 'S').nonzero())

board[start_i, start_j] = '.'

# Part 1
def reachable(i, j, steps):
    points = {(start_i, start_j)}
    for step in range(steps):
        new_points = set()
        for i, j in points:
            for new_i, new_j in neighbours(board, i, j):
                if board[new_i, new_j] == '.':
                    new_points.add((new_i, new_j))
        points = new_points

    return points

solution(len(reachable(start_i, start_j, 64)))

# Part 2
directions = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)

from tqdm.auto import tqdm


def reachable_mod(start_i, start_j, steps):
    points = {(start_i, start_j)}
    stepp = []
    lens = []
    for step in tqdm(range(steps)):
        new_points = set()
        for i, j in points:
            for di, dj in directions:
                new_i = i + di
                new_j = j + dj
                if board[new_i % rows, new_j % cols] == '.':
                    new_points.add((new_i, new_j))
        points = new_points

        stepp.append(step+1)
        lens.append(len(points))

    return stepp, lens

steps = 600

save_path = pathlib.Path(__file__).parent / f'save_{steps}.pickle'

if save_path.exists():
    stepp, lens = pickle.load(save_path.open('rb'))
else:
    stepp, lens = reachable_mod(start_i, start_j, steps)
    pickle.dump((stepp, lens), save_path.open('wb'))

assert rows == cols

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