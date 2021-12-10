import datetime
import pathlib
import shutil
import sys

date = datetime.date.today()

year = date.year
day = date.day

target_dir = pathlib.Path(str(year), f'{day:02d}')
template = pathlib.Path('template')

if target_dir.exists():
    sys.exit(f'{target_dir} already exists')

target_dir.mkdir(parents=True)
for file in template.iterdir():
    print(file.name)
    shutil.copy(file, target_dir)

print(target_dir)
print(f'https://adventofcode.com/{year}/day/{day:02d}')