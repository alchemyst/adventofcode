#!/usr/bin/env python

import numpy as np
from collections import defaultdict

filename = "input.txt"

boards = []

# maps numbers to their positions in boards
bingomap = defaultdict(list)

with open(filename) as f:
    numbers = list(map(int, next(f).split(',')))

    for line in f:
        if line.strip() == '':
            board = []
            boards.append(board)
        else:
            board.append(list(map(int, line.strip().split())))

boardsize = len(board[0])

for boardnum, board in enumerate(boards):
    for i, row in enumerate(board):
        for j, num in enumerate(row):
            bingomap[num].append((boardnum, i, j))

boardarr = np.array(boards)
markings = np.zeros_like(boardarr)

winner = None
for number in numbers:
    for boardnum, i, j in bingomap[number]:
        markings[boardnum, i, j] = 1
        rowsums = markings.sum(axis=1)
        colsums = markings.sum(axis=2)

        if (rowsums == boardsize).any() or (colsums == boardsize).any():
            winner = boardnum
            break
    if winner is not None:
        break

winningboard = boardarr[winner, :, :]
winningmarkings = markings[winner, :, :]

unmarkedsum = winningboard[winningmarkings == 0].sum()

print(unmarkedsum)
print(number)
print(unmarkedsum*number)

# Part 2

print("Part 2")
boardarr = np.array(boards)
markings = np.zeros_like(boardarr)

winningboards = np.zeros(len(boards))

for number in numbers:
    for boardnum, i, j in bingomap[number]:
        markings[boardnum, i, j] = 1
        rowsums = markings[boardnum, :, :].sum(axis=0)
        colsums = markings[boardnum, :, :].sum(axis=1)

        if (rowsums == boardsize).any() or (colsums == boardsize).any():
            if winningboards[boardnum] == 1:
                continue
            
            winner = boardnum
            winningboards[winner] = 1
            if winningboards.sum() == len(boards):
                break

    if winningboards.sum() == len(boards):
        break

print("number", number)
print("winner", winner)

winningboard = boardarr[winner, :, :]
winningmarkings = markings[winner, :, :]

unmarkedsum = winningboard[winningmarkings == 0].sum()

print(unmarkedsum)
print(number)
print(unmarkedsum*number)
