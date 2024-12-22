import itertools
from dataclasses import dataclass
from itertools import pairwise
from textwrap import dedent
import networkx as nx
from functools import lru_cache

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.read().splitlines(keepends=False)

@dataclass
class Finger:
    moves: dict[tuple[str, str], str]
    position: str = 'A'

    def simulate(self, moves, start='A'):
        output = ''
        self.position = start
        for move in moves:
            if move == 'A':
                output += self.position
                continue

            key = (self.position, move)
            if key not in self.moves:
                raise ValueError(f'Invalid move: {key}')

            self.position = self.moves[key]

        return output

directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}
def keypad_to_moves(keypad: str):
    lines = keypad.strip("\n").split('\n')
    moves = {}
    for i, row in enumerate(lines):
        for j, key in enumerate(row):
            if key == ' ':
                continue
            for direction, delta in directions.items():
                new_i, new_j = i + delta[0], j + delta[1]
                if new_i < 0 or new_i >= len(lines) or new_j < 0 or new_j >= len(row) or lines[new_i][new_j] == ' ':
                    continue
                moves[(key, direction)] = lines[new_i][new_j]
    return moves


numeric = Finger(keypad_to_moves(dedent(
    """
    789
    456
    123
     0A
    """
)))

directional_moves = keypad_to_moves(dedent(
    """
     ^A
    <v>
    """
))

@dataclass
class Stack:
    fingers: list[Finger]

    def simulate(self, moves, starts):
        state = ''
        for finger, start in zip(self.fingers, starts):
            output = finger.simulate(moves, start)
            state += finger.position
            moves = output

        return output, state

# Part 1
stack = Stack([Finger(directional_moves), Finger(directional_moves), numeric])
# output = print(stack.simulate("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A", 'AAA'))

pad_types = [numeric, Finger(directional_moves)]

@lru_cache
def graph_from_finger(finger):
    graph = nx.DiGraph()
    for (start, move), end in pad_types[finger].moves.items():
        graph.add_edge(start, end, move=move)

    return graph

@lru_cache(maxsize=1000000)
def all_shortest_paths(finger, start, end):
    graph = graph_from_finger(finger)
    options = []
    for path in nx.all_shortest_paths(graph, start, end):
        output = (
            ''.join(
                graph[node1][node2]['move'] for node1, node2 in pairwise(path)
            )
            + "A"
        )
        options.append(output)

    return options


@lru_cache(maxsize=1000000)
def shortest(sequence, finger):

    outputs = []
    for start, end in pairwise("A" + sequence):
        outputs.append(all_shortest_paths(finger, start, end))

    return [''.join(combo) for combo in itertools.product(*outputs)]


def solve(stack_size):
    stack = [0] + [1]*stack_size
    s = 0
    for code in lines:
        sequences = [code.strip()]

        for finger in stack:
            new_sequences = set()
            for sequence in sequences:
                subsequences = [s + "A" for s in sequence.split("A")[:-1]]

                new_sequences.update(''.join(combo) for combo in itertools.product(*[shortest(subsequence, finger) for subsequence in subsequences]))


            min_len = min(len(s) for s in new_sequences)
            sequences = [s for s in new_sequences if len(s) == min_len]
            print(len(sequences))

        sequence = min(sequences, key=lambda x: len(x))
        complexity = len(sequence) * int(code[:-1])

        s += complexity

    return s

solution(solve(2))

# Part 2
solution('Dummy')