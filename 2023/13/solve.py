import numpy as np

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    blocks = f.read().split('\n\n')

boards = [np.array([list(line) for line in block.splitlines(keepends=False)]) for block in blocks]

def reflection(board, target=0):
    cols = board.shape[1]
    for i in range(1, cols):
        width = min(i, cols-i)
        left = board[:, i-width:i]
        right = board[:, i + width-1:i-1:-1]

        if (left != right).sum() == target:
            return i

    return 0


def summarise(boards, target):
    vertical_sum = 0
    horizontal_sum = 0
    for board in boards:
        vertical_sum += reflection(board, target)
        horizontal_sum += reflection(board.T, target)

    return vertical_sum + 100*horizontal_sum


# Part 1
solution(summarise(boards, 0))

# Part 2
solution(summarise(boards, 1))