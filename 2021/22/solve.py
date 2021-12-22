from itertools import product
from octtree import Cube
from aoc import solution
from rich.progress import track


def parse(filename):
    instructions = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            onoff, rest = line.split(maxsplit=1)
            numbers = []
            for pair in rest.split(','):
                rhs = pair.split('=')[1]
                parts = rhs.split('..')
                numbers += [int(p) for p in parts]

            instruction = (onoff, *numbers)
            instructions.append(instruction)

    return instructions


# Part 1
def inclusive_range(rfrom, rto):
    if rfrom > rto:
        rfrom, rto = rto, rfrom
    return range(rfrom, rto+1)

def outside(rrange):
    memory_size = 50
    rfrom, rto = rrange
    return (rfrom < -memory_size and rto < -memory_size) or (rfrom > memory_size and rto > memory_size)

def part1(filename):
    instructions = parse(filename)
    memory = {}
    for onoff, *coords in instructions:
        xfrom, xto, yfrom, yto, zfrom, zto = coords
        xrange = inclusive_range(xfrom, xto)
        yrange = inclusive_range(yfrom, yto)
        zrange = inclusive_range(zfrom, zto)

        number = 1 if onoff == 'on' else 0

        if any(outside(rrange) for rrange in ((xfrom, xto), (yfrom, yto), (zfrom, zto))):
            continue

        for location in product(xrange, yrange, zrange):
            memory[location] = number

    solution(sum(memory.values()))

# Part 2

def part2(filename):
    instructions = parse(filename)

    # Find outer dimensions
    # we follow Python convention for coordinate
    # | 0 | 1 | 2 |   <- cells
    # 0   1   2   3   <- coordinates
    xfrom, xto, yfrom, yto, zfrom, zto = zip(*(coords for _, *coords in instructions))
    xmin = min(xfrom)
    xmax = max(xto)
    ymin = min(yfrom)
    ymax = max(yto)
    zmin = min(zfrom)
    zmax = max(zto)

    world = Cube(xmin, xmax+1, ymin, ymax+1, zmin, zmax+1, value=0, children=[])
    print(f'{world=}')
    for onoff, xfrom, xto, yfrom, yto, zfrom, zto in track(instructions):
        if xfrom > xto:
            xfrom, xto = xto, xfrom
        if yfrom > yto:
            yfrom, yto = yto, yfrom
        if zfrom > zto:
            zfrom, zto = zto, zfrom
        value = 1 if onoff == 'on' else 0
        other = Cube(xfrom, xto+1, yfrom, yto+1, zfrom, zto+1, value=value, children=[])
        print(other)
        world.add(other)

    solution(world.valuesum())

if __name__ == '__main__':
    debug = False
    filename = 'test.txt' if debug else 'input.txt'
    part1(filename)

    filename = 'test2.txt' if debug else 'input.txt'
    part2(filename)