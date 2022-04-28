import itertools

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    line = f.read().strip()


def look_and_say(line):
    return ''.join(f"{len(tuple(group))}{digit}" for digit, group in itertools.groupby(line))


def repeat(line, n):
    for _ in range(n):
        line = look_and_say(line)
    return line
    

if debug:
    examples = (
    ("1", "11"),
    ("11", "21"),
    ("21", "1211"),
    ("1211", "111221"),
    ("111221", "312211"),
    )

    for start, result in examples:
        assert look_and_say(start) == result


# Part 1
solution(len(repeat(line, 40)))

# Part 2
solution(len(repeat(line, 50)))