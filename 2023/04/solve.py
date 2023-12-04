from aoc import solution, sum_every
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

matches_lines = [match_count(line) for line in lines]


def points(matches):
    return 0 if matches == 0 else 2**(matches - 1)


# Part 1
solution(sum_every(points, matches_lines))

# Part 2
card_counts = {card_number: 1 for card_number in range(1, len(lines)+1)}

for card_number, matches in enumerate(matches_lines, 1):
    for card_offset in range(matches):
        card_counts[card_number + card_offset + 1] += card_counts[card_number]

solution(sum(card_counts.values()))