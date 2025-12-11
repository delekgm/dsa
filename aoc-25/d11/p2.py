from functools import cache

input = [line.split(": ") for line in open("input.txt").read().splitlines()]

graph = {}
for node, connections in input:
    graph[node] = connections.split()

@cache
def count_paths(node, seen_dac, seen_fft):
    if node == "out":
        return 1 if (seen_dac and seen_fft) else 0

    total = 0
    for nxt in graph[node]:
        nxt_seen_dac = (nxt == "dac") or seen_dac
        nxt_seen_fft = (nxt == "fft") or seen_fft
        total += count_paths(nxt, nxt_seen_dac, nxt_seen_fft)
    return total

print(count_paths("svr", False, False))
