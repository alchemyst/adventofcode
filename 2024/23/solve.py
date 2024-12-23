import itertools

from aoc import solution
import networkx as nx

debug = False
filename = 'test.txt' if debug else 'input.txt'

graph = nx.Graph()

with open(filename) as f:
    for line in f:
        a, b = line.strip().split("-")
        graph.add_edge(a, b)

cliques = nx.enumerate_all_cliques(graph)

# Part 1
solution(sum(
    1
    for c in itertools.takewhile(lambda x: len(x) <= 3, cliques)
    if len(c) == 3 and any(computer.startswith('t') for computer in c)
))

# Part 2
max_clique = max(nx.find_cliques(graph), key=lambda x: len(x))
solution(','.join(sorted(max_clique)))