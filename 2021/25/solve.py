import numpy as np
from scipy import ndimage

from aoc import solution, print_board

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    data = [list(line.strip()) for line in f]

initial_board = np.array(data)

def move(board, char, axis):
    new_board = board.copy()

    cucumbers = board == char
    destination = np.roll(cucumbers, 1, axis=axis)
    destination_open = (board == '.') & destination
    moving_cucumbers = np.roll(destination_open, -1, axis=axis)

    new_board[moving_cucumbers] = '.'
    new_board[destination_open] = char

    return new_board

def move_east(board):
    return move(board, '>', 1)

def move_south(board):
    return move(board, 'v', 0)

def step(board):
    return move_south(move_east(board))

def f(a):
    return a[0]

def p(board):
    print_board(board, type='s')

# Part 1
board = initial_board.copy()

steps = 0
while True:
    previous_board = board.copy()
    board = step(board)
    steps += 1
    if (previous_board == board).all():
        break

solution(steps)

# Part 2
board = initial_board.copy()
# solution('Dummy')