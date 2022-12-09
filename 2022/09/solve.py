from aoc import solution
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

vectors = {
    'U': 1j,
    'D': -1j,
    'L': -1,
    'R': 1,
}

def read_instructions(filename):
    instructions = []
    with open(filename) as f:
        for line in f:
            direction, step_str = line.strip().split()
            steps = int(step_str)

            instructions.append((direction, steps))

    return instructions


def simulate(instructions, length):
    rope = [complex()]*length
    tail_history = {rope[-1]}

    for direction, steps in instructions:
        for _ in range(steps):
            rope[0] += vectors[direction]
            for i in range(1, len(rope)):
                diff = rope[i-1] - rope[i]

                if abs(diff) > 1:
                    step = np.sign(diff.imag)*1j + np.sign(diff.real)
                    rope[i] += step

            tail_history.add(rope[i])

    return len(tail_history)

instructions = read_instructions(filename)

# Part 1
solution(simulate(instructions, 2))

# Part 2
solution(simulate(instructions, 10))