from itertools import product
from typing import Generator, Tuple, Any


def read_board(filename, converter=None):
    """Read a file containing a rectangular array of characters

    returns a nested list of characters
    """
    with open(filename) as f:
        lines = f.read().splitlines()

    if converter is None:
        return list(map(list, lines))
    else:
        return [[converter(c) for c in line] for line in lines]

def neighbours(
        arr,
        i: int,
        j: int,
        self: bool=False,
        simple: bool=True,
        diag: bool=False,
        values: bool=False,
        deltas: bool=False,
        stepsize: int=1,
) -> Generator[Tuple[int, int] | Any, None, None]:
    """
    Return the locations or values of the neighbours of an element in an array

    :param arr: the array
    :param i: center row location
    :param j: center column location
    :param self: include (i, j) in return
    :param simple: include up/down left/right
    :param diag: include sideways
    :return: iterator of (row, col) or iterator of arr[row, col]
    """
    maxi, maxj = arr.shape
    for di, dj in product([-stepsize, 0, stepsize], repeat=2):
        ri = i + di
        rj = j + dj
        if 0 <= ri < maxi and 0 <= rj < maxj:
            if (di == 0 and dj == 0) and not self:
                continue
            if (di != 0 and dj != 0) and not diag:
                continue
            if (di == 0 or dj == 0) and not simple:
                continue

            if values:
                yield arr[ri, rj]
            elif deltas:
                yield di, dj
            else:
                yield ri, rj


def on_board(board, i, j):
    rows = len(board)
    cols = len(board[0])

    return 0 <= i < rows and 0 <= j < cols