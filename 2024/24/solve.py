from aoc import solution
import pathlib
import graphlib
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

graph = graphlib.TopologicalSorter()

operations = {}

for i1, op, i2, _, o in map(str.split, connections_spec.splitlines(keepends=False)):
    operations[o] = (i1, op, i2)
    graph.add(o, i1, i2)

for wire in graph.static_order():
    if wire in wires:
        continue
    print(wire)
    i1, op, i2 = operations[wire]
    wires[wire] = WIRE_OPS[op](wires[i1], wires[i2])

def output_bits(wires):
    return sum(wires[wire]*2**i for i, wire in enumerate(sorted(w for w in wires if w.startswith('z')), 0))

# Part 1
solution(output_bits(wires))

# Part 2
solution('Dummy')