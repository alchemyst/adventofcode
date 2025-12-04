from aoc import solution
import numpy as np
import scipy.ndimage as ndi
import aoc.array

debug = False
filename = "test.txt" if debug else "input.txt"

board = np.array(aoc.array.read_board(filename, converter="@".__eq__)).astype(int)

shape = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def to_remove(board):
    return (ndi.convolve(board, shape, mode="constant", cval=0) < 4) * board


# Part 1
solution(to_remove(board).sum())

# Part 2
s = 0
while True:
    previous_board = np.array(board)
    remove = to_remove(previous_board)
    s += remove.sum()
    board *= 1 - remove

    if np.array_equal(previous_board, board):
        break

solution(s)
