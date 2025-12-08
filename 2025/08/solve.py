from math import prod

from aoc import solution
import numpy as np
import scipy.spatial as ssp
import networkx as nx

debug = False
filename = "test.txt" if debug else "input.txt"
limit = 10 if debug else 1000

positions_list = []
with open(filename) as f:
    for line in f:
        positions_list.append(list(map(int, line.strip().split(","))))

positions = np.array(positions_list)

distance = ssp.distance.pdist(positions, metric="euclidean")
distance_matrix = ssp.distance.squareform(distance)
order = np.argsort(distance)

graph = nx.Graph()
for o in order[:limit]:
    boxes = ssp.distance._row_col()
    graph.add_edge(boxes[0], boxes[1])

sizes = list(len(c) for c in nx.connected_components(graph))
sizes.sort()

# Part 1
solution(prod(sizes[-3:]))

# Part 2
graph = nx.Graph()

for i in range(len(positions)):
    graph.add_node(i)

for o in order:
    boxes = tuple((distance_matrix == distance[o]).nonzero()[0])
    graph.add_edge(boxes[0], boxes[1])

    if nx.is_connected(graph):
        break

solution(prod(positions[boxes, 0]))
