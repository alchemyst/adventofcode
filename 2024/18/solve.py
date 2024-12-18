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
while True:
    cutoff += 1
    print(cutoff)
    graph = board_graph(cutoff)
    if not nx.has_path(graph, (0, 0), (board_size, board_size)):
        break

solution(','.join(map(str, bytes[cutoff-1])))