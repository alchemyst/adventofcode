from aoc import solution, print_board

from aoc.array import read_board
import numpy as np

debug = False
filename = "test.txt" if debug else "input.txt"

# Part 1
lines = []
with open(filename) as f:
    for line in f:
        lines.append(line.strip().split())

numbers = np.array([[int(x) for x in line] for line in lines[:-1]])

OPS = {
    "+": np.sum,
    "*": np.prod,
}

s = 0
for i, op in enumerate(lines[-1]):
    s += OPS[op](numbers[:, i])

solution(s)

# Part 2
board = np.array(read_board(filename)).T

numbers = board[:, :-1]
operations = board[:, -1]

start = True
s = 0
for numberline, opline in zip(numbers, operations):
    if start:
        op = opline
        ns = []
        start = False

    if (numberline == " ").all():
        s += OPS[op](ns)
        start = True
        continue

    ns.append(int("".join(numberline).strip()))

s += OPS[op](ns)

solution(s)
