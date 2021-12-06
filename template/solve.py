#!/usr/bin/env python

debug = True
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.readlines()

print(len(lines))