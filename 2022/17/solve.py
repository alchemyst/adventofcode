from itertools import cycle

from aoc import solution, print_board
import numpy as np

debug = False
move_debug = False
filename = 'test.txt' if debug else 'input.txt'

ROCK = 1
OPEN = 0
WIDTH = 7

rocks_array = [np.array(a, dtype='ubyte') for a in [
    [[1, 1, 1, 1]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1]],

    [[1],
     [1],
     [1],
     [1]],

    [[1, 1],
     [1, 1]],
]]

moves = {
    '>': np.array([0, 1]),
    '<': np.array([0, -1]),
    'v': np.array([1, 0]),
}


def rock_footprint(board, rock, bottom_left):
    rock_height, rock_width = rock.shape

    top, left = bottom_left - [rock_height, 0]
    bottom = bottom_left[0]

    return board[top:bottom, left:left + rock_width]


def checkmove(board, rock, bottom_left, move):
    di, dj = direction = moves[move]

    target_blocks = rock_footprint(board, rock, bottom_left + direction)

    if (target_blocks & rock).any():
        return bottom_left, True
    else:
        return bottom_left + direction, False


with open(filename) as f:
    jetline = f.read().strip()


def simulate(target_rocks):
    jets = cycle(jetline)
    rocks = cycle(rocks_array)

    board = np.zeros((4 * target_rocks, WIDTH + 2), dtype='ubyte')
    board[-1, :] = ROCK
    board[:, 0] = ROCK
    board[:, -1] = ROCK

    top_of_stack = board.shape[0]-1

    rocks_fallen = 0
    stopped = True
    heights = []
    while True:
        jet = next(jets)
        if stopped:
            if False:
                print_board(board[top_of_stack-5:, :], type='s', lookup='.#@')
                print()
            rock = next(rocks)
            bottom_left = np.array([top_of_stack - 3, 3])
            stopped = False

        if move_debug:
            board_copy = board.copy()
            target = rock_footprint(board_copy, rock, bottom_left)
            target[rock == 1] = 2

            print_board(board_copy[top_of_stack-10:, :], type='s', lookup='.#@')
            print()

        bottom_left, _ = checkmove(board, rock, bottom_left, jet)
        new_bottom_left, stopped = checkmove(board, rock, bottom_left, 'v')
        if stopped:
            target = rock_footprint(board, rock, bottom_left)
            target |= rock
            top_of_stack = min(top_of_stack, bottom_left[0]-rock.shape[0])
            height = board.shape[0] - top_of_stack - 1
            heights.append(height)
            rocks_fallen += 1
            if rocks_fallen == target_rocks:
                break
        else:
            bottom_left = new_bottom_left

    return heights


# Part 1
heights = simulate(2022)
solution(heights[-1])


# Part 2
target_rocks = 5000
heights = simulate(target_rocks)
height = heights[-1]
changes = np.diff(heights)
settle = 500
width = 400

diffs = []
for start in range(settle+width, len(changes)-width):
    diff = np.abs(changes[settle:settle+width] - changes[start:start+width]).sum()
    diffs.append(diff)
diffs = np.array(diffs)

zeros = np.nonzero(diffs == 0)

pattern_width, = np.unique(np.diff(zeros))

total_rocks = 1000000000000
growth_in_pattern = sum(changes[-pattern_width:])
rocks_remaining = total_rocks - target_rocks
full_cycles, partial_rocks = divmod(rocks_remaining, pattern_width)
growth_in_part = sum(changes[-pattern_width:-(pattern_width - partial_rocks)])

solution(height + full_cycles*growth_in_pattern + growth_in_part)
