from aoc import solution
from aoc.directions import DIRECTIONS, rotate
import aoc.array
import numpy as np
import networkx as nx

debug = False
filename = 'test.txt' if debug else 'input.txt'

board = np.array(aoc.array.read_board(filename))


start = np.array((board == 'S').nonzero()).flatten()
end = np.array((board == 'E').nonzero()).flatten()

if debug:
    aoc.print_board(board, type='s')
    print(start, end)

# graph contains nodes for each possible transition, this is either a move or a rotation
graph = nx.DiGraph()

for pos, value in np.ndenumerate(board):
    if value == '#':
        continue

    for direction, move in DIRECTIONS.items():
        here = (*pos, direction)

        # We can always turn
        graph.add_edge(here, (*pos, rotate(direction, 1)), weight=1000)
        graph.add_edge(here, (*pos, rotate(direction, -1)), weight=1000)

        # When we move we stay in the same direction
        if (target_block := board[tuple(pos + move)]) in '.E':
            graph.add_edge(here, (*(pos + move), direction if target_block == '.' else 'E'), weight=1)


# Part 1
solution(nx.shortest_path_length(graph, (*start, '>'), (*end, 'E'), weight='weight'))

# Part 2
on_path = np.zeros_like(board, dtype=bool)
for path in nx.all_shortest_paths(graph, (*start, '>'), (*end, 'E')):
    for (i, j, _) in path:
        on_path[i, j] = True

solution(on_path.sum())