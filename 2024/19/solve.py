from aoc import solution
import pathlib
import re
import itertools

debug = False
filename = pathlib.Path('test.txt' if debug else 'input.txt')

patterns, designs = filename.read_text().split("\n\n")
patterns = patterns.split(", ")
designs = designs.split("\n")

patterns.sort(key=lambda x: len(x))

def matches(patterns, design):
    towel_matcher = re.compile("^(" + "|".join(p for p in patterns if p in design) + ")+$")
    return bool(towel_matcher.match(design))

print("Before", len(patterns))

while True:
    combopatterns = []
    for i in range(1, 2):
        for subset in itertools.combinations(patterns, i):
            # print(subset)
            for otherpattern in patterns:
                if otherpattern in subset:
                    continue
                if matches(subset, otherpattern):
                    combopatterns.append(otherpattern)
    for c in combopatterns:
        patterns.remove(c)
    if not combopatterns:
        break

print("After", len(patterns))


s = 0
for design in designs:
    s += matches(patterns, design)

# Part 1
solution(s)

# Part 2
solution('Dummy')