from collections import Counter

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'


def parse(filename):
    with open(filename) as f:
        template = next(f).strip()
        next(f)
        rules = dict(line.strip().split(' -> ') for line in f)
    return template, rules


def pair_polymerize(pairs):
    newpairs = Counter()
    for pair, count in pairs.items():
        if pair in pair_rules:
            a, b = pair
            i = pair_rules[pair]
            newpairs[(a, i)] += count
            newpairs[(i, b)] += count
        else:
            newpairs[pair] = count
    return newpairs


def solve(steps):
    # polymerize
    pairs = Counter(zip(template, template[1:]))
    for i in range(steps):
        pairs = pair_polymerize(pairs)

    # Count
    counts = Counter()
    for (a, _), count in pairs.items():
        counts[a] += count
    # Tricky - you have to add the last item,
    # which will never change because you're always adding in the middle of two
    counts[template[-1]] += 1

    return max(counts.values()) - min(counts.values())


template, rules = parse(filename)
pair_rules = {tuple(rule): value for rule, value in rules.items()}

solution(solve(10))
solution(solve(40))
