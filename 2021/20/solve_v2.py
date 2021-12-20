import numpy as np
from scipy import ndimage
from rich.progress import track
from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

chars = {
    '#': 1,
    '.': 0,
}

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


def lookup(values):
    string = ''.join(str(int(value)) for value in values)
    return algorithm[int(string, 2)]


def enhance(image, outside):
    return ndimage.generic_filter(image, lookup, size=3, mode='constant', cval=outside)


def apply_enhance(times):
    newimage = np.pad(image, times*2)

    for i in track(range(times), description='Enhancing'):
        newimage = enhance(newimage, outside=0)

    return newimage[times:-times, times:-times]


image, algorithm = parse(filename)

# Part 1
newimage = apply_enhance(2)
solution(newimage.sum())

# Part 2
newimage = apply_enhance(50)
solution(newimage.sum())