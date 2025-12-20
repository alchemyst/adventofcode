from functools import lru_cache
from itertools import product
from sys import maxsize

from aoc import solution, print_board
from aoc.parse import blocks
import numpy as np

debug = True
filename = "test.txt" if debug else "input.txt"

shapes = []

*shape_blocks, region_block = blocks(filename)

shapes = [np.array([list(l) for l in block[1:]]) == "#" for block in shape_blocks]

regions = []
for region_line in region_block:
    left, right = region_line.split(": ")
    width, height = map(int, left.split("x"))
    counts = tuple(int(g) for g in right.split(" "))

    regions.append((width, height, counts))


# Part 1
# We'll model the state as a number of (row, col, shape (index), rotation, flip) tuples
# that say where the shapes have been placed so far


def fits(board, row, col, shape, rotation, flip):
    rotated_shape = rotate_and_flip(shape, rotation, flip)

    shape_rows, shape_cols = rotated_shape.shape
    board_rows, board_cols = board.shape

    if row + shape_rows > board_rows or col + shape_cols > board_cols:
        return False

    return not np.any(
        board[row : row + shape_rows, col : col + rotated_shape.shape[1]]
        & rotated_shape
    )


def rotate_and_flip(shape, rotation, flip):
    rotated_shape = np.rot90(shapes[shape], rotation)
    if flip:
        rotated_shape = np.fliplr(rotated_shape)

    return rotated_shape


def board_from_state(state):
    board = np.zeros((height, width), dtype=bool)

    for row, col, shape, rotation, flip in state:
        rotated_shape = rotate_and_flip(shape, rotation, flip)
        board[
            row : row + rotated_shape.shape[0], col : col + rotated_shape.shape[1]
        ] = rotated_shape

    return board


@lru_cache
def fits_from_state(state, row, col, shape, rotation, flip):
    board = board_from_state(state)
    return fits(board, row, col, shape, rotation, flip)


def pick_shape(counts):
    for i, count in enumerate(counts):
        if count:
            break

    return i, (*counts[:i], count - 1, *counts[i + 1 :])


@lru_cache
def can_place(state, counts):
    shape, remaining_counts = pick_shape(counts)

    seen_shapes = set()
    for rotation, flip in product(rotations, flips):
        rotated_shape = tuple(rotate_and_flip(shape, rotation, flip).ravel())

        if rotated_shape in seen_shapes:
            continue

        seen_shapes.add(rotated_shape)

        rows = range(height - shapes[shape].shape[0] + 1)
        cols = range(width - shapes[shape].shape[1] + 1)

        for row, col in product(rows, cols):
            if fits_from_state(tuple(sorted(state)), row, col, shape, rotation, flip):
                if not any(remaining_counts):
                    return True

                new_state = (*state, (row, col, shape, rotation, flip))
                if can_place(new_state, remaining_counts):
                    return True
    return False


rotations = range(4)
flips = [False, True]

# test

width, height = 4, 4
board = board_from_state(((0, 0, 4, 0, 0),))

# assert fits(board, 1, 1, 4, 2, 0)

s = 0
for width, height, counts in regions:
    print(width, height, counts)

    if can_place((), counts):
        print(True)
        s += 1

solution(s)

# Part 2
solution("dummy")
