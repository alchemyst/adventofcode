from graphlib import TopologicalSorter
from collections import defaultdict

import more_itertools

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

    return tuple(TopologicalSorter(graph).static_order())

def midway(update):
    return update[len(update)//2]

# Part 1
correct_orders = [order(update) for update in updates]
incorrect, correct = more_itertools.partition(lambda x: x[0] == x[1], zip(updates, correct_orders))

solution(sum(midway(update) for update, _ in correct))

# Part 2
solution(sum(midway(corrected) for _, corrected in incorrect))