from collections import defaultdict
from itertools import product

from aoc import solution
from aoc.parse import blocks
import numpy as np

debug = False
filename = "test.txt" if debug else "input.txt"

shapes = []

*shape_blocks, region_block = blocks(filename)

shapes = [np.array([list(l) for l in block[1:]]) == "#" for block in shape_blocks]

regions = []
for region_line in region_block:
    left, right = region_line.split(": ")
    width, height = map(int, left.split("x"))
    counts = tuple(int(g) for g in right.split(" "))

    regions.append((width, height, counts))


# Part 1
status = defaultdict(int)

for width, height, counts in regions:
    total_squares = width * height

    required_squares = sum(
        shape.astype(int).sum() * count for shape, count in zip(shapes, counts)
    )

    if required_squares > total_squares:
        status["too small"] += 1
        continue

    spots = (width // 3) * (height // 3)

    if spots >= sum(counts):
        status["enough to tile"] += 1
        continue

    status["not handled"] += 1

print(status)
solution(status["enough to tile"])

# Part 2
solution("dummy")
