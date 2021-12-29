import numpy as np
import scipy.signal as sps

from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

board = []
with open(filename) as f:
    for line in f:
        board.append([int(char) for char in line.strip()])

board = np.array(board)

steps = 1000

flashcount = 0
flashmask = np.ones((3, 3))
flashmask[1, 1] = 0

for i in range(steps):
    allflashed = np.zeros_like(board, dtype=bool)

    # first we add one
    board += 1

    # then we flash
    while True:
        flashed = (board > 9) & ~allflashed
        flashed_this_round = flashed.sum()
        flashcount += flashed_this_round
        if flashed_this_round == 0:
            break
        board += sps.convolve2d(flashed, flashmask, "same").astype(int)
        allflashed |= flashed

    if allflashed.all():
        # Part 2 - this assumes it happens after part 1
        solution(i + 1)
        break

    if i + 1 == 100:
        solution(flashcount)

    board[allflashed] = 0
    if debug:
        print("After step", i + 1)
        print(board)

if debug:
    print(board)
