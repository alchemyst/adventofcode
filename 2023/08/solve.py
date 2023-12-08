import math

from aoc import solution
import parse
from itertools import cycle, count

debug = False
filename = 'test.txt' if debug else 'input.txt'

node_pattern = parse.compile('{} = ({}, {})')

def read_nodes(filename):
    nodes = {}

    with open(filename) as f:
        lr_instructions = next(f).strip()
        next(f)
        for line in f:
            node, left, right = node_pattern.parse(line.strip())
            nodes[node] = {"L": left, "R": right}

    return nodes, lr_instructions

nodes, lr_instructions = read_nodes(filename)

# Part 1
location = 'AAA'
for n, direction in enumerate(cycle(lr_instructions), 1):
    location = nodes[location][direction]

    if location == 'ZZZ':
        break

solution(n)

# Part 2
filename = 'test2.txt' if debug else 'input.txt'
nodes, lr_instructions = read_nodes(filename)


def steps_to_next_z(node, instructions):
    for steps, instruction in enumerate(instructions, 1):
        node = nodes[node][instruction]

        if node.endswith("Z"):
            return node, instructions, steps


states = [(n, cycle(lr_instructions), 0) for n in nodes if n.endswith('A')]

# settle into a cycle
for _ in range(3):
    for position, (node, instruction, steps) in enumerate(states):
        node, instruction, extra_steps = steps_to_next_z(node, instruction)
        states[position] = (node, instruction, steps + extra_steps)

cycle_times = []
for node, instruction, steps in states:
    _, _, cycle_time = steps_to_next_z(node, instruction)
    cycle_times.append(cycle_time)

solution(math.lcm(*cycle_times))