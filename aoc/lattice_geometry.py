import numpy as np


class LatticePolygon:
    def __init__(self):
        self.points = []

    def add(self, x, y):
        self.points.append((int(x), int(y)))

    def closed(self):
        return self.points[0] == self.points[-1]

    def boundary_points(self):
        """Lattice points on boundary"""
        x, y = zip(*self.points)

        dx = np.abs(np.diff(x))
        dy = np.abs(np.diff(y))
        n = np.gcd(dx, dy).sum()

        return n

    def area(self):
        # Shoelace formula for area of polygon
        x, y = zip(*self.points)
        return np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))/2

    def internal_points(self):
        """Count the number of lattice points internal to the polygon"""
        # Pick's formula says
        # A = i + b/2 - 1
        # so

        return int(self.area() - self.boundary_points() / 2) + 1

    def total_points(self):
        return self.boundary_points() + self.internal_points()
