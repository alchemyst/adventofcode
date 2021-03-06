from collections import Counter
from functools import lru_cache
from itertools import product

from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

# parse
positions = []
with open(filename) as f:
    for line in f:
        positions.append(int(line.strip().split(" ")[-1]))
starting_positions = tuple(positions)


def deterministic_die():
    roll = 1
    while True:
        yield roll
        roll = roll % 100 + 1


def take_3(die):
    return [next(die) for n in range(3)]


# Part 1
scores = [0, 0]
die = deterministic_die()
positions = list(starting_positions)
rolls = 0
player = 0
while max(scores) < 1000:
    throw = take_3(die)
    rolls += 3
    positions[player] = (positions[player] + sum(throw) - 1) % 10 + 1
    scores[player] += positions[player]
    player = (player + 1) % 2

solution(min(scores) * rolls)

# Part 2
# each sum comes up this many times in repeated throws
sumcounts = Counter(sum(t) for t in product([1, 2, 3], repeat=3))


@lru_cache(maxsize=None)
def play(starting_positions, starting_scores, player):
    wins = [0, 0]

    for sum_throw, universes in sumcounts.items():
        positions = list(starting_positions)
        scores = list(starting_scores)

        positions[player] = (positions[player] + sum_throw - 1) % 10 + 1
        scores[player] += positions[player]

        if scores[player] >= 21:
            wins[player] += universes
        else:
            deepwins = play(tuple(positions), tuple(scores), (player + 1) % 2)
            for i in range(2):
                wins[i] += deepwins[i] * universes

    return wins


wins = play(starting_positions, (0, 0), 0)
solution(max(wins))
