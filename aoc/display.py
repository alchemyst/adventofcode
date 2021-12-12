import rich
import rich.text


def print_board(array, highlight=None, length=1):
    if highlight is None:
        highlight = np.zeros_like(array, dtype=bool)
    for i, row in enumerate(array):
        for j, value in enumerate(row):
            text = rich.text.Text(f'{value:{length}d}')
            if highlight[i, j]:
                text.stylize(style='bold magenta')
            rich.print(text, end='')
        rich.print()
