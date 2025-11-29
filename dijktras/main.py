import heapq
from indexedminpq import IndexedMinPQ

INF = float('inf')

def init_single_source(n, s):
    dist = [INF] * n
    dist[s] = 0
    parent = [-1] * n
    return dist, parent

def relax(u, v, w, dist, parent):
    if dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
        parent[v] = u
        return True
    return False

def assert_non_negative(graph):
    # pick the right iterable of neighbor-lists
    if isinstance(graph, dict):
        iterable = graph.values()
    else:  # assume it's a list adjacency list
        iterable = graph

    for edges in iterable:
        for _, w in edges:
            if w < 0:
                raise ValueError("Edges must be non-negative for Dijkstra.")


def dijkstra_lazy(graph, s, t=None):
    assert_non_negative(graph)
    n = len(graph)
    dist, parent = init_single_source(n, s)
    
    # min-heap dist, vertex id
    pq = [(0, s)]

    while pq:
        d, u = heapq.heappop(pq)

        # skip stale values or values that are larger than the min
        if d != dist[u]:
            continue

        # Early exit for target
        if t is not None and u == t:
            break

        for v, w in graph[u]:
            if relax(u, v, w, dist, parent):
               heapq.heappush(pq, (dist[v], v))
    return dist, parent

def reconstruct_path(parent, s, t):
    path = []
    cur = t
    while cur != -1:
        path.append(cur)
        if cur == s:
            path.reverse()
            return path
        cur = parent[cur]
    return []  # no path

def dijkstra_book(graph, s, t=None):
    assert_non_negative(graph)
    n = len(graph)
    dist, parent = init_single_source(n, s)

    pq = IndexedMinPQ(dist)
    for v in range(n):
        pq.push(v)

    while not pq.is_empty():
        u = pq.pop_min()
        if t is not None and u == t:
            break

        for v, w in graph[u]:
            if relax(u, v, w, dist, parent):
                pq.decrease_key(v)
    return dist, parent

graph = [
    [(1,1), (2,4)],  # 0
    [(2,2), (3,5)],  # 1
    [(3,1)],         # 2
    []               # 3
]

dist, parent = dijkstra_lazy(graph, 0, 2)
print(dist, parent)

dist, parent = dijkstra_book(graph, 0)
print(dist, parent)

# Expect: dist[0] == 0, and all others are INF
_, parent = dijkstra_lazy(graph, 0)
print(reconstruct_path(parent, 0, 3))
# Expect: [0, 1, 2, 3]

INF = float('inf')
keys = [5, 7, 9, 3]  # keys indexed by vertex id
pq = IndexedMinPQ(keys)
pq.push(0); pq.push(1); pq.push(2); pq.push(3)
# min should be vertex 3 (key=3), then 0 (5), then 1 (7), then 2 (9)
assert pq.pop_min() == 3
assert pq.pop_min() == 0
assert pq.pop_min() == 1
assert pq.pop_min() == 2