from aoc import solution
from aoc.array import read_board
from aoc.display import print_board
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

debug = False
filename = 'test3.txt' if debug else 'input.txt'

board = np.array(read_board(filename))

if debug: print_board(board, type='s')

start = tuple(int(i[0]) for i in (np.array(board) == 'S').nonzero())

# using (row, col)
directions = {
    'north': (-1, 0),
    'south': (1, 0),
    'east': (0, 1),
    'west': (0, -1),
}

#| is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

connections = {
    '|': {'north', 'south'},
    '-': {'east', 'west'},
    'L': {'north', 'east'},
    'J': {'north', 'west'},
    '7': {'south', 'west'},
    'F': {'south', 'east'},
}

links = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east',
}

matches = {
    (-1, 0): ('north', 'south'),
    (1, 0): ('south', 'north'),
    (0, 1): ('east', 'west'),
    (0, -1): ('west', 'east'),
}

def add(self, other):
    return tuple(s + o for s, o in zip(self, other))


def connectivity(board):
    # build the connectivity graph
    graph = nx.Graph()
    for this_ij, value in np.ndenumerate(board):
        for delta_ij in matches:
            other_ij = add(this_ij, delta_ij)
            if any(i < 0 for i in other_ij):
                continue
            try:
                other_value = str(board[other_ij])
            except:
                continue

            this_connections = connections.get(value, set())
            other_connections = connections.get(other_value, set())
            mine, theirs = matches[delta_ij]
            if mine not in this_connections or theirs not in other_connections:
                continue

            graph.add_edge(this_ij, other_ij)

    return graph

for connection in connections:
    newboard = board.copy()
    newboard[start] = connection
    graph = connectivity(newboard)

    if False and debug:
        nx.draw(graph)
        plt.show()

    try:
        cycle = nx.find_cycle(graph, start)
    except:
        continue


# Part 1
solution(len(cycle)/2)

# Part 2
candidates = np.ones_like(board, dtype=bool)
for node1, node2 in cycle:
    candidates[node1] = 0
    candidates[node2] = 0

from matplotlib.path import Path

cycle_path = Path([c for c, _ in cycle], closed=True)

for candidate_point in zip(*candidates.nonzero()):
    if not cycle_path.contains_point(candidate_point):
        candidates[candidate_point] = False

if debug:
    plt.imshow(candidates)
    plt.show()

solution(candidates.sum())
