import json
from dataclasses import dataclass
from itertools import count

import networkx as nx
from aoc import solution
from aoc.array import neighbours

import numpy as np
import matplotlib.pyplot as plt

debug = False
plot = False
save = True
filename = 'test.txt' if debug else 'input.txt'

directions = {
    '<': np.array((-1, 0)),
    '>': np.array((+1, 0)),
    'v': np.array((0, 1)),
    '^': np.array((0, -1)),
}


def read(filename):
    blizzards = []
    with open(filename) as f:
        for y, line in enumerate(f, -1):
            if y == -1 or line.startswith("##"):
                continue
            for x, c in enumerate(line.strip()[1:]):
                if c not in '.#':
                    blizzards.append((c, np.array([x, y])))

    start = 0, -1
    end = x-1, y

    board_size = (x, y)

    return blizzards, board_size, start, end


def simulate(blizzards, board_size):
    new_blizzards = []
    for direction, position in blizzards:
        new_blizzards.append(
            (direction, (position + directions[direction]) % board_size)
        )

    return new_blizzards


def plot_board(blizzards, board_size, start, end):
    fig, ax = plt.subplots(figsize=(20, 7))
    bsx, bsy = board_size
    ax.plot(
        np.array([0, bsx, bsx, 0, 0]) - 0.5,
        np.array([0, 0, bsy, bsy, 0]) - 0.5,
    )
    for b, (bx, by) in blizzards:
        ax.text(bx, by, b)
    ax.plot(*start, 'gs')
    ax.plot(*end, 'rx')
    ax.invert_yaxis()
    ax.axis('off')


def add_nodes(board, g, previous_board, t):
    # Start node
    if previous_board[0, 0] == 0:
        g.add_edge(start_node, (t - 1, 0, 0))
        g.add_edge((t - 1, 0, 0), start_node)
    # End node?
    if previous_board[-1, -1] == 0:
        g.add_edge((t - 1, board_width - 1, board_height - 1), end_node)
        g.add_edge(end_node, (t - 1, board_width - 1, board_height - 1))
    # time connectivity
    for x, y in zip(*np.nonzero(previous_board == 0)):
        for otherx, othery in neighbours(board, x, y, diag=False, self=True):
            if board[otherx, othery] == 0:
                g.add_edge((t - 1, x, y), (t, otherx, othery))
        if plot:
            plt.plot(x, y, 'r.')


def render(blizzards, board_size):
    # find open positions
    board = np.zeros(board_size)
    for _, pos in blizzards:
        board[tuple(pos)] += 1
    return board


def shortest_path(blizzards, previous_board, source, target, start_t):
    g = nx.DiGraph()

    for t in count(start_t):
        blizzards = simulate(blizzards, board_size)

        board = render(blizzards, board_size)

        if plot:
            plot_board(blizzards, board_size, start, end)
            plt.imshow(board.T)
        if save:
            save_blizzards(blizzards, t)

        add_nodes(board, g, previous_board, t)

        previous_board = board

        if start_node in g.nodes() and end_node in g.nodes() and nx.has_path(g, source, target):
            if save:
                save_path(g, source, t, target)
            break

    return t, blizzards, previous_board


def save_blizzards(blizzards, t):
    with open(f'output/blizzards_{t:03d}.json', 'w') as f:
        json.dump(
            [
                [direction, tuple(map(int, position))]
                for direction, position in blizzards],
            f
        )


def save_path(g, source, t, target):
    with open(f'output/path_{t:03d}.json', 'w') as f:
        json.dump(
            [[int(part) for part in node]
             for node in nx.shortest_path(g, source, target)
             ],
            f,
        )


if __name__ == '__main__':
    # simulate blizzards, we build a graph showing connections between row, col, time
    # Then shortest path

    blizzards, board_size, start, end = read(filename)
    board_width, board_height = board_size

    start_node = tuple(start)
    end_node = tuple(end)

    if plot:
        plt.show()

    # Part 1
    previous_board = np.ones(board_size)
    t, blizzards, previous_board = shortest_path(blizzards, previous_board, start_node, end_node, 1)
    solution(t)

    # Part 2
    t, blizzards, previous_board = shortest_path(blizzards, previous_board, end_node, start_node, t)
    t, blizzards, previous_board = shortest_path(blizzards, previous_board, start_node, end_node, t)
    solution(t)

    if save:
        with open('output/parameters.json', 'w') as f:
            json.dump({
                "board_size": board_size,
                "start": start_node,
                "end": end_node,
            }, f)
