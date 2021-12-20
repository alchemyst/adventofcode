import time

import rich
import rich.text
import numpy as np

STATS = {'start': time.perf_counter(), 'times': []}

def print_board(array, highlight=None, length=1, lookup=None, type='d'):
    if highlight is None:
        highlight = np.zeros_like(array, dtype=bool)
    for i, row in enumerate(array):
        for j, value in enumerate(row):
            if lookup:
                v = lookup[value]
            else:
                v = value
            text = rich.text.Text(f'{v:{length}{type}}')
            if highlight[i, j]:
                text.stylize(style='bold magenta')
            rich.print(text, end='')
        rich.print()


def solution(value):
    start = STATS['start']
    elapsed = time.perf_counter() - start
    STATS['times'].append(elapsed)
    part = len(STATS['times'])
    print(f"Part {part} ({elapsed:.02f} s):", value)

