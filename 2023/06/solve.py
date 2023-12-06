import math
import re

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

numbers = re.compile('[0-9]+')

def all_numbers(line):
    return tuple(int(n) for n in numbers.findall(line))


with open(filename) as f:
    lines = f.read().splitlines()
    times = all_numbers(lines[0])
    records = all_numbers(lines[1])

print(times, records)


def distance_travelled(button, time):
    speed = button
    remaining = time - button
    return speed * remaining


def distances(time):
    for i in range(time):
        yield distance_travelled(i, time)


def winners(record, time):
    for distance in distances(time):
        if distance > record:
            yield distance


from numpy import prod

wins = []
for time, record in zip(times, records):
    wins.append(len(list(winners(record, time))))

# Part 1
solution(prod(wins))

# Part 2
time = int(''.join(str(t) for t in times))
record = int(''.join(str(r) for r in records))

def wins(time, record):
    left, right = sorted([
        (time + math.sqrt(time**2 - 4*record))/2,
        (time - math.sqrt(time**2 - 4*record))/2
    ])

    left = math.ceil(left)
    right = math.floor(right)

    return right - left + 1


solution(wins(time, record))