from aoc import solution
import aoc.array
import networkx as nx
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(aoc.array.read_board(filename, int))

if debug:
    aoc.print_board(board)

graph = nx.DiGraph()

for (i, j), from_value in np.ndenumerate(board):
    for ni, nj in aoc.array.neighbours(board, i, j):
        to_value = board[ni, nj]
        if from_value == to_value - 1:
            graph.add_edge((i, j), (ni, nj))

# Part 1
# First part is just about reachability, but the statement contains "as long as possible"
# which suggests that we need to find the longest path between any two trailheads eventually

heads = np.where(board == 0)
tops = np.where(board == 9)

s = 0
for hi, hj in zip(*heads):
    for ti, tj in zip(*tops):
        if nx.has_path(graph, (hi, hj), (ti, tj)):
            s += 1

solution(s)

# Part 2
s = 0
for hi, hj in zip(*heads):
    for ti, tj in zip(*tops):
        lengths = [len(path) for path in nx.all_simple_paths(graph, (hi, hj), (ti, tj))]
        if not lengths:
            continue
        maxlength = max(lengths)
        s += sum(1 for length in lengths if length == maxlength)

solution(s)