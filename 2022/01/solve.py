from aoc import solution
import heapq

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = f.readlines()


elf = []
elves = [elf]
for line in lines:
    line = line.strip()
    if not line:
        elf = []
        elves.append(elf)
        continue
    cals = int(line)
    elf.append(cals)

sums = [sum(elf) for elf in elves]

# Part 1
solution(max(sums))

# Part 2
top3 = heapq.nlargest(3, sums)
solution(sum(top3))