import itertools
from collections import defaultdict
from functools import lru_cache
from itertools import pairwise
from textwrap import dedent
import networkx as nx

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.read().splitlines(keepends=False)

directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

def graph_from_keypad(keypad: str):
    lines = dedent(keypad).strip("\n").split('\n')

    graph = nx.DiGraph()
    for i, row in enumerate(lines):
        for j, key in enumerate(row):
            if key == ' ':
                continue
            for direction, delta in directions.items():
                other_i, other_j = i + delta[0], j + delta[1]
                if 0 <= other_i < len(lines) and 0 <= other_j < len(row):
                    other_key = lines[other_i][other_j]
                    if other_key == ' ':
                        continue

                    graph.add_edge(key, other_key, direction=direction)

    return graph

numeric = graph_from_keypad(
    """
    789
    456
    123
     0A
    """
)

directional = graph_from_keypad(
    """
     ^A
    <v>
    """
)

moves = defaultdict(list)

for i, graph in enumerate([numeric, directional]):
    for start, end in itertools.product(graph.nodes, repeat=2):
        for path in nx.all_shortest_paths(graph, start, end):
            move = ''.join(graph[path_a][path_b]["direction"] for path_a, path_b in pairwise(path)) + 'A'
            moves[start, end].append(move)
        if start == end:
            moves[start, end] = ["A"]

@lru_cache
def shortest_path(code, depth):
    length = 0
    for start, end in pairwise("A" + code):
        if depth == 0:
            length += len(moves[start, end][0])
        else:
            length += min(
                shortest_path(move, depth - 1) for move in moves[start, end]
            )

    return length


def solve(depth):
    return sum(
        shortest_path(code, depth)*int(code[:3])
        for code in lines
    )

solution(solve(2))

# Part 2
solution(solve(25))