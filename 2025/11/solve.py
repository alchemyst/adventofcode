from aoc import solution
import networkx as nx
from functools import cache

debug = False
filename = "test2.txt" if debug else "input.txt"

graph = nx.DiGraph()

with open(filename) as f:
    for line in f:
        source, *rest = line.strip().replace(":", "").split()
        for item in rest:
            graph.add_edge(source, item)


# Part 1
@cache
def count_paths(start, end):
    if end in graph.neighbors(start):
        return 1
    else:
        return sum(
            count_paths(neighbor, end)
            for neighbor in graph.neighbors(start)
            if neighbor is not end
        )


solution(count_paths("you", "out"))

# Part 2
svr_fft = count_paths("svr", "fft")
fft_dac = count_paths("fft", "dac")
# there are no paths from dac to fft
dac_out = count_paths("dac", "out")

total_paths = svr_fft * fft_dac * dac_out

solution(total_paths)
