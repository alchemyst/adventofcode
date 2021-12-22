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
class Cube:
    xfrom: int
    xto: int
    yfrom: int
    yto: int
    zfrom: int
    zto: int
    value: int
    children: List["Cube"]

    def ranges(self):
        return (self.xfrom, self.xto), (self.yfrom, self.yto), (self.zfrom, self.zto)

    def coords(self):
        return self.xfrom, self.xto, self.yfrom, self.yto, self.zfrom, self.zto

    def valuesum(self):
        if self.children:
            return sum(child.valuesum() for child in self.children)

        if self.value == 0:
            return 0

        return (self.xto - self.xfrom)*(self.yto - self.yfrom)*(self.zto - self.zfrom)

    def vertices(self):
        return tuple(product(self.ranges()))

    def contains(self, point):
        return all(f <= c <= t for c, (f, t) in zip(point, self.ranges()))

    def subdivide(self):
        """Binary division into eight equal children"""
        xfrom, xto, yfrom, yto, zfrom, zto = self.coords()

        xmid = int((xto + xfrom)//2)
        ymid = int((yto + yfrom)//2)
        zmid = int((zto + zfrom)//2)

        def add_cube(x1, x2, y1, y2, z1, z2):
            if x1 == x2 or y1 == y2 or z1 == z2:
                return

            self.children.append(Cube(x1, x2, y1, y2, z1, z2, self.value, []))

        self.children = []
        add_cube(xfrom, xmid, yfrom, ymid, zfrom, zmid)
        add_cube(xfrom, xmid, yfrom, ymid, zmid, zto)
        add_cube(xfrom, xmid, ymid, yto, zfrom, zmid)
        add_cube(xfrom, xmid, ymid, yto, zmid, zto)
        add_cube(xmid, xto, yfrom, ymid, zfrom, zmid)
        add_cube(xmid, xto, yfrom, ymid, zmid, zto)
        add_cube(xmid, xto, ymid, yto, zfrom, zmid)
        add_cube(xmid, xto, ymid, yto, zmid, zto)

    def try_combine(self):
        if not self.children:
            return

        values = set()
        for child in self.children:
            child.try_combine()
            if child.children:
                break
            values.add(child.value)
        else:  # all children have no children
            if len(values) == 1:  # all children have the same value
                self.value, = values
                self.children = []

    def intersection(self, other):
        intx = range_overlap(self.xfrom, self.xto, other.xfrom, other.xto)
        inty = range_overlap(self.yfrom, self.yto, other.yfrom, other.yto)
        intz = range_overlap(self.zfrom, self.zto, other.zfrom, other.zto)

        if intx is None or inty is None or intz is None:
            return None

        return Cube(*intx, *inty, *intz, value=other.value, children=[])

    def equal(self, other):
        return self.coords() == other.coords()

    def add(self, other):
        if self.equal(other):
            self.value = other.value
            self.children = []
        else:
            if not self.children:
                self.subdivide()

            for child in self.children:
                overlap = child.intersection(other)
                if overlap:
                    child.add(overlap)

            # self.try_combine()


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