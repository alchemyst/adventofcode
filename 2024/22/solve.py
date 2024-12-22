from collections import defaultdict
from itertools import pairwise

from more_itertools import windowed

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    starts = [int(i) for i in f.read().strip().split()]

def mix(secret, other):
    return secret ^ other

def prune(number):
    return number % 16777216

def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))

    return secret

if debug:
    print("mix", mix(42, 15))
    print("prune", prune(100000000))

    print("Example next 10")
    secret = 123
    for i in range(10):
        secret = next_secret(secret)
        print(secret)

def iterate(secret, n):
    yield secret
    for i in range(n):
        secret = next_secret(secret)
        yield secret

# Part 1
sequences = []

s = 0
for start in starts:
    sequences.append(list(iterate(start, 2000)))
    s += sequences[-1][-1]


solution(s)

# Part 2
first_occurences = []
all_windows = set()
for sequence in sequences:
    prices = [secret % 10 for secret in sequence]
    changes = [(b - a) for a, b in pairwise(prices)]
    first_occurence = defaultdict(int)
    for window, price in zip(map(tuple, windowed(changes, 4)), prices[4:]):
        if window not in first_occurence:
            first_occurence[window] = price
        all_windows.add(window)
    first_occurences.append(first_occurence)

solution(max(sum(occurence[window] for occurence in first_occurences) for window in all_windows))