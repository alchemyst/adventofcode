import operator
from functools import cache
from scipy.optimize import fsolve

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

tree = {}
with open(filename) as f:
    for line in f:
        node, *parts = line.strip().split()
        node = node[:-1]

        if len(parts) == 1:
            v = int(parts[0])
            tree[node] = ('identity', v)
        else:
            left, op, right = parts
            tree[node] = (ops[op], left, right)


@cache
def evaluate1(node):
    match tree[node]:
        case 'identity', v:
            return v
        case op, left, right:
            return op(evaluate1(left), evaluate1(right))


# Part 1
s1 = evaluate1('root')
solution(s1)


# Part 2
@cache
def evaluate2(node, x):
    match node, tree[node]:
        case "humn", _:
            return x
        case "root", (_, left, right):
            return evaluate2(left, x) - evaluate2(right, x)
        case _, ('identity', v):
            return v
        case _, (op, left, right):
            return op(evaluate2(left, x), evaluate2(right, x))


def zerofunc(x):
    return evaluate2("root", float(x))

s2, = fsolve(zerofunc, s1)

solution(s2)