from aoc import solution
import numpy as np
import pathlib
import more_itertools

debug = False
filename = 'test.txt' if debug else 'input.txt'

blocks = [
    np.array([list(line) for line in block.splitlines(keepends=False)])
    for block in pathlib.Path(filename).read_text().split("\n\n")
]

def is_lock(block):
    return (block[0] == "#").all() and (block[-1] == '.').all()

keys, locks = map(list, more_itertools.partition(is_lock, blocks))

def fits(key, lock):
    return ((key == '#').astype(int) + (lock == '#').astype(int) <= 1).all()

# Part 1
solution(sum(fits(key, lock) for key in keys for lock in locks))

# Part 2
solution(0)