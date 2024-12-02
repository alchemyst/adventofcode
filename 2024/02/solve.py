import aoc.parse
from aoc import solution
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

reports = [aoc.parse.all_numbers(line) for line in aoc.parse.read_splitlines(filename)]

def is_safe(report):
    diffs = np.diff(report)
    signs = np.sign(diffs)
    abs_diffs = np.abs(diffs)

    return (signs[0] == signs).all() and (abs_diffs <= 3).all() and (abs_diffs >= 1).all()


# Part 1
solution(aoc.solution_patterns.sum_every(is_safe, reports))

# Part 2
def is_safe_with_deletion(report):
    if is_safe(report):
        return True

    return any(is_safe(report[:i] + report[i+1:]) for i in range(len(report)))

solution(aoc.solution_patterns.sum_every(is_safe_with_deletion, reports))