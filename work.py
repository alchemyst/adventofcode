import datetime
import pathlib
import shutil
import sys
import argparse
import aocd

date = datetime.date.today()

parser = argparse.ArgumentParser()
parser.add_argument('year', type=int, default=date.year)
parser.add_argument('day', type=int, default=date.day)
parser.add_argument('--test', action='store_true')

args = parser.parse_args()

target_dir = pathlib.Path(str(args.year), f'{args.day:02d}')
template = pathlib.Path('template')

if target_dir.exists():
    sys.exit(f'{target_dir} already exists')

target_dir.mkdir(parents=True)
for file in template.iterdir():
    print(file.name)
    shutil.copy(file, target_dir)

inputdata = target_dir / 'input.txt'

puzzle = aocd.models.Puzzle(year=args.year, day=args.day)
with open(inputdata, 'w') as f:
    f.write(puzzle.input_data)

print(target_dir)
print(f'https://adventofcode.com/{args.year}/day/{args.day:02d}')
