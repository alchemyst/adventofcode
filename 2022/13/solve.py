from itertools import chain
from functools import cmp_to_key
from aoc import solution
from more_itertools import chunked
from pprint import pprint

debug = False
filename = 'test.txt' if debug else 'input.txt'

pairs = []
with open(filename) as f:
    for group in chunked(f, 3):
        pair = eval(group[0]), eval(group[1])
        pairs.append(pair)


def smaller(left, right):
    match left, right:
        case int(), int():
            return left - right
        case list(), list():
            for new_left, new_right in zip(left, right):
                s = smaller(new_left, new_right)
                if s != 0:
                    return s
            else:
                return len(left) - len(right)
        case int(), list():
            return smaller([left], right)
        case list(), int():
            return smaller(left, [right])
    return 0


right_order = [
    i for i, (left, right) in enumerate(pairs, 1)
    if smaller(left, right) < 0
]

# Part 1
solution(sum(right_order))

all_packets = list(chain.from_iterable(pairs))
dividers = [[[2]], [[6]]]
all_packets += dividers
all_packets.sort(key=cmp_to_key(smaller))

if debug:
    pprint(all_packets)

div1, div2 = (all_packets.index(d) + 1 for d in dividers)

# Part 2
solution(div1*div2)