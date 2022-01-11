from hashlib import md5
from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    start = f.read().strip()

def searcher(zeros, start):
    i = 0
    while True:
        i += 1
        if md5(f"{start}{i}".encode()).hexdigest().startswith('0'*zeros):
            break
    return i

# Part 1
solution(searcher(5, start))

# Part 2
solution(searcher(6, start))