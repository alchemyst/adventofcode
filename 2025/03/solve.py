from aoc import solution

debug = False
filename = "test.txt" if debug else "input.txt"

with open(filename) as f:
    lines = f.read().splitlines(keepends=False)


# Part 1
def max_joltage(line, length=2):
    positions = list(range(len(line)))
    position_value = {i: int(v) for i, v in enumerate(line)}

    sol = []
    start = 0
    for digits in range(length):
        sol.append(
            max(
                positions[start : len(line) - length + digits + 1],
                key=position_value.get,
            )
        )
        start = sol[-1] + 1

    return int("".join(line[p] for p in sol))


solution(sum(max_joltage(line) for line in lines))

# Part 2
solution(sum(max_joltage(line, 12) for line in lines))
