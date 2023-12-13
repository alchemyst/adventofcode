import numpy as np

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

boards = []
board = []
boards.append(board)
with open(filename) as f:
    for line in f:
        if line := line.strip():
            board.append(list(line))
        else:
            board = []
            boards.append(board)

boards = [np.array(board) for board in boards]


def reflection(board, target=0, flipped=False):
    cols = board.shape[1]
    for i in range(1, cols//2 + 1):
        left = board[:, :i]
        right = board[:, i:i*2]

        mismatches = (left != np.fliplr(right)).sum()
        if mismatches == target:
            return i

    if flipped:  # we checked both sides
        return None

    flipped_reflection = reflection(np.fliplr(board), target, flipped=True)

    return cols - flipped_reflection if flipped_reflection is not None else None


def summarise(boards, target):
    verticals = []
    horizontals = []
    for board in boards:
        if (v := reflection(board, target)) is not None:
            verticals.append(v)
        if (h := reflection(board.T, target)) is not None:
            horizontals.append(h)

    return sum(verticals) + 100*sum(horizontals)


# Part 1
solution(summarise(boards, 0))

# Part 2
solution(summarise(boards, 1))