import itertools
from collections import defaultdict

import pandas as pd
import parse
import pulp
from tqdm import tqdm

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'


def prod(*args):
    return list(itertools.product(*args))


def read_blueprints(filename):
    blueprint_pattern = parse.compile(
        "Blueprint {:d}:"
        " Each {} robot costs {:d} {}."
        " Each {} robot costs {:d} {}."
        " Each {} robot costs {:d} {} and {:d} {}."
        " Each {} robot costs {:d} {} and {:d} {}."
    )

    resources = set()
    blueprints = []
    with open(filename) as f:
        for line in f:
            cost = defaultdict(int)
            n, *rest = blueprint_pattern.parse(line.strip())
            pos = 0
            for i in range(4):
                resources.add(rest[pos])
                cost[(rest[pos], rest[pos + 2])] = rest[pos + 1]
                if i in (2, 3):
                    cost[(rest[pos], rest[pos + 4])] = rest[pos + 3]
                    pos += 2
                pos += 3
            blueprints.append(cost)
    return list(resources), blueprints


production_rate = 1

resources, blueprints = read_blueprints(filename)

# Part 1
def max_geode(cost, maxtime):
    times = range(0, maxtime + 1)

    p = pulp.LpProblem("part1", pulp.LpMaximize)

    totals = pulp.LpVariable.dicts("totals", prod(resources, times), cat="Integer", lowBound=0)
    robots = pulp.LpVariable.dicts("robots", prod(resources, times), cat="Integer", lowBound=0)
    build = pulp.LpVariable.dicts("build", prod(resources, times), cat="Binary")

    for t in times:
        for r in resources:
            # running total resources
            if t > 0:
                p.add(
                    totals[r, t] ==
                    totals[r, t - 1]
                    - sum(build[robot, t] * cost[robot, r] for robot in resources)
                    + robots[r, t] * production_rate
                )
                # running total robots
                p.add(
                    robots[r, t] == robots[r, t - 1] + build[r, t - 1]
                )
                # can only build a robot if resources allow
                for rprime in resources:
                    p.add(build[r, t] * cost[r, rprime] <= totals[rprime, t-1])
        # can only build one robot at a time
        p.add(sum(build[(robot, t)] for robot in resources) <= 1)

    # initial conditions
    for r in resources:
        p.add(robots[r, 0] == (1 if r == 'ore' else 0))
        p.add(totals[r, 0] == 0)
        p.add(build[r, 0] == 0)

    # Objective: maximise geodes
    p += totals[("geode", maxtime)]
    p.solve(
        pulp.PULP_CBC_CMD(msg=False)
    )

    return p.objective.value()

# data = []
# for r in resources:
#     data.append([r, 'robots'] + [robots[r, t].value() for t in times])
#     data.append([r, 'build'] + [build[r, t].value() for t in times])
#     data.append([r, 'totals'] + [totals[r, t].value() for t in times])
#
# df = pd.DataFrame(data, columns=["resource", "var"] + list(times)).sort_values(
#     ["var", "resource"])
# print(df)

maxtime = 24

total_quality = 0
for id_number, cost in enumerate(tqdm(blueprints), 1):
    mg = max_geode(cost, maxtime)
    quality_level = id_number * mg
    total_quality += quality_level

solution(total_quality)

# Part 2
p = 1
for cost in tqdm(blueprints[:3]):
    mg = max_geode(cost, 32)
    p *= mg

solution(p)
