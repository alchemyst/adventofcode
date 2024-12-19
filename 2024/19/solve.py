from functools import lru_cache

from aoc import solution
import pathlib

debug = False
filename = pathlib.Path('test.txt' if debug else 'input.txt')

patterns, designs = filename.read_text().split("\n\n")
patterns = patterns.split(", ")
designs = designs.split("\n")

@lru_cache
def matches(patterns, design):
    subset = tuple(p for p in patterns if p in design)
    if not subset:
        return 0

    ways = 0
    for p in subset:
        if design == p:
            ways += 1
        if design.startswith(p):
            ways += matches(subset, design[len(p):])

    return ways


working = 0
total_ways = 0
for design in designs:
    ways = matches(tuple(patterns), design)
    if debug:
        print(design, ways)
    working += bool(ways)
    total_ways += ways

# Part 1
solution(working)

# Part 2
solution(total_ways)