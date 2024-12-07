import itertools
from operator import add, mul
from aoc import solution
import aoc.parse

debug = False
filename = 'test.txt' if debug else 'input.txt'

equations = [aoc.parse.all_numbers(line) for line in aoc.parse.read_splitlines(filename)]


def possible(target, nums, operators):
    op_combos = itertools.product(operators, repeat=len(nums)-1)
    for ops in op_combos:
        total = nums[0]
        for num, op in zip(nums[1:], ops):
            total = op(total, num)
            if total > target:
                break
        if total == target:
            return True

    return False


def solve(equations, operators):
    return sum(target for target, *nums in equations if possible(target, nums, operators))


# Part 1
solution(solve(equations, (add, mul)))

# Part 2
def concatenate(a, b):
    return int(f'{a}{b}')

solution(solve(equations, (add, mul, concatenate)))