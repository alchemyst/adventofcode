import re

from aoc import solution, sum_every
from aoc.number_words import digit_values

debug = False
filename = 'test.txt' if debug else 'input.txt'

# Part 1
def part1(line):
    digits = [int(c) for c in line.strip() if c.isdigit()]
    return digits[0]*10 + digits[-1]


solution(sum_every(part1, open(filename)))

# Part 2

digit = f'({"|".join(digit_values)}|[0-9])'
digit_start = re.compile(f'{digit}')
digit_end = re.compile(f'.*{digit}')

for i in range(10):
    digit_values[str(i)] = i


def part2(line):
    m_start = digit_start.search(line)
    m_end = digit_end.match(line)
    first = digit_values[m_start[1]]
    last = digit_values[m_end[1]]
    return first * 10 + last

æ
solution(sum_every(part2, open(filename)))
