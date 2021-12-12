import numpy as np
from scipy import ndimage
from aoc import print_board

debug = True
filename = 'test.txt' if debug else 'input.txt'

data = []
with open(filename) as f:
    for line in f:
        data.append([int(c) for c in line.strip()])
heightmap = np.array(data)

# Part 1
cross = ndimage.morphology.generate_binary_structure(2, 1)
cross[1, 1] = False

mins = ndimage.minimum_filter(heightmap, footprint=cross, mode='constant', cval=10)
minima = heightmap < mins
print_board(heightmap, minima)

minimum_heights = heightmap[minima]
risk_level = minimum_heights + 1
print('Part 1:', sum(risk_level))
