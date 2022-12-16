from itertools import product, groupby
from operator import itemgetter

import numpy as np
from matplotlib import pyplot as plt
from tqdm.auto import tqdm
from aoc import solution
import re

debug = False
plot = True
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

def dist(p1, p2):
    return np.abs(p1 - p2).sum()

if plot: fig, ax = plt.subplots()

if debug:
    y = 10
else:
    y = 2000000

distances = np.abs(sensors - beacons).sum(axis=1)

def part1():
    reachable = (sensors[:, 1] + distances > y) & (sensors[:, 1] - distances < y)

    rsensors = sensors[reachable, :]
    rbeacons = beacons[reachable, :]
    rdistances = distances[reachable]
    minx = (rsensors[:, 0] - rdistances).min()
    maxx = (rsensors[:, 0] + rdistances).max()

    covered_x = set()
    print(minx, maxx)
    for x in tqdm(range(minx, maxx)):
        for s, d in zip(rsensors, rdistances):
            point = (x, y)
            if dist(s, point) <= d:
                covered_x.add(x)

    for bx, by in beacons:
        if by == y:
            if bx in covered_x:
                covered_x.remove(bx)

covered_x = part1()

# Part 1
solution(len(covered_x))

# Part 2
if debug:
    boardsize = 20
else:
    boardsize = 4000000

def plot_board(zoom):
    fig, ax = plt.subplots()

    for s, b, d in zip(sensors, beacons, distances):
        plt.plot(*s, 'r.')
        plt.plot(*b, 'b.')
        x, y = s

        plt.fill([x-d, x, x+d, x], [y, y-d, y, y+d], color='b', alpha=0.1)


    if zoom:
        plt.xlim([found_x - 10, found_x + 10])
        plt.ylim([found_y - 10, found_y + 10])

    plt.plot(found_x, found_y, 'rx')
    ax.invert_yaxis()

if plot: plot_board()

found_y = None
for y in tqdm(range(boardsize)):
    x = 0
    if plot: plt.axhline(y)
    edges = []
    for s, d in zip(sensors, distances):
        sx, sy = s
        dy = abs(sy - y)
        if dy > d:
            continue
        offset = d - dy
        edges += [(sx - offset, 1), (sx + offset, -1)]
    edges.sort()
    coverage = 0
    coverplot = []
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
    plt.show(zoom=True)

tuning_frequency = found_x*4000000 + found_y
solution(tuning_frequency)