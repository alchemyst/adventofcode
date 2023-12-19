import math
import sys
from collections import defaultdict
from dataclasses import dataclass, replace

from aoc import solution
import parse

debug = True
filename = 'test.txt' if debug else 'input.txt'

blocks = open(filename).read().split('\n\n')

workflows = {}

instruction_pattern = parse.compile('{}{{{}}}')
for line in blocks[0].splitlines(keepends=False):
    name, rule_list = instruction_pattern.parse(line)
    workflows[name] = [rule.split(':') for rule in rule_list.split(',')]

parts = []
for line in blocks[1].splitlines(keepends=False):
    part = line[1:-1]
    parts.append(eval(f'dict({part})'))

accepted = []
for part in parts:
    state = 'in'
    while state not in {'A', 'R'}:
        for rule in workflows[state]:
            match rule:
                case expr, next_state:
                    if eval(expr, {}, part):
                        state = next_state
                        break
                case [next_state]:
                    state = next_state
                    break
    if state == 'A':
        accepted.append(part)

# Part 1
solution(sum(sum(part.values()) for part in accepted))

# Part 2
expr_pattern = parse.compile('{}{}{:d}')

@dataclass
class Range:
    lower: int
    upper: int

    def with_limit(self, op, rhs):
        match op:
            case '>':
                return Range(max(self.lower, rhs+1), self.upper)
            case '<':
                return Range(self.lower, min(self.upper, rhs-1))

    def intersection(self, other):
        lower = max(self.lower, other.lower)
        upper = min(self.upper, other.upper)

        if lower <= upper:
            return Range(lower, upper)

        return None

    def size(self):
        return self.upper - self.lower + 1

r1 = Range(1, 10)
assert r1.size() == 10

r2 = Range(11, 20)
assert r1.intersection(r2) is None

r3 = Range(5, 20)
assert r1.intersection(r3).size() == 6


@dataclass
class Region:
    dimensions: dict[str]

    def size(self):
        return math.prod(dim.size() for dim in self.dimensions.values())

    def intersection(self, other):
        new_dim = {}
        for d, dim in self.dimensions.items():
            dim_intersection = dim.intersection(other.dimensions[d])
            if dim_intersection is None:
                return None

            new_dim[d] = dim_intersection

        return Region(new_dim)

r1 = Region({'x': Range(1, 10), 'y': Range(1, 10)})
assert r1.size() == 100

r2 = Region({'x': Range(5, 20), 'y': Range(10, 10)})
assert r1.intersection(r2).size() == 6

r3 = Region({'x': Range(20, 30), 'y': Range(1, 10)})
assert r1.intersection(r3) is None


locations = defaultdict(list)
locations['in'] = [{v: Range(1, 4000) for v in 'xmas'}]

for i in range(20):
    for workflow, allowed_values in list(locations.items()):
        if workflow in {'A', 'R'}:
            continue

        locations[workflow] = []
        for allowed_value in allowed_values:
            for rule in workflows[workflow]:
                match rule:
                    case expr, next_state:
                        variable, op, rhs = expr_pattern.parse(expr)
                        new_value = allowed_value.copy()
                        new_value[variable] = new_value[variable].with_limit(op, rhs)
                        locations[next_state].append(new_value)
                    case [next_state]:
                        locations[next_state].append(allowed_value)


uniques = set(tuple((v, r.lower, r.upper) for v, r in allowed_value.items()) for allowed_value in locations['A'])


def add_region(regions, sign, region):
    this = sign, region
    if len(regions) == 0:
        return [this]

    intersections = []
    for other_sign, other_region in regions:
        intersection = region.intersection(other_region)
        if intersection is not None:
            intersections = add_region(intersections, -sign*other_sign, intersection)

    return regions + intersections + [this]


total_regions = []
for unique in uniques:
    region = Region({v: Range(lower, upper) for v, lower, upper in unique})
    total_regions = add_region(total_regions, 1, region)

s = sum(sign*region.size() for sign, region in total_regions)

print(s - 167409079868000)
solution(s)