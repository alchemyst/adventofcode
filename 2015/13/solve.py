from collections import defaultdict
from itertools import permutations

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

edgeweights = defaultdict(int)

def edge(a, b):
    if a < b:
        return (a, b)
    else:
        return (b, a)

nodes = set()

with open(filename) as f:
    for line in f:
        a, _, sign, happiness, *_, b = line.strip().strip('.').split()
        happiness = (1 if sign == 'gain' else -1) * int(happiness)
        edgeweights[edge(a, b)] += int(happiness)

        nodes.add(a)
        nodes.add(b)

def pathhappiness(path):
    return sum(edgeweights[edge(*e)] for e in zip(path, path[1:]))

def seat(first, rest):
    return max(
        pathhappiness([first, *perm, first])
        for perm in permutations(rest)
    )

# Part 1
firstnode = list(nodes)[0]
solution(seat(firstnode, nodes-{firstnode}))

# Part 2
nothing = "XXXXXXX"
solution( seat(nothing, nodes))