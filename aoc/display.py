import rich
import rich.text
import numpy as np

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
