from collections import Counter

import aoc.array
from aoc import solution
import numpy as np

debug = False
filename = "test.txt" if debug else "input.txt"

board = np.array(aoc.array.read_board(filename))

if debug:
    aoc.print_board(board, type="s")


def find(board, char):
    return (board == char).nonzero()[0]


# Part 1
beams = set(find(board[0], "S"))

s = 0
for row in board[1:]:
    splitters = set(find(row, "^"))
    split_beams = beams & splitters
    s += len(split_beams)

    beams -= split_beams

    for beam in split_beams:
        if beam > 0:
            beams.add(beam - 1)
        if beam < len(row):
            beams.add(beam + 1)


solution(s)

# Part 2
beams = Counter(find(board[0], "S"))

s = 1
for row in board[1:]:
    splitters = set(find(row, "^"))
    split_beams = {v: c for v, c in beams.items() if v in splitters}
    s += sum(split_beams.values())

    for beam in split_beams:
        del beams[beam]

    for beam, c in split_beams.items():
        if beam > 0:
            beams[beam - 1] += c
        if beam < len(row):
            beams[beam + 1] += c

solution(s)
