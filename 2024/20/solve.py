from collections import Counter

from aoc import solution
import aoc.array
import numpy as np
import networkx as nx
import scipy.ndimage as sci

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

def board_with_cheat(board, cheat1, cheat2):
    new_board = board.copy()
    new_board[cheat1] = '.'
    new_board[cheat2] = '.'

    return new_board

def shortest_path(board, start, end):
    graph = board_graph(board)
    return nx.shortest_path_length(graph, tuple(start), tuple(end))

# Part 1
counter = Counter()

original_shortest = shortest_path(board, start, end)
print(original_shortest)

walls = board == '#'
opens = (~walls).astype(int)
simple_walls = (
        walls & (
        (sci.convolve(opens, [[1, 0, 1]]) == 2)
        | (sci.convolve(opens, [[1], [0], [1]]) == 2)
    )
)

aoc.print_board(simple_walls, type='d')

wall_i, wall_j = np.where(simple_walls)
print(len(wall_i))
s = 0
for ii, cheat in enumerate(zip(wall_i, wall_j)):
    print(ii)
    shortest_with_cheat = shortest_path(board_with_cheat(board, cheat, cheat), start, end)
    savings = original_shortest - shortest_with_cheat

    counter[savings] += 1

    if savings >= 100:
        s += 1

print(sorted(counter.most_common()))

solution(s)

# Part 2
solution('Dummy')