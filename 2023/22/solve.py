from dataclasses import dataclass, field
from functools import cache
from operator import attrgetter

import numpy as np

from aoc import solution
import parse

debug = False
filename = 'test.txt' if debug else 'input.txt'

brick_pattern = parse.compile('{:d},{:d},{:d}~{:d},{:d},{:d}')


@dataclass
class Brick:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int
    supported_by: set = field(default_factory=set)
    supporting: set = field(default_factory=set)

    def footprint(self):
        r = np.zeros((max_x + 1, max_y + 1), dtype=bool)
        r[self.x1:self.x2 + 1, self.y1:self.y2 + 1] = True

        return r

    def bottom(self):
        return self.z1

    def height(self):
        return self.z2 - self.z1 + 1

    def size(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)


bricks = []

with open(filename) as f:
    for line in f:
        brick = Brick(*brick_pattern.parse(line.strip()))
        assert brick.x1 <= brick.x2 and brick.y1 <= brick.y2 and brick.z1 <= brick.z2
        bricks.append(brick)

bricks.sort(key=attrgetter('z1'))
max_x = max(brick.x2 for brick in bricks)
max_y = max(brick.y2 for brick in bricks)


# Part 1
floor = np.zeros((max_x+1, max_y+1), dtype=np.int32)
top_bricks = -np.ones_like(floor)

settled_bricks = []

for i, brick in enumerate(bricks):
    footprint = brick.footprint()
    floor_max = floor[footprint].max()
    supporting_bricks = set(top_bricks[footprint & (floor == floor_max)]) - {-1}
    for supporting_brick in supporting_bricks:
        settled_bricks[supporting_brick].supporting.add(i)

    new_brick = Brick(brick.x1, brick.y1, floor_max + 1, brick.x2, brick.y2, floor_max + brick.height(), supported_by=supporting_bricks)
    assert brick.size() == new_brick.size()
    settled_bricks.append(new_brick)

    top_bricks[footprint] = i
    floor[footprint] = new_brick.z2

c = len(bricks) - sum(
    any(
        len(settled_bricks[supported_brick_i].supported_by) == 1
        for supported_brick_i in brick.supporting
    )
    for brick in settled_bricks
)

solution(c)

# part 2
def extra_fallen(i):
    fallens = {i}
    processing = True
    while processing:
        processing = False
        for fallen_i in list(fallens):
            fallen_brick = settled_bricks[fallen_i]
            for supported_brick_i in fallen_brick.supporting:
                if supported_brick_i in fallens:
                    continue

                supported_brick = settled_bricks[supported_brick_i]
                if supported_brick.supported_by and supported_brick.supported_by <= fallens:
                    fallens.add(supported_brick_i)
                    processing = True
    return len(fallens) - 1


solution(sum(extra_fallen(i) for i in (range(len(settled_bricks)))))

