import numpy as np
import re
from aoc import print_board

foldre = re.compile(r'fold along ([xy])=(\d+)')

debug = False
filename = 'test.txt' if debug else 'input.txt'


def p(board):
    print_board(board, lookup={0: '.', 1: '#'}, type='s')


def parse(filename):
    xs = []
    ys = []
    folds = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ',' in line:
                x, y = map(int, line.split(','))
                xs.append(x)
                ys.append(y)
            if 'fold' in line:
                m = foldre.match(line)
                direction, pos = m.groups()
                pos = int(pos)
                folds.append([direction, pos])

    board = np.zeros((max(ys)+1, max(xs)+1), dtype=int)
    board[ys, xs] = 1

    return board, folds


def foldud(board, position):
    top, bottom = board[0:position], board[position+1:]
    width = board.shape[1]
    topheight = top.shape[0]
    bottomheight = bottom.shape[0]
    if debug:
        print("Proposed fold:")
        p(top)
        print('-'*width)
        p(bottom)
    height = max(topheight, bottomheight)
    newboard = np.zeros((height, width), dtype=int)
    newboard[-topheight:] = top
    newboard[-bottomheight:] |= np.flipud(bottom)
    if debug:
        print("New board:")
        p(newboard)
        print()
    return newboard


def dofold(board, direction, position):
    if direction == 'y':
        return foldud(board, position)
    else:
        return foldud(board.T, position).T

board, folds = parse(filename)

# Part 1
if debug:
    print('Board')
    p(board)
direction, position = folds[0]
newboard = dofold(board, direction, position)
if debug:
    print()
    p(newboard)
print('Part 1:', newboard.sum())

# Part 2
for direction, position in folds[1:]:
    newboard = dofold(newboard, direction, position)

print("Part 2:")
print_board(newboard, lookup={1: '█', 0: ' '}, type='s')