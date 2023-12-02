import re
import pandas as pd

from aoc import solution, sum_every

debug = True
filename = 'test.txt' if debug else 'input.txt'


"Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
game_pattern = re.compile('Game ([0-9]+): (.*)')
show_pattern = re.compile('([0-9]+) ([a-z]+)')

games = {}
for line in open(filename):
    if debug: print(line)
    m = game_pattern.match(line)
    game_id = int(m[1])
    games[game_id] = []
    for n, color in show_pattern.findall(m[2]):
        if debug: print(n, color)
        games[game_id].append((int(n), color))


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