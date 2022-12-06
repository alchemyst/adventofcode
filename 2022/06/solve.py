from more_itertools import windowed

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'


def find_marker(line, size):
    for i, chars in enumerate(windowed(line, size), size):
        if len(set(chars)) == size:
            return i


with open(filename) as f:
    line = f.read().strip()


# Part 1
solution(find_marker(line, 4))

# Part 2
solution(find_marker(line, 14))