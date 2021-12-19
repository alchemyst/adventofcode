import itertools
import networkx as nx

import numpy as np

from aoc import solution, print_board

debug = False
filename = 'test.txt' if debug else 'input.txt'

scanners = []

with open(filename) as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        if line.startswith('--'):
            scanner = []
            scanners.append(scanner)
            continue

        scanner.append([int(n) for n in line.split(',')])

scanners = [np.array(scanner) for scanner in scanners]


def rotate(scanner, rot):
    order, signs = rot
    return scanner[:, order] * np.array(signs)


def inverse(rot, delta):
    """Note: this is broken, it's supposed to find the opposite transform"""
    order, signs = rot
    asigns = np.array(signs)
    aorder = np.array(order)
    new_order = order
    new_signs = tuple(asigns[aorder])
    new_delta = (-delta*asigns)[aorder]

    return (new_order, new_signs), new_delta


def rotations(scanner):
    for order in itertools.permutations(range(0, 3), 3):
        for signs in itertools.product([-1, 1], repeat=3):
            rot = order, signs
            yield rotate(scanner, rot), rot


def unique_points(scanner):
    return set(tuple(point) for point in scanner)


def overlaps(a, bb):
    apoints = unique_points(a)
    for b, rot in rotations(bb):
        for apoint in a:
            for bpoint in b:
                delta = apoint - bpoint
                common_points = apoints.intersection(unique_points(b + delta))

                if len(common_points) >= 12:
                    return True, rot, delta

    return False, None, None


transforms = {}
graph = nx.DiGraph()


def add_link(scanner_a, scanner_b, rot, delta):
    graph.add_edge(scanner_a, scanner_b)
    transforms[(scanner_a, scanner_b)] = rot, delta
    print(f'Scanner {scanner_a} overlaps Scanner {scanner_b} with {rot=} and {delta=}')


for scanner_a in range(len(scanners)):
    for scanner_b in range(scanner_a + 1, len(scanners)):

        does_overlap, rot, delta = overlaps(scanners[scanner_a], scanners[scanner_b])
        if not does_overlap:
            continue

        # figure out reversed transform by brute force because my inverse
        # formula is broken
        do_r, rot_r, delta_r = overlaps(scanners[scanner_b], scanners[scanner_a])
        # print('Inverse found:', rot_r, delta_r)
        # print('Inverse calc:', *inverse(rot, delta))
        assert do_r

        add_link(scanner_a, scanner_b, rot, delta)
        add_link(scanner_b, scanner_a, rot_r, delta_r)


transformed_scanners = []
transformed_locations = []
for perspective, scanner in enumerate(scanners):
    path = nx.shortest_path(graph, perspective, 0)
    transformed_scanner = scanner
    location = np.zeros((1, 3))
    for a, b in zip(path, path[1:]):
        rot, delta = transforms[(b, a)]
        transformed_scanner = rotate(transformed_scanner, rot) + delta
        location = rotate(location, rot) + delta

    transformed_scanners.append(transformed_scanner)
    transformed_locations.append(location[0])

allpoints = set()
for scanner in transformed_scanners:
    allpoints.update(unique_points(scanner))

# Part 1
solution(len(allpoints))

# Part 2
maxdistance = 0
for i in range(len(transformed_locations)):
    for j in range(i+1, len(transformed_locations)):
        distance = np.abs(transformed_locations[i] - transformed_locations[j]).sum()
        if distance > maxdistance:
            maxdistance = distance

solution(maxdistance)