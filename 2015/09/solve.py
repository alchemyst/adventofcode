from aoc import solution
import networkx
import networkx.algorithms.approximation

from parse import compile

debug = False
filename = 'test.txt' if debug else 'input.txt'

graph = networkx.Graph()
parser = compile('{} to {} = {:d}')
with open(filename) as f:
    for line in f:
        if (m := parser.parse(line.strip())):
            graph.add_edge(m[0], m[1], weight=m[2])


def path_finder(graph, path_so_far, agg):
    remaining_nodes = set(graph.nodes) - set(path_so_far)
    if not remaining_nodes:
        return networkx.path_weight(graph, path_so_far, 'weight')

    return agg(path_finder(graph, path_so_far + [node], agg) for node in remaining_nodes)


# Part 1
solution(path_finder(graph, [], agg=min))

# Part 2
solution(path_finder(graph, [], agg=max))