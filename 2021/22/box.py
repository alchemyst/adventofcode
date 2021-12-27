from dataclasses import dataclass
from itertools import product
from typing import List, Tuple


def range_overlap(afrom, ato, bfrom, bto):
    if ato < bfrom or afrom > bto:
        return None
    rfrom = max(afrom, bfrom)
    rto = min(ato, bto)

    if rfrom < rto:
        return rfrom, rto
    else:
        return None

@dataclass
class Box:
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def ranges(self):
        return (self.xmin, self.xmax), (self.ymin, self.ymax), (self.zmin, self.zmax)

    def coords(self) -> Tuple:
        return self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax

    def vertices(self):
        return tuple(product(*self.ranges()))

    def contains(self, point):
        return all(f <= c <= t for c, (f, t) in zip(point, self.ranges()))

    def inside(self, other):
        return all(other.contains(v) for v in self.vertices())

    def outside(self, other):
        return not any(other.contains(v) for v in self.vertices())

    def size(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin) * (self.zmax - self.zmin)

    def cut(self, position, axis):
        coords = self.coords()
        minpos, maxpos = coords[axis*2:axis*2+2]
        if minpos < position < maxpos:
            boxes = []
            newcoords = list(coords)
            newcoords[axis*2] = position
            boxes.append(Box(*newcoords))

            newcoords = list(coords)
            newcoords[axis*2+1] = position
            boxes.append(Box(*newcoords))

            return boxes
        if maxpos <= position or position <= minpos:
            # completely outside cut position
            # | ###    or | ###
            return [self]

    def split(self, other):
        coords = other.coords()
        all_parts = [self]
        for axis in range(3):
            for positioni in range(2):
                position = coords[axis*2 + positioni]
                new_parts = []
                for box in all_parts:
                    for new_box in box.cut(position, axis):
                        new_parts.append(new_box)
                all_parts = new_parts

        return all_parts