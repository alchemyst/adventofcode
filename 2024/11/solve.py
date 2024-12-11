from functools import lru_cache

import aoc.parse
from aoc import solution
import pathlib

debug = False
filename = 'test.txt' if debug else 'input.txt'

def read_stones():
    return aoc.parse.all_numbers(pathlib.Path(filename).read_text())

stones = read_stones()

# Part 1
def apply_rule(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
            continue

        digits = f"{stone}"
        if len(digits) % 2 == 0:
            midway = len(digits) // 2
            new_stones += [int(digits[:midway]), int(digits[midway:])]
            continue

        new_stones.append(stone*2024)
    return new_stones

if debug:
    print("Initial arrangement:")
    print(stones)

for i in range(25):
    # print(i)
    stones = apply_rule(stones)
    if debug:
        print(f"After {i+1} blinks")
        print(stones[0])

solution(len(stones))

# Part 2
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

stones = read_stones()
solution(sum(children(stone, 75) for stone in stones))
