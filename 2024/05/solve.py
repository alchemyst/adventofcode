from graphlib import TopologicalSorter
from collections import defaultdict

import aoc.parse
from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

orders = []
updates = []
with open(filename) as f:
    for line in f:
        if line == '\n':
            break
        orders.append(aoc.parse.all_numbers(line))

    for line in f:
        updates.append(aoc.parse.all_numbers(line))

# Part 1
s = 0
incorrect = []
for update in updates:
    for i in range(len(update)):
        before, item, after = set(update[:i]), update[i], set(update[i+1:])
        must_be_before = set()
        must_be_after = set()
        for spec_before, spec_after in orders:
            if spec_after == item:
                must_be_before.add(spec_before)
            if spec_before == item:
                must_be_after.add(spec_after)

        # before must be a subset of must_be_before
        if not (before <= must_be_before):
            incorrect.append(update)
            break
        # after must be a subset of must_be_after
        if not (after <= must_be_after):
            incorrect.append(update)
            break
        # before must not have elements in must be_after
        if before & must_be_after:
            incorrect.append(update)
            break
        # after must not have elements in must be_before
        if after & must_be_before:
            incorrect.append(update)
            break
    else:
        s += update[len(update)//2]

solution(s)

# Part 2

s = 0
for update in incorrect:
    graph = defaultdict(list)
    for before, after in orders:
        if before in update and after in update:
            graph[after].append(before)
    sorter = TopologicalSorter(graph)
    order = list(sorter.static_order())

    correct_order = [item for item in order if item in update]
    s += correct_order[len(correct_order)//2]

solution(s)