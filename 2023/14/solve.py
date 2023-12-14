import numpy as np
import numba

from aoc import solution, print_board
from aoc.array import read_board

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename))

if debug:
    print_board(board, type='s')
    print('--')

@numba.jit(nopython=True)
def tilt_north(board):
    for (row, col), value in np.ndenumerate(board):
        if value in ('#', '.'):
            continue

        new_row = row
        while new_row - 1 >= 0 and board[new_row - 1, col] == '.':
            new_row -= 1

        board[row, col] = '.'
        board[new_row, col] = 'O'
    return board

def load(board):
    return ((board == 'O') * np.arange(board.shape[0], 0, -1)[:, None]).sum()


# Part 1
solution(load(tilt_north(board.copy())))

# Part 2
def spin_cycle(board, N):
    loads = []
    for c in range(1, N+1):
        for i in range(4):
            board = tilt_north(board)
            board = np.rot90(board, k=-1)
        loads.append(load(board))

    return loads

loads = np.array(spin_cycle(board.copy(), 400))

cycle_start = 200
m = np.arange(100)
cycle_length = 1
while (loads[m + cycle_start] != loads[m + cycle_start + cycle_length]).any():
    cycle_length += 1

target = 1000000000
target_cycle = (target - cycle_start) % cycle_length + cycle_start - 1

solution(loads[target_cycle])