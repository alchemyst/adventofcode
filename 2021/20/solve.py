from collections import defaultdict

import numpy as np
import rich
from matplotlib import pyplot as plt

from aoc import solution, print_board

debug = False
filename = 'test.txt' if debug else 'input.txt'

chars = {
    '#': 1,
    '.': 0,
}

displaymap = {
    1: '#',
    0: '.',
}

class Image:
    def __init__(self, other, shape, generation=0):
        self.shape = shape
        self.generation = generation
        self.pixels = defaultdict(int)
        self.pixels.update(other)
        self.mini = min(i for i, _ in self.pixels)
        self.maxi = max(i for i, _ in self.pixels)
        self.minj = min(j for i, j in self.pixels)
        self.maxj = max(j for i, j in self.pixels)

    def subregion(self, i, j):
        result = []
        for ii in [-1, 0, 1]:
            result.append([self.pixels[i + ii, i + jj] for jj in [-1, 0, 1]])

        return result

    def decode(self, i, j):
        pixels = []
        for ii in [-1, 0, 1]:
            for jj in [-1, 0, 1]:
                pixels.append(self.pixels[i + ii, j + jj])

        return int(''.join(str(i) for i in pixels), 2)

    def array(self):
        shapei, shapej = self.shape
        generation = self.generation
        arr = np.zeros((shapei + generation*2, shapej + generation*2))
        for (i, j), value in np.ndenumerate(arr):
            arr[i, j] = self.pixels[i - generation, j - generation]

        return arr

    def full_array(self):
        result = []
        for i in range(self.mini, self.maxi+1):
            row = []
            for j in range(self.minj, self.maxj+1):
                row.append(self.pixels[i, j])
            result.append(row)
        return np.array(result)

    def show(self):
        show(self.array())

    def apply(self, algorithm):
        buffer = 110
        ones = []
        shapei, shapej = self.shape
        generation = self.generation
        for i in range(-buffer-self.generation, shapei + buffer + generation):
            for j in range(-buffer - self.generation, shapej + buffer + generation):
                newpixel = algorithm[self.decode(i, j)]
                if newpixel:
                    ones.append([(i, j), 1])
        return Image(ones, self.shape, self.generation+1)

    def copy(self):
        return Image(self.pixels.items(), self.shape, self.generation)

    def lit(self):
        return int(self.array().sum())


def readline(line):
    return list(map(chars.get, line.strip()))


def parse(filename):
    image = []
    with open(filename) as f:
        algorithm = readline(next(f))
        next(f)
        for line in f:
            image.append(readline(line))
    return np.array(image), algorithm


def show(image):
    print_board(image, lookup=displaymap, type='s')
    print()


rawimage, algorithm = parse(filename)
image = Image(dict((loc, value) for loc, value in np.ndenumerate(rawimage) if value), rawimage.shape)

def apply_enhance(times):
    newimage = image.copy()

    for i in range(times):
        print(i)
        newimage = newimage.apply(algorithm)

    return newimage

# Part 1
newimage = apply_enhance(2)
solution(newimage.lit())

# Part 2
newimage = apply_enhance(50)
plt.imshow(newimage.full_array())
plt.show()
solution(newimage.lit())