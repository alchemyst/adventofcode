from collections import defaultdict

from aoc import solution
import re

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.read().splitlines()

numbers = re.compile('[0-9]+')

def match_count(line):
    pre, post = line.split("|")
    winning = set([int(n) for n in numbers.findall(pre)][1:])
    what_i_have = {int(n) for n in numbers.findall(post)}
    return len(winning.intersection(what_i_have))

points = 0
for line in lines:
    matches = match_count(line)

    if matches == 1:
        points += 1
    elif matches == 2:
        points += 2
    elif matches > 2:
        points += 2**(matches - 1)


# Part 1
solution(points)

# Part 2

card_counts = defaultdict(lambda: 1)

for card_number, line in enumerate(lines, 1):
    matches = match_count(line)

    for card_offset in range(matches):
        card_counts[card_number + card_offset + 1] += card_counts[card_number]


solution(sum(card_counts.values()))