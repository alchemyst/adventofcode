from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

pairs = []
with open(filename) as f:
    for line in f:
        line = line.strip()
        a, b = line.split(',')
        a1, a2 = map(int, a.split('-'))
        b1, b2 = map(int, b.split('-'))

        pairs.append(((a1, a2), (b1, b2)))

s = 0
for ((a1, a2), (b1, b2)) in pairs:
    if (a1 >= b1 and a2 <= b2) or (b1 >= a1 and b2 <= a2):
        if debug: print(a1, a2, b1, b2)
        s += 1

# Part 1
solution(s)


s = 0
for ((a1, a2), (b1, b2)) in pairs:
    left = max(a1, b1)
    right = min(a2, b2)
    if left <= right:
        if debug: print(a1, a2, b1, b2)
        s += 1


# Part 2
solution(s)