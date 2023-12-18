from aoc import solution
import parse

from aoc.lattice_geometry import LatticePolygon

debug = False
plot = False
filename = "test.txt" if debug else "input.txt"

instruction_pattern = parse.compile("{} {:d} (#{})")

directions = {
    "U": complex(-1, 0),
    "D": complex(1, 0),
    "L": complex(0, -1),
    "R": complex(0, 1),
}

instructions = []
with open(filename) as f:
    for line in f:
        instructions.append(tuple(instruction_pattern.parse(line.strip())))


# Part 1
trench = LatticePolygon()
trench.add(0, 0)

location = 0
for direction, steps, color in instructions:
    for s in range(steps):
        location += directions[direction]
        trench.add(location.real, location.imag)

assert trench.closed()

solution(trench.total_points())

# Part 2
trench = LatticePolygon()
trench.add(0, 0)

location = 0
for _, _, color in instructions:
    distance = int(color[:5], 16)
    location += distance * directions["RDLU"[int(color[-1])]]
    trench.add(location.real, location.imag)

assert trench.closed()

solution(trench.total_points())
