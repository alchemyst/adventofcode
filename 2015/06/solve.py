from collections import namedtuple

import numpy as np
import re

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

Instruction = namedtuple('Instruction', ['action', 'r1', 'c1', 'r2', 'c2'])

instructions = []

instruction_re = re.compile(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')

with open(filename) as f:
    for line in f:
        m = instruction_re.match(line)
        if m:
            instructions.append(Instruction(m.group(1), *map(int, m.groups()[1:])))

# Part 1
lights = np.zeros((1000, 1000), dtype=bool)
for instruction in instructions:
    match instruction:
        case Instruction('turn on', r1, c1, r2, c2):
            lights[r1:r2+1, c1:c2+1] = True
        case Instruction('turn off', r1, c1, r2, c2):
            lights[r1:r2+1, c1:c2+1] = False
        case Instruction('toggle', r1, c1, r2, c2):
            lights[r1:r2+1, c1:c2+1] = ~lights[r1:r2+1, c1:c2+1]

solution(lights.sum())

# Part 2
lights = np.zeros((1000, 1000), dtype=int)
for instruction in instructions:
    match instruction:
        case Instruction('turn on', r1, c1, r2, c2):
            lights[r1:r2+1, c1:c2+1] += 1
        case Instruction('turn off', r1, c1, r2, c2):
            lights[r1:r2+1, c1:c2+1] -= 1
        case Instruction('toggle', r1, c1, r2, c2):
            lights[r1:r2+1, c1:c2+1] += 2
    lights[lights < 0] = 0

solution(lights.sum())
