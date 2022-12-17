from itertools import product, groupby
from operator import itemgetter

import numpy as np
from matplotlib import pyplot as plt
from tqdm.auto import tqdm
from aoc import solution
import re

debug = False
plot = False
filename = 'test.txt' if debug else 'input.txt'

int_re = re.compile(r'[-0-9]+')

sensors = []
beacons = []
with open(filename) as f:
    for line in f:
        sx, sy, bx, by = [int(p) for p in int_re.findall(line)]
        sensors.append((sx, sy))
        beacons.append((bx, by))

sensors = np.array(sensors)
beacons = np.array(beacons)
distances = np.abs(sensors - beacons).sum(axis=1)


def dist(p1, p2):
    return np.abs(p1 - p2).sum()


def find_edges(sensors, distances, y):
    edges = []
    for s, d in zip(sensors, distances):
        sx, sy = s
        dy = abs(sy - y)
        if dy > d:
            continue
        offset = d - dy
        edges += [(sx - offset, 1), (sx + offset, -1)]
    edges.sort()

    return edges


def plot_board(zoom=False):
    fig, ax = plt.subplots()

    for s, b, d in zip(sensors, beacons, distances):
        plt.plot(*s, 'r.')
        plt.plot(*b, 'b.')
        x, y = s

        plt.fill([x-d, x, x+d, x], [y, y-d, y, y+d], color='b', alpha=0.1)


    if zoom:
        plt.xlim([found_x - 10, found_x + 10])
        plt.ylim([found_y - 10, found_y + 10])

    ax.invert_yaxis()


# Part 1
if debug:
    y = 10
else:
    y = 2000000

covered_x = set()
for s, d in zip(sensors, distances):
    sx, sy = s
    dy = abs(sy - y)
    if dy > d:
        continue
    offset = d - dy
    covered_x.update(range(sx - offset, sx + offset+1))

for bx, by in beacons:
    if by == y:
        covered_x -= {bx}

if plot:
    plot_board()
    for x in covered_x:
        plt.plot(x, y, 'kx')

solution(len(covered_x))

# Part 2
if debug:
    boardsize = 20
else:
    boardsize = 4000000


found_y = None
for y in tqdm(range(boardsize)):
    x = 0
    coverage = 0
    coverplot = []
    edges = find_edges(sensors, distances, y)
    for x, g in groupby(edges, itemgetter(0)):
        total_coverage = sum(c for _, c in g)
        coverage += total_coverage
        coverplot.append([x, coverage])
        if coverage == 0 and 0 <= x <= boardsize:
            found_x = x + 1
            found_y = y
            break

    if found_y is not None:
        break


if plot:
    plt.plot(found_x, found_y, 'rx')
    plt.show()

tuning_frequency = found_x*4000000 + found_y
solution(tuning_frequency)