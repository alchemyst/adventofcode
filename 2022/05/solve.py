from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'


def pad(l, n, v):
    for i in range(n):
        if i < len(l):
            yield l[i]
        else:
            yield v


def read_file(filename):
    crates = []
    with open(filename) as f:
        for line in f:
            if line.strip().startswith('1'):
                continue
            if not line.strip():
                break

            crates.append(list(line[1::4]))

        spaces = max(len(c) for c in crates)
        if debug: print(spaces)
        crates = [list(pad(l, spaces, ' ')) for l in crates]
        piles = [[item for item in c[::-1] if item != ' '] for c in zip(*crates)]

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