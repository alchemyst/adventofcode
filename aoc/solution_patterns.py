from math import prod

def sum_every(f, iterable):
    return sum(f(line) for line in iterable)

def prod_every(f, iterable):
    return prod(f(line) for line in iterable)
