import math

from aoc import solution, prod_every
from aoc.parse import all_numbers, read_splitlines

debug = False
filename = 'test.txt' if debug else 'input.txt'

lines = read_splitlines(filename)
times, records = map(all_numbers, lines[:2])

def wins(time, record):
    left = math.ceil((time - math.sqrt(time ** 2 - 4 * record)) / 2)
    right = math.floor((time + math.sqrt(time ** 2 - 4 * record)) / 2)

    return right - left + 1

# Part 1
solution(prod_every(lambda a: wins(*a), zip(times, records)))

# Part 2
time = int(''.join(str(t) for t in times))
record = int(''.join(str(r) for r in records))

solution(wins(time, record))

