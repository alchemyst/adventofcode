from collections import Counter
from aoc import solution

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

solution(solve(fishes, 80))
solution(solve(fishes, 256))
