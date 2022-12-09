from aoc import solution, print_board
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

vectors = {
    'U': 1j,
    'D': -1j,
    'L': -1,
    'R': 1,
}

instructions = []
with open(filename) as f:
    for line in f:
        direction, step_str = line.strip().split()
        steps = int(step_str)

        instructions.append((direction, steps))

# def board(head, tail):
#     size = 6
#     b = np.zeros((size, size), dtype=str)
#     b[:, :] = '.'
#
#     b[int(size-tail.imag-1), int(tail.real)] = 'T'
#     b[int(size-head.imag-1), int(head.real)] = 'H'
#
#     return b

head = 0 + 0j
tail = head
tail_history = {tail}

# if debug:
#     print_board(board(head, tail), type='s')
#     print()
for direction, steps in instructions:
    for _ in range(steps):
        head += vectors[direction]
        taildiff = head - tail

        if abs(taildiff.real) > 1 or abs(taildiff.imag) > 1:  # not adjacent
            tailstep = np.sign(taildiff.imag)*1j + np.sign(taildiff.real)
        else:
            tailstep = 0

        tail += tailstep

        # if debug:
        #     print_board(board(head, tail), type='s')
        #     print()
        tail_history.add(tail)


# Part 1
solution(len(tail_history))

rope = [0 + 0j]*10
tail_history = {0 + 0j}

# if debug:
#     print_board(board(head, tail), type='s')
#     print()
for direction, steps in instructions:
    for _ in range(steps):
        rope[0] += vectors[direction]
        for i in range(1, len(rope)):
            head = rope[i-1]
            tail = rope[i]

            taildiff = head - tail

            if abs(taildiff.real) > 1 or abs(taildiff.imag) > 1:  # not adjacent
                tailstep = np.sign(taildiff.imag)*1j + np.sign(taildiff.real)
            else:
                tailstep = 0

            rope[i] += tailstep

        tail_history.add(rope[i])

# Part 2
solution(len(tail_history))