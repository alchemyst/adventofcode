#!/usr/bin/env python

import numpy as np


def read(filename):
    boards = []
    with open(filename) as f:
        numbers = list(map(int, next(f).split(",")))

        for line in f:
            if line.strip() == "":
                board = []
                boards.append(board)
            else:
                board.append(list(map(int, line.strip().split())))

    return numbers, boards


def play(numbers, boards, stop):
    boardsize = len(boards[0][0])

    boards = np.array(boards)
    marked = np.full(boards.shape, False)
    won_boards = np.full(len(boards), False)

    # Run game
    for number in numbers:
        marked |= boards == number

        winner = np.full(len(boards), False)
        for axis in (1, 2):
            winner |= (marked.sum(axis=axis) == boardsize).any(axis=1) & (~won_boards)

        won_boards |= winner

        if stop(won_boards):
            break

    return number * boards[winner[:, None, None] & ~marked].sum()


if __name__ == "__main__":
    numbers, boards = read("input.txt")
    print("Part 1:", play(numbers, boards, any))
    print("Part 2:", play(numbers, boards, all))
