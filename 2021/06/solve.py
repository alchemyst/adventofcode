#!/usr/bin/env python
from collections import Counter

debug = False
filename = 'input.txt' if debug else 'input.txt'

with open(filename) as f:
    fishes = [int(x) for x in f.read().strip().split(',')]

def solve(fishes, days):
    fishcounts = Counter(fishes)

    for day in range(1, days+1):
        newcounts = Counter()

        zeros = fishcounts.pop(0, 0)
        for count, fish in fishcounts.items():
            if fish != 0:
                newcounts[count-1] = fish
        newcounts[8] = zeros
        newcounts[6] += zeros

        fishcounts = newcounts
        if debug:
            print(f"Day {day}", fishcounts, sum(fishcounts.values()))
    
    return sum(fishcounts.values())

print("Part 1:", solve(fishes, 80))
print("Part 2:", solve(fishes, 256))
