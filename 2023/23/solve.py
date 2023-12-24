from functools import cache

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


def longest_path(start, end):
    return max(nx.path_weight(graph, path, 'weight') for path in nx.all_simple_paths(graph, start, end))


@cache
def longest_path2(start, end, seen=()):
    if start == end:
        return 0

    return max(
        (
            longest_path2(other, end, tuple(sorted(seen + (other,)))) + graph[start][other]['weight']
            for other in graph.neighbors(start)
            if other not in seen
        )
        ,
        default=0
    )


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
            graph.add_edge(this, other, weight=1)
    elif b == '.':
        for other in neighbours(board, *this):
            bo = board[other]
            if bo == "#":
                continue
            elif bo == ".":
                graph.add_edge(this, other, weight=1)
                graph.add_edge(other, this, weight=1)
            elif bo in slopes:
                oi, oj = other
                di, dj = slopes[bo]
                down_slope = oi + di, oj + dj
                if this != down_slope:
                    graph.add_edge(this, other, weight=1)


# remove nodes in a chain, replace with edge with sums of incoming edge weights
print("Nodes before:", len(graph.nodes))
running = True
while running:
    running = False
    for node in list(graph.nodes):
        if graph.degree(node) != 4:
            continue

        linked = list(graph.neighbors(node))
        if len(linked) != 2:
            continue

        u, v = linked
        weight = graph[node][u]['weight'] + graph[node][v]['weight']
        graph.add_edge(u, v, weight=weight)
        graph.add_edge(v, u, weight=weight)
        graph.remove_node(node)
        running = True

print("Nodes after:", len(graph.nodes))


solution(longest_path2(start, end))

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
print("Nodes before:", len(graph.nodes))
running = True
while running:
    running = False
    for node in list(graph.nodes):
        if graph.degree(node) == 2:
            neighbours = list(graph.neighbors(node))
            u, v = neighbours
            graph.add_edge(u, v, weight=graph[node][u]['weight'] + graph[node][v]['weight'])
            graph.remove_node(node)
            running = True

print("Nodes after:", len(graph.nodes))

longest_path2.cache_clear()
solution(longest_path2(start, end))
