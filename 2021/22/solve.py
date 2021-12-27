from box import Box
from aoc import solution

debug = False
filename = 'test2.txt' if debug else 'input.txt'

def parse(filename):
    instructions = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            onoff, rest = line.split(maxsplit=1)
            numbers = []
            for pair in rest.split(','):
                rhs = pair.split('=')[1]
                parts = rhs.split('..')
                numbers += [int(p) for p in parts]

            instruction = (onoff, *numbers)
            instructions.append(instruction)

    # Convert to numbers and coordinates
    instructions = [
        (1 if onoff == 'on' else 0, xmin, xmax + 1, ymin, ymax + 1, zmin, zmax + 1)
        for onoff, xmin, xmax, ymin, ymax, zmin, zmax in instructions
    ]

    return instructions


def find_overlaps(current: Box, rest):
    overlaps = []
    for othervalue, *othercoords in rest:
        other = Box(*othercoords)
        for part in other.split(current):
            if part.inside(current):
                overlaps.append([othervalue, *part.coords()])
    return overlaps


def total_size(instructions):
    if not instructions:
        return 0
    instruction, *rest = instructions
    value, *coords = instruction
    current = Box(*coords)

    overlaps = find_overlaps(current, rest)

    return current.size() + total_size(rest) - total_size(overlaps)


def process(instructions):
    if not instructions:
        return 0

    instruction, *rest = instructions
    value, *coords = instruction
    current = Box(*coords)

    if value:
        overlaps = find_overlaps(current, rest)
        # print(overlaps)
        return current.size() - total_size(overlaps) + process(rest)
    else:
        return process(rest)


instructions = parse(filename)

initial_box = find_overlaps(Box(-50, 50, -50, 50, -50, 50), instructions)

solution(process(initial_box))

solution(process(instructions))
