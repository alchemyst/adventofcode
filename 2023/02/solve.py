import re
import pandas as pd

from aoc import solution, sum_every

debug = False
filename = 'test.txt' if debug else 'input.txt'

"Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
game_pattern = re.compile('Game ([0-9]+): (.*)')
show_pattern = re.compile('([0-9]+) ([a-z]+)')

games = {}
for line in open(filename):
    m = game_pattern.match(line)
    games[int(m[1])] = [(int(n), color) for n, color in show_pattern.findall(m[2])]

# Part 1
targets = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

bad_ids = set()
for gid, plays in games.items():
    for n, color in plays:
        if n > targets[color]:
            bad_ids.add(gid)
            break


solution(sum(games.keys() - bad_ids))

def part2(game):
    gid, plays = game
    return pd.DataFrame(plays, columns=["n", "color"]).groupby("color")["n"].max().prod()


solution(sum_every(part2, games.items()))
