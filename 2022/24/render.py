import json
from itertools import chain, pairwise

import numpy as np
import matplotlib.pyplot as plt
import pathlib

from tqdm import tqdm

from solve import render, plot_board

parameters = json.load(open('output/parameters.json'))

board_size = parameters["board_size"]
start = parameters["start"]
end = parameters["end"]

output = pathlib.Path('output')
blizzardfiles = sorted(output.glob('blizzards*.json'))
position = np.array(start)

path = chain.from_iterable(json.loads(f.read_text()) for f in sorted(output.glob('path*.json')))

t = 1
node = start
all_positions = []
for node1, node2 in pairwise(path):
    if len(node2) == 3:
        new_t, *target = node2
        while t < new_t:
            all_positions.append(node)
            t += 1
        node = target
    else:
        node = node2
        all_positions.append(node)
        t += 1

print(all_positions)

for t, (blizzardfile, position) in tqdm(enumerate(zip(blizzardfiles, all_positions)), total=len(all_positions)):
    blizzards = json.loads(blizzardfile.read_text())

    board = render(blizzards, board_size)
    plot_board(blizzards, board_size, start, end)
    plt.imshow(board.T)
    plt.plot(*position, 'ro')
    plt.savefig(f'output/frame_{t:03d}.png')
    plt.close()
