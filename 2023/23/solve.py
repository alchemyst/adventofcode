import networkx as nx
import numpy as np

from aoc import solution
from aoc.array import read_board, neighbours

debug = False
plot = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))

start = (0, 1)
end = (len(board) - 1, len(board) - 2)

slopes = {
    '<': (0, -1),
    '>': (0, 1),
    'v': (1, 0),
    '^': (-1, 0),
}

# Part 1
graph = nx.DiGraph()

for this, b in np.ndenumerate(board):
    if b == "#":
        continue
    elif b in slopes:
        i, j = this
        di, dj = slopes[b]
        other = i + di, j + dj
        if board[other] != '#':
            graph.add_edge(this, other)
    elif b == '.':
        for other in neighbours(board, *this):
            bo = board[other]
            if bo == "#":
                continue
            elif bo == ".":
                graph.add_edge(this, other)
                graph.add_edge(other, this)
            elif bo in slopes:
                oi, oj = other
                di, dj = slopes[bo]
                down_slope = oi + di, oj + dj
                if this != down_slope:
                    graph.add_edge(this, other)


solution(max(nx.path_weight(graph, path, 'weight') for path in nx.all_simple_paths(graph, start, end)))

# Part 2
graph = nx.Graph()

for this, b in np.ndenumerate(board):
    if b == "#":
        continue
    elif b == '.':
        for other in neighbours(board, *this):
            bo = board[other]
            if bo == "#":
                continue

            graph.add_edge(this, other, weight=1)

# simplify graph:
# remove nodes with degree 2, replace with edge with sums of incoming edge weights
print("Edges before:", len(graph.edges))
running = True
while running:
    running = False
    for node in list(graph.nodes):
        if graph.degree(node) == 2:
            neighbours = list(graph.neighbors(node))
            u, v = neighbours
            graph.add_edge(u, v, weight=graph[u][node]['weight'] + graph[node][v]['weight'])
            graph.remove_node(node)
            modified = True

print("Edges after:", len(graph.edges))

solution(max(nx.path_weight(graph, path, 'weight') for path in nx.all_simple_paths(graph, start, end)))
