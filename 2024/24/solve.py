from aoc import solution
import pathlib
import networkx as nx
from operator import __or__, __and__, __xor__

WIRE_OPS = {
    "AND": __and__,
    "OR": __or__,
    "XOR": __xor__,
}

debug = False
filename = 'test.txt' if debug else 'input.txt'

wires_spec, connections_spec = pathlib.Path(filename).read_text().split("\n\n")

wires = {
    line.split(": ")[0]: int(line.split(": ")[1])
    for line in wires_spec.splitlines(keepends=False)
}

graph = nx.DiGraph()

for i1, op, i2, _, o in map(str.split, connections_spec.splitlines(keepends=False)):
    print(o)
    graph.add_node(o, operation=(i1, op, i2))
    graph.add_edge(i1, o)
    graph.add_edge(i2, o)

for wire in nx.topological_sort(graph):
    if wire in wires:
        continue
    print(wire)
    i1, op, i2 = graph.nodes[wire]["operation"]
    wires[wire] = WIRE_OPS[op](wires[i1], wires[i2])

def output_bits(wires):
    return sum(wires[wire]*2**i for i, wire in enumerate(sorted(w for w in wires if w.startswith('z')), 0))

# Part 1
solution(output_bits(wires))

# Part 2
solution('Dummy')