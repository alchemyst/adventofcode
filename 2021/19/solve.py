from itertools import product
from collections import Counter

import numpy as np
from scipy.spatial.transform import Rotation
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


def rotations(scanner):
    for rotation in Rotation.create_group('O'):
        yield rotation.apply(scanner).astype(int)


def unique_points(scanner):
    return set(tuple(point) for point in scanner)


def overlaps(apoints, bb):
    for b in rotations(bb):
        counts = Counter(tuple(apoint - bpoint) for apoint, bpoint in product(apoints, b))
        [[delta, count]] = counts.most_common(1)
        if count >= 12:
            return True, np.array(delta), unique_points(b + delta)

    return False, None, None


allpoints = unique_points(scanners.pop(0))
base = allpoints.copy()
deltas = []

while scanners:
    print(f"{len(base)=} {len(scanners)=}")
    newscanners = []
    newbase = set()
    for scanner in scanners:
        does_overlap, delta, upoints = overlaps(base, scanner)
        if does_overlap:
            newbase.update(upoints)
            allpoints.update(upoints)
            deltas.append(delta)
        else:
            newscanners.append(scanner)
    base = newbase
    scanners = newscanners

# Part 1
solution(len(allpoints))

# Part 2
maxdistance = max(np.abs(a - b).sum() for a, b in product(deltas, repeat=2))
solution(int(maxdistance))
