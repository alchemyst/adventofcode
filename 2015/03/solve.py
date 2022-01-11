from collections import defaultdict

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    instructions = f.read().strip()


movements = {
    '>': complex(1, 0),
    '<': complex(-1, 0),
    '^': complex(0, -1),
    'v': complex(0, 1),
}

def traverse(instructions, counts):
    location = complex(0, 0)
    for instruction in instructions:
        location += movements[instruction]
        counts[location] += 1

# Part 1
counts = defaultdict(int)
traverse(instructions, counts)
solution(len(counts))

# Part 2
counts = defaultdict(int)
traverse(instructions[::2], counts)
traverse(instructions[1::2], counts)

solution(len(counts))