import math
from functools import cache

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

state_cache = {}

def steps_to_next_z(node, instruction):
    key = (node, instruction)
    if key in state_cache:
        return state_cache[key]

    keys = [key]
    steps = 0
    while True:
        node = nodes[node][lr_instructions[instruction]]
        instruction = (instruction + 1) % len(lr_instructions)
        steps += 1
        key = (node, instruction)
        if key in state_cache:
            # fast-forward to solution state
            node, instruction, extra_steps = state_cache[key]
            steps += extra_steps

        if node.endswith("Z"):
            solution = node, instruction, steps
            for i, visited_key in enumerate(keys):
                state_cache[visited_key] = node, instruction, steps - i
            return solution
        keys.append(key)


states = [(n, 0, 0) for n in nodes if n.endswith('A')]

for i in range(10):
    steps = [state[2] for state in states]
    max_steps = max(steps)
    if max_steps > 0 and all(step == max_steps for step in steps):
        break

    for position, (node, instruction, steps) in enumerate(states):
        if max_steps > 0 and steps == max_steps:
            continue
        node, instruction, extra_steps = steps_to_next_z(node, instruction)
        states[position] = (node, instruction, steps + extra_steps)

cycle_times = []

for node, instruction, steps in states:
    _, _, cycle_time = steps_to_next_z(node, instruction)
    cycle_times.append(cycle_time)

solution(math.lcm(*cycle_times))