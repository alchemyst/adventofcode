import numpy as np

DIRECTIONS = {
    '^': np.array([-1, 0]),
    'v': np.array([1, 0]),
    '<': np.array([0, -1]),
    '>': np.array([0, 1]),
}

CLOCKWISE = '^>v<'
COUNTER_CLOCKWISE = '^<v>'

def rotate(direction, clockwise_90_rotations):
    return CLOCKWISE[(CLOCKWISE.index(direction) + clockwise_90_rotations) % 4]