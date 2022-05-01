import json

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

def intvalues(doc, skipred=False):
    if isinstance(doc, int):
        yield doc
    elif isinstance(doc, list):
        for d in doc:
            yield from intvalues(d, skipred=skipred)
    elif isinstance(doc, dict):
        if not skipred or 'red' not in doc.values():
            for v in doc.values():
                yield from intvalues(v, skipred=skipred)

with open(filename) as f:
    document = json.load(f)

# Part 1
solution(sum(intvalues(document)))

# Part 2
solution(sum(intvalues(document, skipred=True)))