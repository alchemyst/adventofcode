from aoc import solution
from aoc.array import read_board
import numpy as np
import scipy.spatial as spatial

debug = False
filename = 'test.txt' if debug else 'input.txt'

def expand(board):
    rows = []
    for row in board:
        rows.append(row)
        if all(row == '.'):
            rows.append(row)
    return np.array(rows)


board = np.array(read_board(filename))
expanded = expand(expand(board.T).T)
nodes = np.array((expanded == '#').nonzero()).T
distances = spatial.distance_matrix(nodes, nodes, p=1)

# Part 1
solution(np.tril(distances).sum().astype(int))

# Part 2
factor = 1000000 - 1
nodes = np.array((board == '#').nonzero()).T
# expand out rows:
row_expansion = (board == '.').all(axis=1).cumsum()*factor
column_expansion = (board == '.').all(axis=0).cumsum()*factor
row_coords = nodes[:, 0]
column_coords = nodes[:, 1]

nodes[:, 0] += row_expansion[row_coords]
nodes[:, 1] += column_expansion[column_coords]

distances = spatial.distance_matrix(nodes, nodes, p=1)

solution(np.tril(distances).sum())