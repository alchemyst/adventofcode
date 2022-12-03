from more_itertools import chunked

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.readlines()

priority = {chr(ord('a') + i): i+1 for i in range(26)}
priority |= {chr(ord('A') + i): i+27 for i in range(26)}


def score1(line):
    line = line.strip()
    half = len(line)//2
    compartment1, compartment2 = line[:half], line[half:]

    common, = set(compartment1).intersection(compartment2)
    if debug:
        print(common)
    return priority[common]


# Part 1
solution(sum(score1(line) for line in lines))


def score2(group):
    a, b, c = [set(line.strip()) for line in group]
    common, = a.intersection(b).intersection(c)

    if debug:
        print(common)

    return priority[common]


# Part 2
solution(sum(score2(group) for group in chunked(lines, 3)))