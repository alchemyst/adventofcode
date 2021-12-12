import networkx as nx
from collections import Counter

debug = False
filename = 'test.txt' if debug else 'input.txt'


def parse(filename):
    graph = nx.Graph()

    with open(filename) as f:
        for line in f:
            if line.strip():
                start, stop = line.strip().split('-')
                graph.add_edge(start, stop)

    return graph


def smallcave(cave):
    return cave.lower() == cave


def traverse(start, stop, pathsofar, valid):
    if start == stop:
        yield pathsofar
    else:
        for cave in graph.neighbors(start):
            if valid(cave, pathsofar):
                yield from traverse(cave, stop, pathsofar + [cave], valid)


def valid_part_1(cave, pathsofar):
    return not (smallcave(cave) and cave in pathsofar)

def valid_part_2(cave, pathsofar):
    if cave == 'start':
        return False
    if smallcave(cave):
        if cave not in pathsofar:
            return True
        smallcavecounts = Counter(c for c in pathsofar if smallcave(c) and c != 'start')
        if max(smallcavecounts.values(), default=0) == 2:
            return False

    return True


graph = parse(filename)

allpaths = list(traverse('start', 'end', ['start'], valid_part_1))
print('Part 1:', len(allpaths))

allpaths2 = list(traverse('start', 'end', ['start'], valid_part_2))
print('Part 2:', len(allpaths2))
