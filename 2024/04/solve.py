import pathlib

from aoc import solution
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(list(map(list, pathlib.Path(filename).read_text().splitlines(keepends=False))), dtype='str')

# Part 1
search_word = 'XMAS'
s = 0

for i in range(board.shape[0]):
    for j in range(board.shape[1]):
        for row_offset in (-1, 0, 1):
            for col_offset in (-1, 0, 1):
                if row_offset == 0 and col_offset == 0:
                    continue
                row = i
                col = j
                word = ''
                while 0 <= row < board.shape[0] and 0 <= col < board.shape[1]:
                    word += board[row, col]
                    if word == search_word:
                        s += 1
                    row += row_offset
                    col += col_offset

solution(s)

# Part 2
search_word = 'MAS'

s = 0
for i in range(board.shape[0] - 2):
    for j in range(board.shape[1] - 2):
        subarray = board[i:i+3, j:j+3]
        d1 = ''.join(np.diagonal(subarray))
        d2 = ''.join(np.diagonal(np.fliplr(subarray)))

        if d1 in (search_word, search_word[::-1]) and d2 in (search_word, search_word[::-1]):
            s += 1
            if debug:
                print(subarray)
                print(d1, d2)
                print('')

solution(s)