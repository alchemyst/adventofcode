from aoc import solution
from aoc.array import read_board
import numpy as np
import scipy.spatial as spatial

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))


def solve(factor):
    nodes = np.array((board == '#').nonzero()).T

    for axis in (0, 1):
        expansion = (board == '.').all(axis=axis).cumsum()*factor
        coords = nodes[:, 1-axis]
        coords += expansion[coords]

    distances = spatial.distance_matrix(nodes, nodes, p=1)
    return int(np.tril(distances).sum())


# Part 1
solution(solve(1))

# Part 2

solution(solve(1000000 - 1))