#!/usr/bin/env python

import re
from collections import defaultdict

contents = defaultdict(dict)
fitsin = defaultdict(set)

for line in open('07/input.txt'):
    container, contains = line.strip().split(' contain ')
    container = ' '.join(container.split()[:2])

    for contain in contains.split(','):
        parts = contain.strip().split()
        if parts[0] == 'no':
            continue
        n = int(parts[0])
        bag = ' '.join(parts[1:3])

        contents[container][bag] = n
        fitsin[bag].add(container)

checklist = ['shiny gold']

answer_bags = set()

while checklist:
    bag_to_check = checklist.pop()
    fits = fitsin[bag_to_check]
    answer_bags.update(fits)
    checklist += fits

print(len(answer_bags))

def count_contents(container):
    if container not in contents:
        return 0

    total = 0
    for bag, n in contents[container].items():
        total += n*(1 + count_contents(bag))

    return total

print(count_contents('shiny gold'))