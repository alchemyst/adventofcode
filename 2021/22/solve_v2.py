from solve import parse
from octtree import Box
from aoc import solution

debug = True
filename = 'test2.txt' if debug else 'input.txt'
# Convert to numbers and coordinates
instructions = [
    (1 if onoff == 'on' else 0, xmin, xmax+1, ymin, ymax+1, zmin, zmax + 1)
    for onoff, xmin, xmax, ymin, ymax, zmin, zmax in parse(filename)
]


def process(instructions):
    totalvalue = 0
    rounds = 0
    while instructions:
        print(f'{len(instructions)=}, {totalvalue=}')
        instruction, *rest = instructions
        value, *coords = instruction

        current = Box(*coords)
        # print(current)

        totalvalue += value*current.size()

        # if not rest:
        #     break

        new_instructions = []
        for othervalue, *othercoords in rest:
            # if there's no overlap we'll deal with that in the next round
            other = Box(*othercoords)
            # print(' ', other)
            # if other.outside(current):
            #     new_instructions.append([othervalue, *other.coords()])
            #     continue

            # otherwise split into parts and cut out the overlap
            for part in other.split(current):
                if part.inside(current) or part.size() == 0:
                    # print(' - ', part)
                    continue

                # print(' + ', part)
                new_instructions.append([othervalue, *part.coords()])

        instructions = new_instructions
        rounds += 1
        # if rounds > 5000:
        #     break

    return totalvalue

# instructions = [
#     (1, 5, 15, 5, 15, 5, 15),
#     (1, 0, 10, 0, 10, 0, 10),
# ]
#
count = process(list(reversed(instructions)))

solution(count)
