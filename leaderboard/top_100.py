import pathlib
import time
import datetime

import aoc_api

today = datetime.datetime.today()

year = today.year
this_day = today.day

for day in range(1, this_day+1):
    target = pathlib.Path(f'{year}_{day:02d}.txt')

    if not target.exists():
        print('Downloading', target)
        url = f"https://adventofcode.com/{year}/leaderboard/day/{day}"
        data = aoc_api.get(url)
        target.write_bytes(data.content)
        print('Sleep')
        time.sleep(1)