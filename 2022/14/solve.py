from itertools import pairwise, chain, count
import matplotlib.pyplot as plt

from aoc import solution, print_board
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

OPEN = 0
ROCK = 1
SAND = 2

lines = []
with open(filename) as f:
    for line in f:
        lines.append([
            [int(c) for c in part.split(',')]
            for part in line.strip().split(' -> ')
        ])

allcoords = np.array(list(chain.from_iterable(lines)))

maxx, maxy = allcoords.max(axis=0) + 1
minx, miny = allcoords.min(axis=0)

def build_board(maxx, maxy, lines):
    board = np.zeros((maxx+1, maxy+1), dtype=int)

    for line in lines:
        for ((x, y), (xx, yy)) in pairwise(line):
            x, xx = sorted([x, xx])
            y, yy = sorted([y, yy])
            board[x:xx+1, y:yy+1] = ROCK

    return board

dirs = np.array((
    (0, 1),
    (-1, 1),
    (1, 1),
))


def sand_grain(board, maxy):
    sand = np.array([500, 0])

    while sand[1] < maxy:
        for dir in dirs:
            newpos = tuple(sand + dir)
            if board[newpos] == OPEN:
                sand += dir
                break
        else:
            board[tuple(sand)] = SAND
            break

    return sand

board = build_board(maxx, maxy, lines)

if debug:
    print_board(board[minx-1:, :].T, type='s', lookup='.#o')

for grains in count():
    sand = sand_grain(board, maxy)
    if sand[1] == maxy:
        break

if debug:
    print_board(board[minx-1:maxx, :].T, type='s', lookup='.#o')


# Part 1
solution(grains)

board = build_board(1000, maxy+1, lines)
board[:, -1] = ROCK

if debug:
    print_board(board[minx-1:maxx, :].T, type='s', lookup='.#o')

for grains in count():
    sand = sand_grain(board, maxy+1)
    if (sand == [500, 0]).all():
        break

used = (board[:, :maxy]).any(axis=1)
plt.imshow(board[:, used].T)
plt.show()

# Part 2
solution(grains+1)