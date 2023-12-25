import math

from matplotlib import pyplot as plt

from aoc import solution
import networkx as nx

debug = False
plot = False
filename = 'test.txt' if debug else 'input.txt'

graph = nx.Graph()

for line in open(filename):
    line = line.strip()
    source, targets = line.split(": ")
    targets = targets.split()

    for target in targets:
        graph.add_edge(source, target)


if plot:
    nx.draw(graph, with_labels=True)
    plt.show()

for edge in nx.minimum_edge_cut(graph):
    graph.remove_edge(*edge)

if plot:
    nx.draw(graph, with_labels=True)
    plt.show()

# Part 1
solution(
    math.prod(len(list(component)) for component in nx.connected_components(graph)))

# Part 2
solution('Press the red button')