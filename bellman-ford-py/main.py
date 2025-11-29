graph = {
    'A': [('B', 3), ('C', 5)],
    'B': [('C', 1)],
    'C': []
}

def bellman_ford(G, s):
    dists = {}
    parents = {}

    def init_single_source(G, s):
        for vert in G:
            dists[vert] = float('inf')
            parents[vert] = None
        dists[s] = 0

    def relax(u, v, weight):
        if dists[v] > dists[u] + weight:
            dists[v] = dists[u] + weight
            parents[v] = u

    init_single_source(G, s)
    for _ in range(1, len(G)):
        for u in G:
            for (v, w) in G[u]:
                relax(u, v, w)
    for u in G:
        for (v, w) in G[u]:
           if dists[v] > dists[u] + w:
               return False
    return dists, parents

result = bellman_ford(graph, 'A')

if result is False:
    print("Negative cycle detected")
else:
    distances, parents = result
    print(distances)
    print(parents)
