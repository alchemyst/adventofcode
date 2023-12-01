from aoc import solution

# Part 1
s = 0
for line in open('input.txt'):
    digits = [c for c in line.strip() if c.isdigit()]
    num = int(f"{digits[0]}{digits[-1]}")
    s += num

solution(s)

# Part 2
import re

digit = '(zero|one|two|three|four|five|six|seven|eight|nine|[0-9])'
digit_start = re.compile(f'{digit}')
digit_end = re.compile(f'.*{digit}')
digit_values = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}
for i in range(10):
    digit_values[str(i)] = i

s = 0
for line in open('input.txt'):
    m_start = digit_start.search(line)
    m_end = digit_end.match(line)
    first = digit_values[m_start[1]]
    last = digit_values[m_end[1]]
    s += first * 10 + last

solution(s)
