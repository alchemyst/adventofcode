import aoc.array
from aoc import solution
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

DIRECTIONS = {
    '^': np.array([-1, 0]),
    'v': np.array([1, 0]),
    '<': np.array([0, -1]),
    '>': np.array([0, 1]),
}

# 90 degree rotation matrix
ROTATION = np.array([[0, 1], [-1, 0]])


def start():
    board = np.array(aoc.array.read_board(filename))
    guard = np.nonzero((board != '.') & (board != '#'))
    guard = np.array([guard[0][0], guard[1][0]])
    guard_direction = DIRECTIONS[board[tuple(guard)]]
    board[tuple(guard)] = '.'

    return board, guard, guard_direction


def off_board(position):
    return any(p < 0 or p >= board.shape[i] for i, p in enumerate(position))


def step(board, guard, guard_direction):
    new_position = guard + guard_direction

    while not(off_board(new_position)) and board[tuple(new_position)] == '#':
        guard_direction = ROTATION @ guard_direction
        new_position = guard + guard_direction

    return new_position, guard_direction


# Part 1
board, guard, guard_direction = start()

if debug:
    aoc.print_board(board, type='s')

steps = np.zeros_like(board, dtype=int)
steps[tuple(guard)] = 1

while True:
    guard, guard_direction = step(board, guard, guard_direction)

    if off_board(guard):
        break

    steps[tuple(guard)] = 1

solution(steps.sum())

# Part 2
board, guard, guard_direction = start()

def stop_condition(board, guard, guard_direction):
    history = set([tuple(guard) + tuple(guard_direction)])
    while True:
        guard, guard_direction = step(board, guard, guard_direction)

        if off_board(guard):
            return "off board"
        state = tuple(guard) + tuple(guard_direction)
        if state in history:  # loop
            return "loop"

        history.add(state)

s = 0
for i, j in np.nditer(np.where(board == '.')):
    # skip initial guard position
    if ((i, j) == guard).all():
        continue

    new_board = board.copy()
    new_board[i, j] = '#'

    if stop_condition(new_board, guard, guard_direction) == 'loop':
        s += 1

solution(s)