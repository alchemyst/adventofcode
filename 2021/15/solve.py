import networkx
import numpy as np
from aoc import print_board, solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

def parse(filename):
    data = []

    with open(filename) as f:
        for line in f:
            data.append([int(c) for c in line.strip()])

    return np.array(data)


def build_graph(board):
    maxi, maxj = board.shape

    graph = networkx.DiGraph()

    def add_edge(this, other):
        i, j = this
        ii, jj = other
        graph.add_edge(this, other, cost=board[ii, jj])
        graph.add_edge(other, this, cost=board[i, j])

    for (i, j), value in np.ndenumerate(board):
        pos = (i, j)
        if i > 0:
            add_edge(pos, (i - 1, j))
        if i < maxi - 1:
            add_edge(pos, (i + 1, j))
        if j > 0:
            add_edge(pos, (i, j - 1))
        if j < maxj - 1:
            add_edge(pos, (i, j + 1))

    return graph


def pathboard(path, board):
    highlight = np.zeros_like(board)

    i, j = zip(*path)
    highlight[i, j] = 1

    return highlight == 1


def solve(board):
    graph = build_graph(board)
    maxi, maxj = board.shape

    start, end = (0, 0), (maxi - 1, maxj - 1)

    shortest = networkx.shortest_path(
        graph, start, end,
        weight='cost',
    )

    i, j = zip(*shortest)
    cost = board[i, j].sum() - board[0, 0]

    if debug:
        print_board(board, pathboard(shortest, board))

    return cost

#  part 1
board = parse(filename)
solution(solve(board))

# Part 2
ii, jj = np.meshgrid(range(5), range(5))
shape = ii + jj
bigboard = (np.tile(board, (5, 5)) + np.kron(shape, np.ones_like(board)))
bigboard[bigboard > 9] -= 9
bigboard[bigboard > 9] -= 9

solution(solve(bigboard))
