from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

data = []

with open(filename) as f:
    for line in f:
        l, w, h = map(int, line.strip().split('x'))

        data.append((l, w, h))

# Part 1
area = 0

for l, w, h in data:
    sides = [l * w, w * h, h * l]
    area += 2*sum(sides) + min(sides)

solution(area)

# Part 2

ribbon_length = 0
for l, w, h in data:
    volume = l * w * h
    sorted_sides = sorted([l, w, h])
    smallest_side, second_smallest_side = sorted_sides[:2]
    ribbon_length += 2*(smallest_side + second_smallest_side) + volume

solution(ribbon_length)