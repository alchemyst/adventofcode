from aoc import solution
import aoc.parse
import aoc.array
import networkx as nx
import numpy as np

debug = False
filename = 'test.txt' if debug else 'input.txt'
board_size = 6 if debug else 70
cutoff = 12 if debug else 1024

bytes = [aoc.parse.all_numbers(line) for line in aoc.parse.read_splitlines(filename)]

def board_graph(cutoff):
    board = np.zeros((board_size+1, board_size+1), dtype=bool)
    for x, y in bytes[:cutoff]:
        board[y, x] = True

    # if debug:
    #     aoc.print_board(board, type='d')

    graph = nx.Graph()

    for (y, x), value in np.ndenumerate(board):
        if value:
            continue
        for n_y, n_x in aoc.array.neighbours(board, y, x):
            nvalue = board[n_y, n_x]
            if nvalue:
                continue
            graph.add_edge((x, y), (n_x, n_y))

    return graph

# Part 1
solution(nx.shortest_path_length(board_graph(cutoff), (0, 0), (board_size, board_size)))

# Part 2
left = cutoff
right = len(bytes) - 1

while True:
    midpoint = (left + right) // 2
    graph = board_graph(midpoint)
    if nx.has_path(graph, (0, 0), (board_size, board_size)):
        left = midpoint
    else:
        right = midpoint

    if left == right - 1:
        break

solution(','.join(map(str, bytes[left])))