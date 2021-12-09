import numpy as np

debug = True
filename = 'test.txt' if debug else 'input.txt'

data = []
with open(filename) as f:
    for line in f:
        data.append([int(c) for c in line.strip()])
heightmap = np.array(data)

lowpoints = []
lowpoint_locations = []
maxi, maxj = heightmap.shape
for j in range(maxj):
    for i in range(maxi):
        value = heightmap[i, j]
        neighbours = []
        if i > 0:
            neighbours.append(heightmap[i - 1, j])
        if i < maxi-1:
            neighbours.append(heightmap[i + 1, j])
        if j > 0:
            neighbours.append(heightmap[i, j-1])
        if j < maxj-1:
            neighbours.append(heightmap[i, j+1])
            
        if all(value < neighbour for neighbour in neighbours):
            lowpoints.append(value)
            lowpoint_locations.append([i, j])

risk_levels = np.array(lowpoints) + 1

print('Part 1:', sum(risk_levels))

# # Part 2

basinmap = np.zeros_like(heightmap) - 1

for basin, (i, j) in enumerate(lowpoint_locations):
    basinmap[i, j] = basin

def basincolor(i, j):
    maxi, maxj = heightmap.shape
    if i < 0 or i >= maxi or j < 0 or j >= maxj:
        return
    
    height = heightmap[i, j]
    
    # Height 9 has no basin
    if height == 9:
        return
    
    basin = basinmap[i, j]
    
    candidates = []
    
    if i > 0:
        candidates.append([i - 1, j])
    if i < maxi-1:
        candidates.append([i + 1, j])
    if j > 0:
        candidates.append([i, j-1])
    if j < maxj-1:
        candidates.append([i, j+1])
    
    for newi, newj in candidates:
        if heightmap[newi, newj] > height and heightmap[newi, newj] != 9:
            basinmap[newi, newj] = basin
            basincolor(newi, newj)


for i, j in lowpoint_locations:
    basincolor(i, j)

from collections import Counter

basincounts = Counter(basinmap[basinmap != -1].ravel())

largest_basins = [size for basin, size in basincounts.most_common(3)]

print('Part 2:', np.prod(largest_basins))


