from collections import defaultdict
from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

sizes = defaultdict(int)

path = ['/']
with open(filename) as f:
    for line in f:
        match line.strip().split():
            case ['$', 'cd', '/']:
                path = ['/']
            case ['$', 'cd', '..']:
                path.pop()
            case ['$', 'cd', dirname]:
                path.append(dirname)
            case ['$', 'ls']:
                pass
            case ['dir', dirname]:
                pass
            case [size_str, _]:
                for i in range(len(path)):
                    sizes[tuple(path[:i + 1])] += int(size_str)

# Part 1
solution(sum(s for s in sizes.values() if s <= 100000))

# Part 2
total = 70000000
required = 30000000
current = sizes[('/',)]
unused = total - current
delete_required = required - unused
solution(min(s for s in sizes.values() if s >= delete_required))