import numpy as np

from aoc import solution, print_board

debug = False
filename = 'test.txt' if debug else 'input.txt'

def visible_line(line):
    v = True
    m = line[0]
    r = [True]
    for e in line[1:]:
        v = e > m
        if e > m:
            m = e
        r.append(v)
    return np.array(r, dtype=bool)


def visible_board(board):
    r = []
    for line in board:
        r.append(visible_line(line))
    return np.array(r)


def all_visible(board):
    result = np.zeros_like(board, dtype=bool)

    for i in range(4):
        vb = np.rot90(visible_board(np.rot90(board, k=i)), k=-i)
        result |= vb

    return result

with open(filename) as f:
    grid = np.array([[int(c) for c in line.strip()] for line in f])


def view(line):
    m = line[0]
    r = 1
    for i, e in enumerate(line[1:], 1):
        r = i
        if e >= m:
            break
    return r


def viewscore(board, i, j):
    up = np.flip(board[:i+1, j])
    down = board[i:, j]
    left = np.flip(board[i, :j+1])
    right = board[i, j:]

    return np.prod([view(d) for d in [up, left, right, down]])

r = all_visible(grid)

# Part 1
solution(r.sum())

# Part 2

result = []
for i in range(grid.shape[0]):
    row = []
    for j in range(grid.shape[1]):
        row.append(viewscore(grid, i, j))
    result.append(row)

result = np.array(result)

solution(result.max())