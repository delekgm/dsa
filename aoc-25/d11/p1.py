from functools import cache

input = [line.split(": ") for line in open("input.txt").read().splitlines()]

graph = {}
for node, connections in input:
    graph[node] = connections.split()

@cache
def count_paths(node):
    if node == "out":
        return 1
    
    total = 0
    for nxt in graph[node]:
        total += count_paths(nxt)
    return total

print(count_paths("you"))
