from aoc import solution, print_board
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

x = 1
history = []
with open(filename) as f:
    for line in f:
        match line.strip().split():
            case ["noop"]:
                history.append(x)
            case ['addx', ax_str]:
                history += [x, x]
                x += int(ax_str)

history = np.array(history)
length = len(history)
points = np.arange(19, length, 40, dtype=int)
signal_strength = (history[points]*(points + 1)).sum()


# Part 1
solution(signal_strength)

cycle_map = (np.reshape(np.arange(length), (length//40, 40))) % 40
x_map = np.reshape(history, (length//40, 40))
pixels = np.abs(x_map - cycle_map) <= 1
print_board(pixels, lookup='.#', type='s')

# Part 2
solution('Dummy')