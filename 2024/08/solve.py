from aoc import solution
import aoc.array
import numpy as np
import itertools

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(aoc.array.read_board(filename))

def off_board(position):
    return any(p < 0 or p >= board.shape[i] for i, p in enumerate(position))


# Part 1
frequencies = np.unique(board[board != '.'])

antinodes = np.zeros_like(board, dtype=bool)
for frequency in frequencies:
    antennas = list(zip(*np.where(board == frequency)))
    for antenna1, antenna2 in itertools.combinations(antennas, 2):
        a1 = np.array(antenna1)
        a2 = np.array(antenna2)

        node1 = a1 + (a1 - a2)
        node2 = a2 + (a2 - a1)

        if not off_board(node1):
            antinodes[tuple(node1)] = True
        if not off_board(node2):
            antinodes[tuple(node2)] = True


solution(antinodes.sum())

# Part 2
antinodes = np.zeros_like(board, dtype=bool)
for frequency in frequencies:
    antennas = list(zip(*np.where(board == frequency)))
    for antenna1, antenna2 in itertools.combinations(antennas, 2):
        a1 = np.array(antenna1)
        a2 = np.array(antenna2)

        for sign in (-1, 1):
            position = a1.copy()
            delta = sign*(a2 - a1)

            while not off_board(position):
                antinodes[tuple(position)] = True
                position += delta

if debug:
    aoc.print_board(antinodes)

solution(antinodes.sum())