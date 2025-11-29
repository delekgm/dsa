import heapq


class NegativeCycleError(Exception):
    pass


def bellman_ford(V, E, s):
    dists = {}
    parents = {}

    def init_single_source(V, s):
        for v in V:
            dists[v] = float('inf')
            parents[v] = None
        dists[s] = 0
    
    def relax(u, v, w):
        if dists[v] > dists[u] + w:
            dists[v] = dists[u] + w
            parents[v] = u
            return True
        return False
    
    init_single_source(V, s)
    for _ in range(len(V) - 1):
        updated = False
        for (u, v, w) in E:
            if relax(u, v, w):
                updated = True
        if not updated:
            break

    # negative weight check
    for (u, v, w) in E:
        if dists[v] > dists[u] + w:
            raise NegativeCycleError("Negative cycle detected")
    return dists, parents


def compute_potential_q(V, E):
    q = object()
    Vq = V + [q] # add q as a temp vert
    Eq = edges + [[q, v, 0] for v in V] # add 0 weight edges to all nodes from q
    dists, _ = bellman_ford(Vq, Eq, q) # get shortest dists from q
    return { v: dists[v] for v in V }


def reweight_edges(V, E, h):
    adj = { v: [] for v in V}
    for (u, v, w) in E:
        w_prime = w + h[u] - h[v]
        adj[u].append((v, w_prime))
    return adj


def dijkstras(G, s, t = None):
    dist = { v: float('inf') for v in G }
    dist[s] = 0
    pq = [(0, s)]

    while pq:
        d, u = heapq.heappop(pq)

        # skip stale values or values that are larger than the min
        if d != dist[u]:
            continue
        
        if t is not None and u == t:
            break

        for v, w in G[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist

def unshift_all(V, dprime_all, h):
    d = { s: {} for s in V }
    d_mat = [[float('inf') for _ in range(len(V))] for _ in range(len(V))]
    for i, s in enumerate(V): # s = source
        for j, v in enumerate(V):
            dv_prime = dprime_all[s].get(v, float('inf'))
            d[s][v] = float('inf') if dv_prime == float('inf') else dv_prime - h[s] + h[v]
            d_mat[i][j] = float('inf') if dv_prime == float('inf') else dv_prime - h[s] + h[v] # matrix version
    return d, d_mat

vertices = ["A", "B", "C", "D"]
edges = [("A","B",1), 
         ("A","C",4), 
         ("B","C",-2), 
         ("B","D",2), 
         ("C","D",3), 
         ("D","B",1)
        ]

def johnsons(V, E):
    h = compute_potential_q(V, E)
    w_primes = reweight_edges(vertices, edges, h)
    dprime_all = { s: dijkstras(w_primes, s) for s in vertices }
    d_shifted = unshift_all(V, dprime_all, h)
    return d_shifted

D, D_MAT = johnsons(vertices, edges)
for s in vertices:
    print(s, D[s])
print(D_MAT)