import itertools
import pathlib
from operator import __or__, __and__, __xor__

import networkx as nx
from matplotlib import pyplot as plt

from aoc import solution

WIRE_OPS = {
    "AND": __and__,
    "OR": __or__,
    "XOR": __xor__,
}

WIRE_SHAPES = {
    "AND": "circle",
    "OR": "invtriangle",
    "XOR": "box",
}

debug = False
filename = "test.txt" if debug else "input.txt"

wires_spec, connections_spec = pathlib.Path(filename).read_text().split("\n\n")


def init():
    wires = {
        line.split(": ")[0]: int(line.split(": ")[1])
        for line in wires_spec.splitlines(keepends=False)
    }

    graph = nx.DiGraph()

    for i1, op, i2, _, o in map(str.split, connections_spec.splitlines(keepends=False)):
        graph.add_node(o, operation=op, shape=WIRE_SHAPES[op])
        graph.add_edge(i1, o)
        graph.add_edge(i2, o)

    return graph, wires


def evaluate(graph, wires):
    wires = wires.copy()
    for wire in nx.topological_sort(graph):
        if wire in wires:
            continue
        op = graph.nodes[wire]["operation"]
        wires[wire] = WIRE_OPS[op](*[wires[n] for n in graph.predecessors(wire)])

    return wires


def bit_values(wires, prefix):
    return [wires[wire] for wire in sorted(w for w in wires if w.startswith(prefix))]


def bits_to_int(bits):
    return sum(bit * 2**i for i, bit in enumerate(bits))


def output_bits(wires):
    return bits_to_int(bit_values(wires, "z"))


# Part 1
graph, wires = init()
solution(output_bits(evaluate(graph, wires)))

# Part 2
# basic scheme: the machine is supposed to add x?? bits and y?? bits to get z?? bits
# x00 and y00 should only affect z00 and z01 (with carry)

def xx(lsb):
    return f"x{lsb:02}"


def yy(lsb):
    return f"y{lsb:02}"


def zz(lsb):
    return f"z{lsb:02}"


def swap(graph, o1, o2):
    new_graph = graph.copy()

    pred_1 = list(new_graph.predecessors(o1))
    pred_2 = list(new_graph.predecessors(o2))

    op1 = new_graph.nodes[o1]["operation"]
    op2 = new_graph.nodes[o2]["operation"]

    for n in pred_1:
        new_graph.remove_edge(n, o1)
    for n in pred_2:
        new_graph.remove_edge(n, o2)

    for n in pred_1:
        new_graph.add_edge(n, o2)
    for n in pred_2:
        new_graph.add_edge(n, o1)

    new_graph.nodes[o1]["operation"] = op2
    new_graph.nodes[o1]["shape"] = WIRE_SHAPES[op2]
    new_graph.nodes[o2]["operation"] = op1
    new_graph.nodes[o2]["shape"] = WIRE_SHAPES[op1]

    return new_graph


def apply_swaps(graph, swaps):
    new_graph = graph.copy()
    for a, b in swaps:
        new_graph = swap(new_graph, a, b)

    return new_graph


def subgraph_for_lsb(graph, lsb):
    return nx.subgraph(
        graph,
        set(nx.ancestors(graph, zz(lsb)))
        | set(nx.ancestors(graph, zz(lsb + 1)))
        | {zz(lsb), zz(lsb + 1)},
    )


def correct(graph, lsb):
    subgraph = subgraph_for_lsb(graph, lsb)

    inputs = {n for n, d in subgraph.in_degree() if d == 0}
    allowed_inputs = {xx(lsb), yy(lsb), xx(lsb + 1), yy(lsb + 1)}

    if inputs != allowed_inputs:
        return False

    all_correct = True
    for x, y in itertools.product([0, 1], repeat=2):
        wires = {
            xx(lsb): x,
            yy(lsb): y,
            xx(lsb + 1): 0,
            yy(lsb + 1): 0,
        }

        output = evaluate(subgraph, wires)

        all_correct = (
            all_correct
            and output[zz(lsb + 1)] == (x & y)
            and output[zz(lsb)] == (x ^ y)
        )
    return all_correct

def output_wires(graph):
    return {n for n, d in graph.in_degree() if d > 0}

nodes = list(graph.nodes)
ys = sorted(n for n in nodes if n.startswith("y"))
xs = sorted(n for n in nodes if n.startswith("x"))
zs = sorted(n for n in nodes if n.startswith("z"))

swap_list = ["z08", "z22", "z31", "jdr", "ffj", "gjh", "kfm", "dwp", ]

swaps = [
    ("z08", "ffj"),
    ("z22", "gjh"),
    ("z31", "jdr"),
    ("kfm", "dwp"),
]

# graph = apply_swaps(graph, swaps)

operations = nx.get_node_attributes(graph, "operation")

print("Bad outputs:")
for z in zs:
    if operations[z] != 'XOR' and z != "z45":
        print(z, operations[z])

print("bad XOR:")
for n, operation in operations.items():
    if operation == 'XOR' and not n.startswith("z"):
        if not all(p[0] in 'xy' for p in graph.predecessors(n)):
            print(n)

print("bad AND/or:")
for n, operation in operations.items():
    if operation == "OR" and not n == "z00":
        for p in graph.predecessors(n):
            if operations[p] != "AND":
                print(p)

for lsb in range(0, int(max(xs)[1:]) + 1):
    print(lsb, correct(graph, lsb))

pathlib.Path("graph.dot").write_text(
    nx.drawing.nx_pydot.to_pydot(graph).to_string()
)
#
# print("{rank=same; %s}" % "; ".join(zs))

print(','.join(sorted(swap_list)))