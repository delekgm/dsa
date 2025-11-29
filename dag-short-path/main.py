from collections import deque

def topo_sort_kahn(graph):
    in_degree = { u: 0 for u in graph }
    for u, nbrs in graph.items():
        for v, _w in nbrs:
            if v not in in_degree:
                in_degree[v] = 0
    
    for u, nbrs in graph.items():
        for v, _w in nbrs:
            in_degree[v] += 1
    
    q = deque([ u for u, deg in in_degree.items() if deg == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v, _w in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)
    if len(order) < len(in_degree):
        print("Cycle detected")
        return
    return order

def relax(u, v, w, d, pi):
    if d[v] > d[u] + w:
        d[v] = d[u] + w
        pi[v] = u

def relax_longest(u, v, w, d, pi):
    if d[v] < d[u] + w:
        d[v] = d[u] + w
        pi[v] = u

def add_edge(graph, u, v, w):
    graph.setdefault(u, []).append((v, w))
    graph.setdefault(v, [])

def init_single_source(graph, s):
    d = { u: float('inf') for u, _nbrs in graph.items() }
    d[s] = 0
    pi = { u: None for u, _nbrs in graph.items() }
    return d, pi

def init_longest_source(graph, s):
    d = { u: float('-inf') for u, _nbrs in graph.items() }
    d[s] = 0
    pi = { u: None for u, _nbrs in graph.items() }
    return d, pi

def dag_shortest_path(graph, s):
    order = topo_sort_kahn(graph)
    d, pi = init_single_source(graph, s)

    for u in order:
        if d[u] == float('inf'):
            continue
        for v, w in graph.get(u, []): # [] is the default return if !u
            relax(u, v, w, d, pi)
    return d, pi, order

def dag_longest_path(graph, s):
    order = topo_sort_kahn(graph)
    d, pi = init_longest_source(graph, s)

    for u in order:
        if d[u] == float('-inf'):
            continue
        for v, w in graph.get(u, []): # [] is the default return if !u
            relax_longest(u, v, w, d, pi)
    return d, pi, order

def reconstruct_path(pi, s, t):
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        if cur == s:
            break
        cur = pi.get(cur) # get the parent of current node
    if not path or path[-1] != s:
        return None
    path.reverse()
    return path

graph = {}
add_edge(graph, "s", "a", 1)
add_edge(graph, "s", "b", 4)
add_edge(graph, "a", "b", -2)
add_edge(graph, "a", "c", 2)
add_edge(graph, "b", "c", 3)
add_edge(graph, "b", "t", 6)
add_edge(graph, "c", "t", 2)

print("------shortest path-------\n")
d, pi, order = dag_shortest_path(graph, 's')
print(f"d = {d}, pi={pi}, order={order}\n")
print(f"reconstruct: {reconstruct_path(pi, 's', 't')}\n")

print("------longest path-------\n")
d, pi, ordeå = dag_longest_path(graph, 's')
print(f"d = {d}, pi={pi}, order={order}\n")
print(f"reconstruct: {reconstruct_path(pi, 's', 't')}\n")
