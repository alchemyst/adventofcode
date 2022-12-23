import re

import numpy as np
from matplotlib import pyplot as plt

from aoc import solution, print_board

right, down, left, up = range(4)
names = ['right', 'down', 'left', 'up']
directions = (
    ( 0,  1),
    ( 1,  0),
    ( 0, -1),
    (-1,  0),
)

debug = False
filename = 'test.txt' if debug else 'input.txt'

if debug:
    face_size = 4
    faces = np.array([
        [0, 0, 6, 0],
        [4, 5, 3, 0],
        [0, 0, 1, 2],
    ])
    # connectivity: down, right, up, left
    # face, new_direction
    conn = {
        #   right       down        left       up
        1: ((2, right), (4, up),    (5, up),   (3, up),    ),
        2: ((6, left),  (4, right), (1, left), (3, left),  ),
        3: ((2, down),  (1, down),  (5, left), (6, up),    ),
        4: ((5, right), (1, up),    (2, up),   (6, down),  ),
        5: ((3, right), (1, right), (4, left), (6, right), ),
        6: ((2, left),  (3, down),  (5, down), (4, down),  ),
    }
else:
    face_size = 50
    faces = np.array([
        [0, 5, 6],
        [0, 3, 0],
        [1, 2, 0],
        [4, 0, 0],
    ])
    conn = {
        #   right       down       left       up
        1: ((2, right), (4, down), (5, right), (3, right), ),
        2: ((6, left),  (4, left), (1, left),  (3, up),    ),
        3: ((6, up),    (2, down), (1, down),  (5, up),    ),
        4: ((2, up),    (6, down), (5, down),  (1, up),    ),
        5: ((6, right), (3, down), (1, right), (4, right), ),
        6: ((2, left),  (3, left), (5, left),  (4, up),    ),
    }


def read_board(filename):
    board_lines = []
    with open(filename) as f:
        for line in f:
            board_lines.append(line[:-1])
            if not line[:-1]:
                break

        instructions = []
        for part in re.findall(r'(R|L|\d+)', f.read().strip()):
            if part in 'RL':
                instructions.append(part)
            else:
                instructions.append(int(part))

    boardwidth = max(len(b) for b in board_lines)

    board = np.array(
        [list(line) + [' '] * (boardwidth - len(line)) for line in board_lines],
        dtype=str
    )

    return board, instructions


board, instructions = read_board(filename)

if False and debug:
    board[board == "#"] = '.'
    instructions = ("R", "R", "R", face_size*5,)
    # print_board(board, type='s')


def plot_board(board, positions):
    fig, ax = plt.subplots()

    # for (i, j), c in np.ndenumerate(board):
    #     plt.text(j, i, c)
    for (i, j), b in np.ndenumerate(faces):
        if b == 0:
            continue
        plt.fill(
            np.array([j, j+1, j+1, j])*face_size,
            np.array([i, i, i+1, i+1])*face_size,
            color=f"C{b}", alpha=0.1
        )
        plt.text((j+0.5)*face_size, (i+0.5)*face_size, str(b), fontsize=20, alpha=0.2)

    plt.xlim(-1, board.shape[1])
    plt.ylim(-1, board.shape[0])
    ax.invert_yaxis()
    ax.plot(positions[:, 1], positions[:, 0], 'r.')
    plt.draw()


# Part 1
def forward1(board, position, direction, number):
    for _ in range(number):
        newposition = (position + directions[direction]) % board.shape
        board_at_newposition = board[tuple(newposition)]
        while board_at_newposition == ' ':
            newposition = (newposition + directions[direction]) % board.shape
            board_at_newposition = board[tuple(newposition)]

        if board_at_newposition == '.':
            position = newposition
        if board_at_newposition == '#':
            break

    return position, direction


def walk(board, instructions, forward):
    position = np.array([0, np.nonzero(board[0, :] == '.')[0][1] - 1])
    direction = 0

    positions = [position]
    for instruction in instructions:
        if debug: print(instruction)
        match instruction:
            case "R":
                direction = (direction + 1) % 4
            case "L":
                direction = (direction - 1) % 4
            case number:
                position, direction = forward(board, position, direction, number)
                positions.append(tuple(position))

    positions = np.array(positions)

    return position, direction, positions


# position, direction, positions = walk(board, instructions, forward1)
#
# if debug:
#     plot_board(board, positions)
#
# solution(1000 * (position[0] + 1) + 4 * (position[1] + 1) + direction)

def get_face(position):
    return faces[tuple((position // face_size) % faces.shape)]


# Part 2
def forward2(board, position, direction, number):
    for _ in range(number):
        face = get_face(position)
        newdirection = direction
        newposition = position + directions[direction]
        newface = get_face(newposition)
        if newface != face:
            position_in_face = position % face_size
            newface, newdirection = conn[face][direction]
            if debug: print(f"Moving {names[direction]} on face {face} to {names[newdirection]} on face {newface}")
            if debug: print("Position before", position)
            # top left of new face
            newposition = np.array(np.nonzero(faces == newface)).T[0]*face_size
            pair = direction, newdirection
            if direction == newdirection:
                newposition += (position_in_face + directions[direction]) % face_size
            elif pair in ((up, down), (down, up)):
                newposition[0] += position_in_face[0]
                newposition[1] += face_size - position_in_face[1] - 1
            elif pair in ((left, right), (right, left)):
                newposition[0] += face_size - position_in_face[0] - 1
                newposition[1] += position_in_face[1]
            elif pair in ((up, left), (right, down)):
                newposition[0] += position_in_face[1]
                newposition[1] += face_size - position_in_face[0] - 1
            elif pair in ((up, right), (left, down)):
                newposition[0] += position_in_face[1]
                newposition[1] += position_in_face[0]
            elif pair in ((down, left), (right, up)):
                newposition[0] += position_in_face[1]
                newposition[1] += position_in_face[0]
            elif pair in ((down, right), (left, up)):
                newposition[0] += face_size - position_in_face[1] - 1
                newposition[1] += face_size - position_in_face[0] - 1

        if debug: print("newposition:", newposition)
        board_at_newposition = board[tuple(newposition)]
        if debug: print("Board at newposition:", board_at_newposition)
        if board_at_newposition == '.':
            position = newposition
            direction = newdirection
            if debug:
                print("Position changed", position)
                plt.plot(position[1], position[0], 'rx')
                plt.draw()
            continue
        if board_at_newposition == '#':
            break

    return position, direction

position, direction, positions = walk(board, instructions, forward2)

if debug:
    plot_board(board, positions)
    plt.show()

solution(1000 * (position[0] + 1) + 4 * (position[1] + 1) + direction)
