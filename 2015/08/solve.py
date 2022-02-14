from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

with open(filename) as f:
    lines = [line.strip() for line in f]


# Part 1
def unescape(line):
    return eval(line)

original_chars = sum(len(line) for line in lines)
memory_chars = sum(len(unescape(line)) for line in lines)

solution(original_chars - memory_chars)

# Part 2
def escape(line):
    return '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '"'

escaped_chars = sum(len(escape(line)) for line in lines)

solution(escaped_chars - original_chars)