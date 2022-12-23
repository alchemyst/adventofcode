import argparse
import datetime
import pathlib
import subprocess
import os
import time
import sqlite3

parser = argparse.ArgumentParser("Simple benchmark for solutions")
parser.add_argument("--year", type=int, default=datetime.date.today().year)
args = parser.parse_args()

start = pathlib.Path.cwd()

db = sqlite3.connect('bench.db')
db.execute(
    """
    create table if not exists times (year int, day int, program text, tm_run timestamp, elapsed real)  
    """
)
for solve in sorted(pathlib.Path(str(args.year)).glob('*/solve.py')):
    print(solve)
    try:
        os.chdir(solve.parent)
        day = int(solve.parent.name)
        start_time = time.perf_counter()
        subprocess.run(["python", str(solve.name)])
        elapsed = time.perf_counter() - start_time
        db.execute(
            "insert into times values (?, ?, ?, ?, ?)",
            (args.year, day, solve.name, datetime.datetime.now(), elapsed),
        )
        db.commit()
    finally:
        os.chdir(start)
db.close()