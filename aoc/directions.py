import numpy as np

DIRECTIONS = {
    '^': np.array([-1, 0]),
    'v': np.array([1, 0]),
    '<': np.array([0, -1]),
    '>': np.array([0, 1]),
}