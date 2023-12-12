from aoc import solution
from aoc.parse import all_numbers
from itertools import groupby
from functools import cache

debug = False
filename = 'test.txt' if debug else 'input.txt'

cases = []

with open(filename) as f:
    lines = f.read().splitlines(keepends=False)
    for line in lines:
        condition, group_string = line.split()
        groups = tuple(all_numbers(group_string))
        cases.append((condition, groups))



@cache
def find_groups(condition):
    return tuple(len(list(group)) for symbol, group in groupby(condition) if symbol == '#')


@cache
def search(condition, groups, hash_budget=None):
    condition = condition.strip('.')

    if not condition:
        return 0

    if hash_budget is None:
        hash_budget = sum(groups) - condition.count('#')

    if hash_budget == 0:
        condition = condition.replace('?', '.')

    first_unknown = condition.find('?')

    if first_unknown == -1:
        return int(groups == find_groups(condition))

    dot = condition[:first_unknown].rfind('.')

    if dot != -1:
        static_part = condition[:dot]
        static_groups = find_groups(static_part)
        if static_groups != groups[:len(static_groups)]:
            return 0
        condition = condition[dot:]
        groups = groups[len(static_groups):]


    return sum(
        search(condition.replace('?', symbol, 1), groups, hash_budget - (symbol == "#"))
        for symbol in '#.'
    )


# Part 1
solution(sum(search(condition, groups) for condition, groups in cases))

# Part 2
def unfold(case):
    condition, groups = case
    return '?'.join([condition]*5), groups*5


unfolded_cases = [unfold(case) for case in cases]

solution(sum(search(condition, groups) for condition, groups in unfolded_cases))
