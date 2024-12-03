from aoc import solution
import re
import pathlib

debug = False
filename = 'test.txt' if debug else 'input.txt'

inp = pathlib.Path(filename).read_text().replace("\n", "")

muls = re.compile(r"mul\((\d+),(\d+)\)")

def goal(inp):
    return sum(int(a) * int(b) for a, b in muls.findall(inp))

# Part 1
solution(goal(inp))

# Part 2
enabled = re.sub(r"don't\(\).*?do\(\)", "", inp)
enabled = re.sub(r"don't\(\).*", "", enabled)

solution(goal(enabled))