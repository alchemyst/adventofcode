from collections import Counter

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

lefts = []
rights = []

with open(filename) as f:
    for line in f:
        left, right = line.strip().split()
        lefts.append(int(left))
        rights.append(int(right))

lefts.sort()
rights.sort()

diffs = (abs(left - right) for left, right in zip(lefts, rights))

# Part 1
solution(sum(diffs))

# Part 2
right_counts = Counter(rights)
similarity_score = sum(right_counts[left]*left for left in lefts)
solution(similarity_score)