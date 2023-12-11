from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.path import Path

from aoc import solution
from aoc.array import read_board
from aoc.display import print_board

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))

if debug: print_board(board, type='s')

start = tuple(int(i[0]) for i in (np.array(board) == 'S').nonzero())

# using (row, col)
north = (-1, 0)
south = (1, 0)
east = (0, 1)
west = (0, -1)

connections = {
    '|': (north, south),
    '-': (east, west),
    'L': (north, east),
    'J': (north, west),
    '7': (south, west),
    'F': (south, east),
}


def add(self, other):
    return tuple(s + o for s, o in zip(self, other))


def connectivity(board):
    # build the connectivity graph

    edge_count = defaultdict(int)
    for this_ij, value in np.ndenumerate(board):
        for delta_ij in connections.get(value, ()):
            implied_edge = (this_ij, add(this_ij, delta_ij))
            edge_count[tuple(sorted(implied_edge))] += 1

    graph = nx.Graph()
    for edge, count in edge_count.items():
        if count == 2:
            graph.add_edge(*edge)

    return graph

# Idea: instead of trying all the kinds of connections
# try the ones that can connect to exactly two neighbours
for connection in connections:
    newboard = board.copy()
    newboard[start] = connection
    graph = connectivity(newboard)
    if debug:
        nx.draw(graph)
        plt.show()

    try:
        cycle = nx.find_cycle(graph, start)
        break
    except:
        continue


# Part 1
solution(int(len(cycle)/2))

# Part 2
candidates = np.ones_like(board, dtype=bool)
for node1, node2 in cycle:
    candidates[node1] = 0
    candidates[node2] = 0

cycle_path = Path([c for c, _ in cycle], closed=True)

for candidate_point in zip(*candidates.nonzero()):
    if not cycle_path.contains_point(candidate_point):
        candidates[candidate_point] = False

if debug:
    plt.imshow(candidates)
    plt.show()

solution(candidates.sum())
