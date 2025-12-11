from aoc import solution
import networkx as nx

debug = False
filename = "test2.txt" if debug else "input.txt"

graph = nx.DiGraph()

with open(filename) as f:
    for line in f:
        source, *rest = line.strip().replace(":", "").split()
        for item in rest:
            graph.add_edge(source, item)


# Part 1
def count_paths(start, end, cutoff=10):
    return sum(1 for _ in nx.all_simple_paths(graph, start, end, cutoff=cutoff))


solution(count_paths("you", "out"))

# Part 2

# Visualised and special-cased the hell out of this one
# found some choke points and exploited the topology of my graph
# definitely won't work in general case

# nx.write_graphml(graph, "graph.graphml")
#
# with open("test.dot", "w") as f:
#     f.write(nx.nx_pydot.to_pydot(graph).to_string())

svr_fft = count_paths("svr", "fft", 11)

fft_rpn = count_paths("fft", "rpn", 9)
fft_apc = count_paths("fft", "apc", 9)
fft_lpz = count_paths("fft", "lpz", 9)

rpn_dac = count_paths("rpn", "dac", 9)
apc_dac = count_paths("apc", "dac", 9)
lpz_dac = count_paths("lpz", "dac", 9)

fft_dac = (fft_rpn * rpn_dac) + (fft_apc * apc_dac) + (fft_lpz * lpz_dac)

dac_out = count_paths("dac", "out", 9)

total_paths = svr_fft * fft_dac * dac_out

solution(total_paths)
