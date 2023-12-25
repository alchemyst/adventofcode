import networkx as nx


import numpy as np

from aoc import solution
from aoc.array import read_board, neighbours

debug = False
plot = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(read_board(filename, int))

rows, cols = board.shape


def add(this, other):
    return (this[0]+other[0], this[1] + other[1])


def neg(t):
    return (-t[0], -t[1])


def create_directions(stepsize):
    return (
        (-stepsize, 0),
        (stepsize, 0),
        (0, -stepsize),
        (0, stepsize)
    )

def path_cost(board, this, other):
    t = np.array(this)
    o = np.array(other)
    delta = o - t
    direction = (delta/np.abs(delta).sum()).astype(int)

    here = t
    cost = 0
    while not (here == o).all():
        here += direction
        cost += board[tuple(here)]

    return cost


def solve(min_step, max_distance):
    directions = create_directions(1)

    graph = nx.DiGraph()

    for this, value in np.ndenumerate(board):
        for this_direction in directions:
            for this_count in range(max_distance):
                for other_direction in neighbours(board, *this, deltas=True):
                    # can't go backwards
                    if other_direction == neg(this_direction):
                        continue

                    # must go at least min_step in a direction
                    if this_count < min_step-1 and this_direction != other_direction:
                        continue

                    # can't go more than max_distance in one direction
                    if other_direction == this_direction:
                        other_count = this_count + 1
                        if other_count >= max_distance:
                            continue
                    else:
                        other_count = 0

                    other = add(this, other_direction)

                    graph.add_edge(
                        this + this_direction + (this_count,),
                        other + other_direction + (other_count,),
                        weight=board[other]
                    )

    source_location = (0, 0)
    target_location = (rows-1, cols-1)

    source_node = source_location
    for other_direction in neighbours(board, *source_location, stepsize=min_step):
        other = add(source_location, other_direction)
        direction = tuple(np.sign(e) for e in other_direction)
        graph.add_edge(
            source_node,
            other + direction + (min_step,),
            weight=path_cost(board, source_location, other),
        )

    # connect target node
    target_node = target_location
    for node in list(graph.nodes):
        if node[:2] == target_location:
            graph.add_edge(node, target_node, weight=0)

    path = nx.shortest_path(graph, source=source_node, target=target_node,
                            weight='weight')
    heat_loss = nx.path_weight(graph, path, weight='weight')

    return path, heat_loss

def plot_path(board, path):
    plot_path = [p[:2] for p in path]

    plt.imshow(board)
    plt.plot(*zip(*plot_path), 'r')
    plt.show()

# Part 1
path, heat_loss = solve(min_step=1, max_distance=3)

if plot:
    import matplotlib.pyplot as plt
    plot_path(board, path)

solution(heat_loss)

# Part 2
path, heat_loss = solve(min_step=4, max_distance=10)

if plot:
    plot_path(board, path)

solution(heat_loss)

