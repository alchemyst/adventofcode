#!/usr/bin/env python

import numpy as np
import pandas as pd
from dataclasses import dataclass
import re

debug = False
filename = 'test.txt' if debug else 'input.txt'

lines = []

numbers = re.compile('[0-9]+')

maxx = 0
maxy = 0

with open(filename) as f:
    for line in f:
        x1, y1, x2, y2 = map(int, numbers.findall(line))
        maxx = max(maxx, x1, x2)
        maxy = max(maxy, y1, y2)
        lines.append([x1, y1, x2, y2])

def solve(diagonals):
    diagram = np.zeros((maxx+1, maxy+1))

    for x1, y1, x2, y2 in lines:
        if not diagonals and not (x1 == x2 or y1 == y2):
            continue
        
        start = np.array([x1, y1])
        end = np.array([x2, y2])
        delta = end - start
        step = np.sign(delta)  # assume all steps are 1 magnitude

        for i in range(max(abs(delta))+1):
            x, y = start + i*step
            diagram[x, y] += 1

    if debug:
        print(diagram.T)
    return (diagram >= 2).sum()

print("Part 1:", solve(False))
print("Part 2:", solve(True))
