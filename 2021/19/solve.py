import itertools

import numpy as np

from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

scanners = []

with open(filename) as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        if line.startswith("--"):
            scanner = []
            scanners.append(scanner)
            continue

        scanner.append([int(n) for n in line.split(",")])

scanners = [np.array(scanner) for scanner in scanners]


def rotate(scanner, rot):
    order, signs = rot
    return scanner[:, order] * np.array(signs)


def rotations(scanner):
    # We could go twice as fast if we didn't generate 48 rotatoins instead of 24
    for order in itertools.permutations(range(0, 3), 3):
        for signs in itertools.product([-1, 1], repeat=3):
            rot = order, signs
            yield rotate(scanner, rot)


def unique_points(scanner):
    return set(tuple(point) for point in scanner)


def overlaps(apoints, bb):
    for b in rotations(bb):
        for apoint in apoints:
            for bpoint in b:
                delta = apoint - bpoint
                upoints = unique_points(b + delta)
                common_points = apoints.intersection(upoints)

                if len(common_points) >= 12:
                    return True, delta, upoints

    return False, None, None


allpoints = unique_points(scanners.pop(0))
deltas = []
while scanners:
    print("Scanners to go:", len(scanners))
    scanner = scanners.pop(0)
    does_overlap, delta, upoints = overlaps(allpoints, scanner)
    if not does_overlap:
        scanners.append(scanner)
        continue
    allpoints.update(upoints)
    deltas.append(delta)

# Part 1
solution(len(allpoints))

# Part 2
maxdistance = max(np.abs(a - b).sum() for a, b in itertools.product(deltas, repeat=2))
solution(int(maxdistance))
