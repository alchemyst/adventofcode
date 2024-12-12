import itertools

from aoc import solution
import aoc.array
import numpy as np
import scipy.ndimage as ndi
import scipy.signal as signal

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(aoc.array.read_board(filename))

# Part 1
if debug:
    aoc.print_board(board, type='s')

def regions(board):
    for plant in np.unique(board):
        if debug:
            print(plant)
            aoc.print_board(board == plant, type='d')

        labelled, nlabels = ndi.label(board == plant)
        for i in range(1, nlabels + 1):
            region = labelled == i
            yield region

s = 0
for region in regions(board):
    area = np.sum(region)
    neighbours = ndi.convolve((~region).astype(int), np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), mode='constant', cval=1) * region
    if debug:
        print(neighbours)
    perimeter = np.sum(neighbours)

    if debug:
        print(f"{area=}, {perimeter=}")
    s += area * perimeter

solution(s)

# Part 2
def count_horizontal_sides(region):
    if debug:
        print("sides")
        aoc.print_board(region, type='d')

    horizontal_edges = signal.convolve(region.astype(int), np.array([[-1], [1]]), mode="full", method="direct")

    if debug:
        print(horizontal_edges)

    sides = sum(
        sum(bool(v != 0)
        for v, g in itertools.groupby(scanline))
        for scanline in horizontal_edges
    )

    if debug:
        print(f"{sides=}")

    return sides

s = 0
for region in regions(board):
    area = np.sum(region)
    sides = count_horizontal_sides(region) + count_horizontal_sides(region.T)
    
    if debug:
        print(f"{area=}, {sides=}")

    s += area * sides
    
solution(s)