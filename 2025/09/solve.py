import scipy.ndimage as ndi
from aoc import solution
from itertools import combinations, pairwise

import numpy as np

debug = False
filename = "test.txt" if debug else "input.txt"

red_tiles = []
with open(filename) as f:
    for line in f:
        pair = list(map(int, line.strip().split(",")))
        red_tiles.append(pair)

red_tiles.append(red_tiles[0])  # close loop

red_tiles = np.array(red_tiles)


def area(c1, c2):
    diff = np.abs(c1 - c2) + np.array([1, 1])
    return np.prod(diff)


# Part 1
solution(max(area(c1, c2) for c1, c2 in combinations(red_tiles, 2)))

# Part 2
red_tiles -= red_tiles.min(axis=0)

board = np.zeros(red_tiles.max(axis=0) + 1, dtype=bool)

for start, end in pairwise(red_tiles):
    delta = end - start
    if delta[0] == 0:
        step = np.array([0, np.sign(delta[1])])
    else:
        step = np.array([np.sign(delta[0]), 0])

    while not (start == end).all():
        board[tuple(start)] = True
        start += step
print("Edges drawn")

# fill in
board = ndi.binary_fill_holes(board)
print("Holes filled")


def all_set(c1, c2):

    left = min(c1[0], c2[0])
    right = max(c1[0], c2[0])
    top = min(c1[1], c2[1])
    bottom = max(c1[1], c2[1])

    return board[left : right + 1, top : bottom + 1].all()


from tqdm.auto import tqdm

cs = list(combinations(red_tiles[:-1], 2))
max_area = 0
for c1, c2 in tqdm(cs):
    if area(c1, c2) > max_area:
        if all_set(c1, c2):
            max_area = area(c1, c2)
solution(max_area)
