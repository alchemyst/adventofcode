#!/usr/bin/env python

from collections import Counter

group = []
groups = [group]

for line in open('input.txt'):
    line = line.strip()

    if not line:
        group = []
        groups.append(group)
        continue

    group.append(line)

sumunique = 0
sumall = 0
for group in groups:
    unique = set(''.join(group))
    sumunique += len(unique)

    counts = Counter()
    for response in group:
        uniqueresponse = set(response)
        counts.update(uniqueresponse)

    for question, count in counts.items():
        if count == len(group):
            sumall += 1

print(sumunique)
print(sumall)