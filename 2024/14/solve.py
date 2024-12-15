import aoc
from aoc import solution
from aoc.parse import all_numbers
import numpy as np
import matplotlib.pyplot as plt


debug = False
filename = 'test.txt' if debug else 'input.txt'

board_size = np.array((11, 7) if debug else (101, 103))

def init():
    ps = []
    vs = []

    with open(filename) as f:
        for line in f:
            numbers = all_numbers(line)
            ps.append(numbers[0:2])
            vs.append(numbers[2:4])

    return np.array(ps, dtype=int), np.array(vs, dtype=int)


safety_factor = 0

def show_positions(ps):
    board = np.zeros(tuple(board_size), dtype=int)
    for p in ps:
        board[tuple(p)] += 1

    return board.T

# Part 1
ps, vs = init()

for i in range(20000):
    ps = (ps + vs) % board_size

    if (i - 30) % 103 == 0 and (i - 67) % 101 == 0:
        print(i+1)
        plt.imshow(show_positions(ps))
        plt.savefig(f'frame_{i+1:03d}.png')
        plt.close()

mid_point = board_size // 2


if debug:
    show_positions(ps)

# quadrants
top_left = ((ps[:, 0] < mid_point[0]) & (ps[:, 1] < mid_point[1])).sum()
top_right = ((ps[:, 0] > mid_point[0]) & (ps[:, 1] < mid_point[1])).sum()
bottom_left = ((ps[:, 0] < mid_point[0]) & (ps[:, 1] > mid_point[1])).sum()
bottom_right = ((ps[:, 0] > mid_point[0]) & (ps[:, 1] > mid_point[1])).sum()

print(top_left, top_right, bottom_left, bottom_right)

solution(np.prod([top_left, top_right, bottom_left, bottom_right]))

# Part 2
solution('Dummy')