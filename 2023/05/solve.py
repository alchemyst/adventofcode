import re

from aoc import solution
from more_itertools import chunked

debug = False
filename = 'test.txt' if debug else 'input.txt'

numbers = re.compile('[0-9]+')
mapline = re.compile('(.*)-to-(.*) map:')

def all_numbers(line):
    return tuple(int(n) for n in numbers.findall(line))

with open(filename) as f:
    lines = f.read().splitlines()

    seeds = all_numbers(lines[0])

    maps = {}
    targets = {}
    sources = {}
    for line in lines[2:]:
        if m := mapline.match(line):
            source, target = m.groups()
            maps[source] = []
            targets[source] = target
            sources[target] = source
            continue

        if n := all_numbers(line):
            maps[source].append(n)

def follow_map(n, source):
    next_destination = targets[source]

    for target_start, source_start, length in maps[source]:
        if source_start <= n < source_start + length:
            return target_start + (n - source_start), next_destination

    return n, next_destination

# TODO: this is really ugly, find a way to generalise
def follow_map_backwards(n, target):
    next_destination = sources[target]

    for target_start, source_start, length in maps[next_destination]:
        if target_start <= n < target_start + length:
            return source_start + (n - target_start), next_destination

    return n, next_destination


def follow(n, start, end, follow_func):
    step = start
    while step != end:
        n, step = follow_func(n, step)

    return n

# Part 1
solution(min(follow(n, "seed", "location", follow_map) for n in seeds))

# Part 2
# Intuition: just check the edges of the maps - places where maps start
# start out with the bottom of each seed range
edges = set(seeds[::2])

for target, source in sources.items():
    for target_start, source_start, length in maps[source]:
        edges.add(follow(source_start, source, "seed", follow_map_backwards))

# Remove edges outside the allowed seed ranges
edges = {e for e in edges if any(start <= e < start+length for start, length in chunked(seeds, 2))}
locations = [follow(n, "seed", "location", follow_map) for n in edges]
solution(min(locations))
