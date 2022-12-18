from aoc import solution
import scipy.ndimage as ndi
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

coords = []
with open(filename) as f:
    for line in f:
        coords.append([int(c) for c in line.strip().split(',')])
coords = np.array(coords, dtype='uint')
world = np.zeros(coords.max(axis=0)+4)
for c in coords+2:
    world[tuple(c)] = 1

faces = np.array([
    [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ],
    [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ],
], dtype='uint')


def count_faces(w):
    neighbours = ndi.convolve(w, faces, mode='constant')
    open_faces = (w * (6 - neighbours)).sum()

    return open_faces


# Part 1
solution(count_faces(world))

# Part 2
filled = ndi.binary_fill_holes(world).astype('uint')
solution(count_faces(filled))