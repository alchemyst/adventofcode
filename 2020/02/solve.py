#!/usr/bin/env python

import re

pattern = re.compile(r'(\d+)-(\d+) (.): (.*)')

c1 = 0
c2 = 0

for line in open('02/input.txt'):
    print(line)

    m = pattern.match(line.strip())
    lower, upper, char, password = m.groups()
    lower = int(lower)
    upper = int(upper)

    print(lower, upper, char, password)

    if lower <= password.count(char) <= upper:
        c1 += 1

    if (password[lower - 1] == char) ^ (password[upper - 1] == char):
        c2 += 1

print(c1)
print(c2)