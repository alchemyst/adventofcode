from aoc import solution
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from aoc.array import neighbours

debug = False
plot = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    board = np.array([list(line) for line in f.read().splitlines()])

g = nx.DiGraph()


def edge(board, i, j, ii, jj, g):
    here = board[i, j]
    there = board[ii, jj]
    ascent = ord(there) - ord(here)
    if ascent <= 1:
        g.add_edge((i, j), (ii, jj))


I, J = board.shape
S = tuple(int(i) for i in np.nonzero(board == 'S'))
E = tuple(int(i) for i in np.nonzero(board == 'E'))

board[S] = 'a'
board[E] = 'z'

for (i, j), v in np.ndenumerate(board):
    if plot:
        plt.text(j, I-i, v)
    for ii, jj in neighbours(board, i, j):
        edge(board, i, j, ii, jj, g)

path = nx.shortest_path(g, S, E)

if plot:
    path_plot = np.array(path).T
    plt.plot(path_plot[1, :], I - path_plot[0, :])
    plt.show()

# Part 1
solution(len(path)-1)

# Part 2
all_paths = []
for point in zip(*np.nonzero(board == 'a')):
    try:
        all_paths.append(nx.shortest_path(g, point, E))
    except nx.NetworkXNoPath:
        continue

path = min(all_paths, key=len)
solution(len(path) - 1)
