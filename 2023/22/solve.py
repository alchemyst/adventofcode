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
can_be_disintegrated = set()
uncovered_bricks = set()

for i, brick in enumerate(bricks):
    footprint = brick.footprint()
    floor_max = floor[footprint].max()
    supporting_bricks = set(top_bricks[footprint & (floor == floor_max)]) - {-1}
    uncovered_bricks -= supporting_bricks
    if len(supporting_bricks) > 1:
        can_be_disintegrated.update(supporting_bricks)
    for supporting_brick in supporting_bricks:
        settled_bricks[supporting_brick].supporting.add(i)

    uncovered_bricks.add(i)

    new_brick = Brick(brick.x1, brick.y1, floor_max + 1, brick.x2, brick.y2, floor_max + brick.height(), supported_by=supporting_bricks)
    assert brick.size() == new_brick.size()
    settled_bricks.append(new_brick)

    top_bricks[footprint] = i
    floor[footprint] = new_brick.z2

c = 0
for brick in settled_bricks:
    crucial = False
    for supported_brick_i in brick.supporting:
        supported_brick = settled_bricks[supported_brick_i]
        if len(supported_brick.supported_by) == 1:
            crucial = True
    if crucial:
        c += 1


solution(len(bricks) - c)


# Part 2
@cache
def extra_fallen(fallen_bricks):
    fallen_bricks = set(fallen_bricks)
    s = set()

    for i, brick in enumerate(settled_bricks):
        if i in fallen_bricks:
            continue

        if brick.supported_by and brick.supported_by <= fallen_bricks:
            s.add(i)
            s |= extra_fallen(tuple(fallen_bricks | {i}))

    return s

from tqdm.auto import tqdm

solution(sum(len(extra_fallen((i,))) for i in tqdm(range(len(settled_bricks)))))

