import itertools
import re
import numpy as np

from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

number = re.compile(r"(-?[0-9]+)")

with open(filename) as f:
    line = f.read().strip()
    x1, x2, y1, y2 = [int(n) for n in number.findall(line)]


def fire(x0, dx0):
    x = np.asarray(x0)
    dx = np.asarray(dx0)

    positions = []
    while True:
        x += dx
        if dx[0] > 0:
            dx[0] -= 1
        if dx[0] < 0:
            dx[0] += 1
        dx[1] -= 1

        in_box = (x1 <= x[0] <= x2) & (y1 <= x[1] <= y2)
        positions.append(x.copy())
        if in_box or x[0] > x2 or x[1] < y1:
            break

    return np.array(positions), in_box


def plot_trajectory(positions):
    plt.plot(0, 0, "o")
    plt.plot(positions[:, 0], positions[:, 1], "*")
    plt.plot([x1, x1, x2, x2, x1], [y1, y2, y2, y1, y1])


# scan possible x velocities:
working_dx = []
for dx0 in range(1, x2):
    x = 0
    dx = dx0
    working = False
    while x <= x2 and dx != 0:
        x += dx
        if dx > 0:
            dx -= 1
        if x1 <= x <= x2:
            working = True
    if working:
        working_dx.append(dx0)


# scan possible y velocities:
working_dy = []
for dy0 in range(y1 - 1, 1000):
    y = 0
    dy = dy0
    working = False
    while y >= y1:
        y += dy
        dy -= 1
        if y1 <= y <= y2:
            working = True
    if working:
        working_dy.append(dy0)


highest = 0
working_combos = []
for dx, dy in itertools.product(working_dx, working_dy):
    positions, in_box = fire([0, 0], [dx, dy])
    if in_box:
        working_combos.append([dx, dy])
        this_highest = positions[:, 1].max()
        # plot_trajectory(positions)
        if this_highest > highest:
            highest = this_highest

solution(highest)
solution(len(working_combos))
