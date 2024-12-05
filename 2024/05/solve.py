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

def order(update):
    graph = defaultdict(list)
    for before, after in orders:
        if before in update and after in update:
            graph[after].append(before)
    sorter = TopologicalSorter(graph)
    return tuple(item for item in sorter.static_order() if item in update)

# Part 1
s = 0
incorrect = []
for update in updates:
    correct_order = order(update)
    if update == correct_order:
        s += update[len(update)//2]
    else:
        incorrect.append(update)

solution(s)

# Part 2
s = 0
for update in incorrect:
    correct_order = order(update)
    s += correct_order[len(correct_order)//2]

solution(s)