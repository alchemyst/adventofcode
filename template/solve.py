from aoc import solution

debug = True
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.readlines()

# Part 1
solution(len(lines))

# Part 2
solution('Dummy')