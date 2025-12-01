from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

pos = 50
TOTAL = 100

with open(filename) as f:
    lines = f.read().splitlines(keepends=False)

n = 0
for line in lines:
    direction = line[0]
    value = int(line[1:])

    if direction == "L":
        pos = (pos - value) % TOTAL
    elif direction == "R":
        pos = (pos + value) % TOTAL

    if pos == 0:
        n += 1


# Part 1
solution(n)

# Part 2
n = 0
pos = 50
for line in lines:
    direction = line[0]
    sign = 1 if direction == "R" else -1
    value = int(line[1:])

    rotations, left = divmod(value, TOTAL)

    n += rotations

    # I couldn't figure out the clever way with mods here
    for i in range(left):
        pos = (pos + sign) % TOTAL
        if pos == 0:
            n += 1

solution(n)
