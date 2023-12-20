import math
from collections import defaultdict
from dataclasses import dataclass

from aoc import solution
import parse

debug = False
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

    def split(self, op, rhs):
        match op:
            case '>':
                if self.lower <= rhs < self.upper:
                    return (
                        Range(max(self.lower, rhs + 1), self.upper),
                        Range(self.lower, min(self.upper, rhs)),
                    )
                elif rhs >= self.upper:
                    return None, self
                else:
                    return self, None
            case '<':
                if self.lower < rhs <= self.upper:
                    return (
                        Range(self.lower, min(self.upper, rhs - 1)),
                        Range(min(self.upper, rhs), self.upper)
                    )
                elif rhs <= self.lower:
                    return None, self
                else:
                    return self, None

    def is_valid(self):
        return self.lower <= self.upper

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

left, right = r1.split('<', 5)
assert left == Range(1, 4)
assert right == Range(5, 10)

left, right = r1.split('<', 1)
assert left is None
assert right == r1

left, right = r1.split('<', 100)
assert left == r1
assert right is None

left, right = r1.split('>', 5)
assert left == Range(6, 10)
assert right == Range(1, 5)

left, right = r1.split('>', 1)
assert left == Range(2, 10)
assert right == Range(1, 1)

left, right = r1.split('>', 0)
assert left == r1
assert right is None

left, right = r1.split('>', 100)
assert left is None
assert right == r1


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

assert r1 != r2

assert r1 == r1

locations = defaultdict(list)
locations['in'] = [{v: Range(1, 4000) for v in 'xmas'}]

while True:
    for workflow, allowed_values in list(locations.items()):
        if workflow in {'A', 'R'}:
            continue

        locations[workflow] = []
        for current_value in allowed_values:
            for rule in workflows[workflow]:
                match rule:
                    case expr, next_state:
                        variable, op, rhs = expr_pattern.parse(expr)
                        new_value = current_value.copy()
                        routed, not_routed = new_value[variable].split(op, rhs)
                        if routed is not None:
                            new_value[variable] = routed
                            locations[next_state].append(new_value)
                        if not_routed is not None:
                            current_value[variable] = not_routed
                        else:
                            break
                    case [next_state]:
                        locations[next_state].append(current_value)

    active_locations = {l for l, v in locations.items() if len(v)}
    if active_locations == {'A', 'R'}:
        break

s = sum(math.prod(r.size() for r in location.values()) for location in locations['A'])

if debug:
    assert s == 167409079868000

solution(s)