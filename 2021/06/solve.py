#!/usr/bin/env python
from collections import Counter

debug = False
filename = 'input.txt' if debug else 'input.txt'

with open(filename) as f:
    fishes = [int(x) for x in f.read().strip().split(',')]

def part1(initialfishes, days):
    fishes = initialfishes[:]
 
    for day in range(1, days+1):
        worklist = fishes.copy()
        for i, fish in enumerate(fishes):
            if fish == 0:
                fish = 6
                worklist.append(8)
            else:
                fish -= 1
                
            worklist[i] = fish

        fishes = worklist
        if debug:
            print(f'Day {day}', Counter(fishes), len(fishes))
            #print(f"Day {day}", ','.join(str(i) for i in fishes))

    return len(fishes)

print("Part 1:", part1(fishes, 80))


fishcounts = dict(Counter(fishes))

days = 256
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

print(sum(fishcounts.values()))
    