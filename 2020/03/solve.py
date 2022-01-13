#!/usr/bin/env python

themap = []
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        themap.append([1 if ch == '#' else 0 for ch in line])

width = len(themap[0])

def checkslope(right, down):
    y = 0
    x = 0
    trees = 0 
    while y < len(themap):
        trees += themap[y][x]

        y += down
        x = (x + right) % width

    return trees

options = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]

prod = 1
for right, down in options:
    prod *= checkslope(right, down)

print(prod)
