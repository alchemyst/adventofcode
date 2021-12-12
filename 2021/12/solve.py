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


def paths1(start, stop, pathsofar):
    if start == stop:
        yield pathsofar.copy()

    for cave in graph.neighbors(start):
        if smallcave(cave) and cave in pathsofar:
            continue
        yield from paths1(cave, stop, pathsofar + [cave])


def valid_visit(cave, pathsofar):
    if cave == 'start':
        return False
    if smallcave(cave):
        if cave not in pathsofar:
            return True
        smallcavecounts = Counter(c for c in pathsofar if smallcave(c) and c != 'start')
        if max(smallcavecounts.values(), default=0) == 2:
            return False

    return True


def paths2(start, stop, pathsofar):
    if start == stop:
        yield pathsofar
    else:
        for cave in graph.neighbors(start):
            if valid_visit(cave, pathsofar):
                yield from paths2(cave, stop, pathsofar + [cave])


graph = parse(filename)

allpaths = list(paths1('start', 'end', ['start']))

print('Part 1:', len(allpaths))

allpaths2 = list(paths2('start', 'end', ['start']))

print('Part 2:', len(allpaths2))
