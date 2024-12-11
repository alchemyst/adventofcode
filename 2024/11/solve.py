from functools import lru_cache

import aoc.parse
from aoc import solution
import pathlib

debug = False
filename = 'test.txt' if debug else 'input.txt'

def read_stones():
    return aoc.parse.all_numbers(pathlib.Path(filename).read_text())

@lru_cache(maxsize=100000)
def children(stone, turns):
    if turns == 0:
        return 1

    if stone == 0:
        return children(1, turns - 1)

    digits = f"{stone}"
    if len(digits) % 2 == 0:
        midway = len(digits) // 2
        return children(int(digits[:midway]), turns-1) + children(int(digits[midway:]), turns - 1)

    return children(stone*2024, turns - 1)

def nstones(stones, turns):
    return sum(children(stone, turns) for stone in stones)

# Part 1
stones = read_stones()
solution(nstones(stones, 25))

# Part 2
stones = read_stones()
solution(nstones(stones, 75))
