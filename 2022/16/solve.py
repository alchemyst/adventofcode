import re
from functools import cache
from itertools import combinations

import networkx as nx
from tqdm import tqdm

from aoc import solution

debug = False
filename = 'test.txt' if debug else 'input.txt'

pattern = re.compile(
    r"Valve ([A-Z]{2}) has flow rate=(\d+); "
    r"tunnels? leads? to valves? (.*)"
)

def read():
    g = nx.Graph()
    closed_valves = set()
    flow_rates = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            m = pattern.match(line)
            valve_name, flow_rate_str, others_string = m.groups()
            connected = others_string.split(', ')
            flow_rate = int(flow_rate_str)

            if flow_rate > 0:
                closed_valves.add(valve_name)
                flow_rates[valve_name] = flow_rate
            for other_valve in connected:
                g.add_edge(valve_name, other_valve)

    return g, closed_valves, flow_rates


def total_flowrate(open_valves):
    return sum(flow_rates[v] for v in open_valves)

@cache
def shortest_path_length(v1, v2):
    return nx.shortest_path_length(g, v1, v2)


def max_pressure(position, closed_valves, open_valves, remaining_time):
    if remaining_time <= 0:
        return 0

    current_rate = total_flowrate(open_valves)
    if not closed_valves or remaining_time == 1:
        return current_rate*remaining_time

    options = []
    for valve in closed_valves:
        time_to_move_to_valve = shortest_path_length(position, valve) + 1
        if time_to_move_to_valve > remaining_time:
            continue
        pressure_in_time = time_to_move_to_valve*current_rate

        new_pressure = pressure_in_time + max_pressure(
            valve,
            closed_valves - {valve},
            open_valves | {valve},
            remaining_time - time_to_move_to_valve,
        )

        options.append(new_pressure)

    if not options:
        return current_rate*remaining_time

    best_pressure = max(options)

    return best_pressure


g, closed_valves, flow_rates = read()

# # Part 1
open_valves = {'BB', 'DD', 'HH', 'JJ'}
# best_pressure = max_pressure("FF", closed_valves - open_valves, open_valves, 12)
best_pressure = max_pressure("AA", closed_valves, set(), 30)
solution(best_pressure)
#
# # Part 2
all_parts = []
for part in tqdm(list(combinations(closed_valves, len(closed_valves)//2))):
    p1 = max_pressure("AA", set(part), set(), 26)
    p2 = max_pressure("AA", closed_valves-set(part), set(), 26)
    all_parts.append(p1+p2)

solution(max(all_parts))
