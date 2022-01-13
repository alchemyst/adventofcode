import datetime
import pathlib
import shutil
import sys
import argparse
import aocd

year = 2015
advent_days = range(1, 26)

def challenge_path(year, day):
    return pathlib.Path(str(year), f'{day:02d}')

date = datetime.date.today()

parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, default=date.year,
                    help='Year to work on, defaults to current year')
parser.add_argument('--day', type=int, default=date.day,
                    help='Day to work on, defaults to current day')
parser.add_argument('--next', action='store_true',
                    help="Work on next open day")

args = parser.parse_args()

template = pathlib.Path('template')

if args.next:
    while True:
        for day in advent_days:
            target_dir = challenge_path(year, day)
            if not target_dir.exists():
                break
        else:
            year += 1
            continue
        break
else:
    year, day = args.year, args.day
    target_dir = challenge_path(year, day)

    if target_dir.exists():
        print(f'{target_dir} already exists')
        sys.exit(2)

print(target_dir)

target_dir.mkdir(parents=True)
for file in template.iterdir():
    print(' - ', file.name)
    shutil.copy(file, target_dir)

inputdata = target_dir / 'input.txt'

puzzle = aocd.models.Puzzle(year=year, day=day)
with open(inputdata, 'w') as f:
    f.write(puzzle.input_data)

print(f'https://adventofcode.com/{year}/day/{day}')
