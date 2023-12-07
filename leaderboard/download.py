import datetime
import pathlib
import sys

import requests

import aoc_api

LEADERBOARD_ID = "1189810"
YEAR = 2023

URL = f"https://adventofcode.com/{YEAR}/leaderboard/private/view/{LEADERBOARD_ID}.json"

target = pathlib.Path(str(YEAR), f'{LEADERBOARD_ID}.json')

def modified(target):
    return datetime.datetime.now() - datetime.datetime.fromtimestamp(target.stat().st_mtime)

if target.exists() and modified(target) < datetime.timedelta(minutes=15):
    sys.exit()

data = aoc_api.get(URL)

target.write_bytes(data.content)

top100_url = "https://www.maurits.vdschee.nl/scatterplot/scores.tsv"

top100_target = pathlib.Path("scores.tsv")

top100_data = requests.get(top100_url)
top100_target.write_bytes(top100_data.content)


