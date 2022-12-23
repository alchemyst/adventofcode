from collections import defaultdict
from itertools import count

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

N = complex(0, 1)
S = complex(0, -1)
E = complex(1, 0)
W = complex(-1, 0)

NE = N + E
NW = N + W

SE = S + E
SW = S + W

def load_elves(filename):
    elves = []
    with open(filename) as f:
        for s, line in enumerate(f):
            for e, char in enumerate(line.strip()):
                if char == ".":
                    continue
                elf = complex(e, -s)
                elves.append(elf)

    order = (
        ((N, NE, NW), N),
        ((S, SE, SW), S),
        ((W, NW, SW), W),
        ((E, NE, SE), E),
    )

    return elves, order


def round(elves, order):
    occupied = defaultdict(bool)
    for elf in elves:
        occupied[elf] = True

    checks = (
        ((N, S, E, W, NE, NW, SE, SW), 0),
    ) + order

    proposals = []
    propcount = defaultdict(int)
    for elf in elves:
        proposal = 0
        for directions, prop in checks:
            if not any(occupied[elf + d] for d in directions):
                proposal = prop
                break
        proposals.append(proposal)
        propcount[elf + proposal] += 1

    moved = False
    return_elves = []
    for elf, proposal in zip(elves, proposals):
        if propcount[elf + proposal] <= 1:
            return_elves.append(elf + proposal)
            moved |= abs(proposal) > 0
        else:
            return_elves.append(elf)

    return moved, return_elves, order[1:] + order[:1]


def open_blocks(elves):
    reals = [e.real for e in elves]
    imags = [e.imag for e in elves]

    width = max(reals) - min(reals) + 1
    height = max(imags) - min(imags) + 1
    area = width * height

    return area - len(elves)


# Part 1
elves, order = load_elves(filename)

for _ in range(10):
    moved, elves, order = round(elves, order)

solution(open_blocks(elves))

# Part 2
elves, order = load_elves(filename)

for rounds in count(1):
    moved, elves, order = round(elves, order)
    if not moved:
        break

solution(rounds)