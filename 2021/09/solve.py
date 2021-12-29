import numpy as np
from scipy import ndimage
from aoc import print_board, solution
from collections import Counter

debug = False
filename = "test.txt" if debug else "input.txt"

data = []
with open(filename) as f:
    for line in f:
        data.append([int(c) for c in line.strip()])
heightmap = np.array(data)

# Part 1
cross = ndimage.morphology.generate_binary_structure(2, 1)
cross[1, 1] = False

mins = ndimage.minimum_filter(heightmap, footprint=cross, mode="constant", cval=10)
minima = heightmap < mins
if debug:
    print_board(heightmap, minima)

minimum_heights = heightmap[minima]
risk_level = minimum_heights + 1
solution(sum(risk_level))

if debug:
    print_board(heightmap, heightmap < 9)
    print()

labels, nbasins = ndimage.label(heightmap < 9)

basincounts = Counter(labels[labels != 0].ravel())

largest_basins = [size for basin, size in basincounts.most_common(3)]

solution(np.prod(largest_basins))
