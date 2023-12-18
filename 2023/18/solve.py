import math

from aoc import solution
import parse
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np

debug = True
plot = True
filename = 'test.txt' if debug else 'input.txt'

instruction_pattern = parse.compile('{} {:d} (#{})')

directions = {
    'U': complex(-1, 0),
    'D': complex(1, 0),
    'L': complex(0, -1),
    'R': complex(0, 1)
}

instructions = []
with open(filename) as f:
    for line in f:
        instructions.append(tuple(instruction_pattern.parse(line.strip())))

location = 0 + 0j

trench = {location}

for direction, steps, color in instructions:
    for s in range(steps):
        location += directions[direction]
        trench.add(location)


trench = np.array(list(trench))

rows = trench.real.astype(int)
cols = trench.imag.astype(int)

rows -= rows.min()
cols -= cols.min()

board = np.zeros((rows.max()+1, cols.max()+1))

for row, col in zip(rows, cols):
    board[row, col] = 1


board = ndi.binary_fill_holes(board)

if plot:
    plt.imshow(board)
    plt.show()


# Part 1
solution(board.sum())

# Part 2
location = 0 + 0j

# After a few minutes, someone realizes what happened; someone swapped
# the color and instruction parameters when producing the dig plan.
# They don't have time to fix the bug; one of them asks if you can
# extract the correct instructions from the hexadecimal codes.  Each
# hexadecimal code is six hexadecimal digits long. The first five
# hexadecimal digits encode the distance in meters as a five-digit
# hexadecimal number. The last hexadecimal digit encodes the direction
# to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

location = 0
trench = [location]
boundary_points = 0

for _, _, color in instructions:
    distance = int(color[:5], 16)
    old_location = location
    location = location + distance*directions['RDLU'[int(color[-1])]]

    x1 = int(old_location.real)
    y1 = int(old_location.imag)

    x2 = int(location.real)
    y2 = int(location.real)

    boundary_on_line = math.gcd(x2 - x1, y2 - y1) # + 1 # removed +1 to account for end-to-end
    boundary_points += boundary_on_line

    trench.append(location)

# add back to zero
x1 = int(location.real)
y1 = int(location.imag)

x2 = 0
y2 = 0

boundary_on_line = math.gcd(x2 - x1, y2 - y1) #+ 1 # removed +1 to account for end-to-end
boundary_points += boundary_on_line

trench = np.array(trench)

x = trench.real.astype(int)
y = trench.imag.astype(int)

if plot:
    plt.plot(x, y)
    plt.show()

import shapely

ring = shapely.Polygon(zip(x, y))
area = ring.area

# Pick's formula says
# A = i + b/2 - 1
# so

i = area - boundary_points/2 + 1

solution(boundary_points + i)