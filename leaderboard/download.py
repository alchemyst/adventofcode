import datetime
import pathlib
import sys

import requests
import aocd

LEADERBOARD_ID = "1189810"

URL = f"https://adventofcode.com/2021/leaderboard/private/view/{LEADERBOARD_ID}.json"

target = pathlib.Path(f'{LEADERBOARD_ID}.json')

modified = datetime.datetime.now() - datetime.datetime.fromtimestamp(target.stat().st_mtime)

if target.exists() and modified < datetime.timedelta(minutes=15):
    sys.exit()

# Get user token
user = aocd.get.default_user()
token = user.token

data = requests.get(URL, cookies={'session': token})

target.write_bytes(data.content)
