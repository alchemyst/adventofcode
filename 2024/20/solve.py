from collections import Counter

from aoc import solution
import aoc.array
import numpy as np
import networkx as nx
from itertools import combinations

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(aoc.array.read_board(filename))

start = np.array((board == 'S').nonzero()).flatten()
end = np.array((board == 'E').nonzero()).flatten()

if debug:
    aoc.print_board(board, type="s")

def board_graph(board):
    graph = nx.Graph()

    board = board == '#'

    for (i, j), value in np.ndenumerate(board):
        if value:
            continue
        for n_i, n_j in aoc.array.neighbours(board, i, j):
            nvalue = board[n_i, n_j]
            if nvalue:
                continue
            graph.add_edge((i, j), (n_i, n_j))

    return graph

# Part 1
def distance(a, b):
    return np.sum(np.abs(np.array(a) - np.array(b)))

graph = board_graph(board)

shortest_path = nx.shortest_path(graph, tuple(start), tuple(end))

def cheats(min_length, max_length, min_savings):
    s = 0
    for i, j in combinations(range(len(shortest_path)), 2):
        cheat_start = shortest_path[i]
        cheat_end = shortest_path[j]

        d = distance(cheat_start, cheat_end)
        if min_length <= d <= max_length:
            savings = j - i - d

            if savings >= min_savings:
                s += 1

    return s

solution(cheats(2, 2, 100))
# Part 2
solution(cheats(1, 20, 100))