from aoc import solution
from aoc.directions import DIRECTIONS
import aoc.array
import pathlib
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

contents = pathlib.Path(filename).read_text()

def init(process=str):
    map_part, instructions = contents.split('\n\n')
    instructions = instructions.replace("\n", "")

    board = np.array([list(process(line)) for line in map_part.splitlines(keepends=False)])
    robot = np.array((board == '@').nonzero()).flatten()
    board[tuple(robot)] = '.'

    return board, robot, instructions

# Part 1
board, robot, instructions = init()

if debug:
    aoc.print_board(board, type='s')

for direction in instructions:
    if debug:
        aoc.print_board(board, type='s')
        print("Move", direction)
    move = DIRECTIONS[direction]
    new_pos = robot + move
    next_block = board[tuple(new_pos)]

    if next_block == '.':
        robot = new_pos
        continue

    if next_block == '#':
        continue

    if next_block == 'O':
        chain_end = new_pos
        chain_blocks = []
        while (chain_end_block := board[tuple(chain_end)]) == 'O':
            chain_end = chain_end + move  # avoid mutation
            chain_blocks.append(chain_end)

        if chain_end_block == '#':
            continue
        elif chain_end_block == '.':
            robot = new_pos
            board[tuple(new_pos)] = '.'
            for block in chain_blocks:
                board[tuple(block)] = 'O'

tops, lefts = (board == 'O').nonzero()
gps_coordinates = 100*tops + lefts

solution(gps_coordinates.sum())

# Part 2
def double(s):
    return (
        s
        .replace('#', '##')
        .replace('O', '[]')
        .replace('.', '..')
        .replace('@', '@.')
    )

board, robot, instructions = init(double)

if debug:
    aoc.print_board(board, type='s')

def box_at(pos):
    return (new_pos // [1, 2]) * [1, 2]


def try_move_box(board, pos, move):
    new_board = board.copy()

    # we always store the top left corner of a box
    if board[tuple(pos)] == ']':
        pos = pos - [0, 1]

    # build a set of boxes connected to the first one
    boxes_to_check = [pos]  # queue of boxes to check
    connected_boxes = set()

    while boxes_to_check:
        box = boxes_to_check.pop()
        connected_boxes.add(tuple(box))

        # horizontal is easy
        if move[0] == 0:
            next_box = box + 2*move
            if board[tuple(next_box)] == '[':
                boxes_to_check.append(next_box)
        else:
            for new_position in box + move, box + [0, 1] + move:
                if board[tuple(new_position)] == '[':
                    boxes_to_check.append(new_position)
                if board[tuple(new_position)] == ']':
                    boxes_to_check.append(new_position - [0, 1])

    for box in connected_boxes:
        new_board[box] = '.'
        new_board[tuple(np.array(box) + [0, 1])] = '.'

    for box in connected_boxes:
        if new_board[tuple(box + move)] != '.' or new_board[tuple(box + move + [0, 1])] != '.':
            return board, False

        new_board[tuple(box + move)] = '['
        new_board[tuple(box + move + [0, 1])] = ']'

    return new_board, True



for direction in instructions:
    if debug:
        board_with_robot = board.copy()
        board_with_robot[tuple(robot)] = '@'
        aoc.print_board(board_with_robot, type='s')
        print("Move", direction)

    move = DIRECTIONS[direction]
    new_pos = robot + move
    next_block = board[tuple(new_pos)]

    if next_block == '.':
        robot = new_pos
        continue

    if next_block == '#':
        continue

    if next_block in '[]':
        new_board, moved = try_move_box(board, new_pos, move)
        if moved:
            board = new_board
            robot = new_pos
            continue

tops, lefts = (board == '[').nonzero()
gps_coordinates = 100 * tops + lefts

solution(gps_coordinates.sum())