import functools
import string

from more_itertools import chunked

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.read().splitlines()

priority = {
    c: score for score, c in
    enumerate(string.ascii_lowercase + string.ascii_uppercase, 1)
}

def score1(line):
    half = len(line)//2
    parts = map(set, [line[:half], line[half:]])

    common, = set.intersection(*parts)

    if debug:
        print(common)

    return common


def run(f, items):
    return sum(priority[f(item)] for item in items)


# Part 1
solution(run(score1, lines))


def score2(group):
    common, = functools.reduce(set.intersection, map(set, group))

    if debug:
        print(common)

    return common


# Part 2
solution(run(score2, chunked(lines, 3)))