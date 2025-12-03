from more_itertools import chunked
from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

with open(filename) as f:
    lines = f.read().splitlines(keepends=False)


def part1(i):
    digits = str(i)
    if len(digits) % 2 != 0:
        return False
    half = len(digits) // 2
    left, right = digits[:half], digits[half:]
    return left == right


def all_ids(lines):
    for line in lines:
        rs = line.split(",")
        for r in rs:
            start, end = map(int, r.split("-"))
            yield from range(start, end + 1)


# Part 1
solution(sum(i for i in all_ids(lines) if part1(i)))


def part2(i):
    digits = str(i)

    for n in range(1, len(digits)):
        if len(digits) % n != 0:
            continue

        chunks = list(chunked(digits, n))
        if all(c == chunks[0] for c in chunks[1:]):
            return True

    return False


# Part 2

solution(sum(i for i in all_ids(lines) if part2(i)))
