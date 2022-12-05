import itertools

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

def read_file(filename):
    layers = []
    with open(filename) as f:
        for line in f:
            if line.strip().startswith('1'):
                spaces = len(line.split())
                continue
            if not line.strip():
                break

            layers.append(list(line[1::4]))

        if debug:
            print(spaces)
            print(layers)

        layers = [l + [' ']*(spaces - len(l)) for l in layers]

        piles = [[item for item in c[::-1] if item != ' '] for c in zip(*layers)]

        if debug:
            print(piles)

        instructions = []
        for line in f:
            instructions.append(list(map(int, line.strip().split()[1::2])))

        if debug:
            print(instructions)
            print()

    return piles, instructions


def run(stack):
    piles, instructions = read_file(filename)

    stack(piles, instructions)

    top_crates = ''.join([p[-1] for p in piles])

    return top_crates


def stack1(piles, instructions):
    # number, from, to
    for n, f, t in instructions:
        for i in range(n):
            from_pile = piles[f - 1]
            to_pile = piles[t - 1]

            picked_up = from_pile.pop(len(from_pile)-1)
            to_pile.append(picked_up)

            if debug:
                print(piles)
                print()


# Part 1
solution(run(stack1))

def stack2(piles, instructions):
    # number, from, to
    for n, f, t in instructions:
        piles[f - 1], picked_up = piles[f - 1][:-n], piles[f - 1][-n:]
        piles[t - 1] += picked_up

        if debug:
            print(piles)
            print()


# Part 2
solution(run(stack2))