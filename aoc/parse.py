import re

numbers = re.compile('[0-9]+')


def read_splitlines(filename):
    with open(filename) as f:
        return f.read().splitlines()


def all_numbers(line):
    return tuple(int(n) for n in numbers.findall(line))
