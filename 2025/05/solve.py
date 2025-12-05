from itertools import pairwise

from aoc import solution
from aoc.solution_patterns import sum_every

debug = False
filename = "test.txt" if debug else "input.txt"

with open(filename) as f:
    lines = iter(f.read().splitlines(keepends=False))

    fresh_ranges = []
    for line in lines:
        if not line:
            break

        fresh_ranges.append(list(map(int, line.split("-"))))

    available_ingredients = []
    for line in lines:
        available_ingredients.append(int(line))


# Part 1
def fresh(ingredient):
    return any(start <= ingredient <= end for start, end in fresh_ranges)


if debug:
    print(fresh_ranges)
    print(available_ingredients)

solution(sum_every(fresh, available_ingredients))

# Part 2
points = []

for left, right in fresh_ranges:
    points.append((left, 1))
    points.append((right + 1, -1))

points.sort()

c = 0
valid = 0
for (v1, c1), (v2, c2) in pairwise(points):
    c += c1

    if c > 0:
        valid += v2 - v1

solution(valid)
