#!/usr/bin/env python

import numpy as np

# x, y, z increments
increments = {
    'forward': np.array([0, 1, 0]),
    'backward': np.array([0, -1, 0]),
    'up': np.array([0, 0, 1]),
    'down': np.array([0, 0, -1]),
    'left': np.array([-1, 0, 0]),
    'right': np.array([1, 0, 0]),
}

lines = [line.strip().split() for line in open("input.txt")]

print('Part 1')

position = np.array([0, 0, 0])

for direction, X in lines:
    position += increments[direction] * int(X)

print(position)

# "depth" is reported as positive going down
print(-position[1]*position[2])

print('Part 2')

# horizontal position, depth
horizontal = 0
depth = 0
aim = 0

for direction, X in lines:
    X = int(X)
    if direction == 'down':
        aim += X
    elif direction == 'up':
        aim -= X
    elif direction == 'forward':
        horizontal += X
        depth += aim * X

print(f'{aim}, {horizontal}, {depth}')
print(horizontal*depth)