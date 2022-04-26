from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = [line.strip() for line in f]

def countchars(func):
    return sum(len(func(line)) for line in lines)

def identity(x):
    return x

# Part 1
unescape = eval

original_chars = countchars(identity)
memory_chars = countchars(unescape)

solution(original_chars - memory_chars)

# Part 2
def escape(line):
    return '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '"'

escaped_chars = countchars(escape)

solution(escaped_chars - original_chars)