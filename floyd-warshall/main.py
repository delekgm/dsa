"""
Floyd Warshall finds all shortest paths between between node pairs using an adjacency matrix O^3 time O^2 space
"""
def build_matrix(n, edges):
    """
    n: num of nodes
    edges: list of (u, v, w) for directed edge u->v with weight w
    """
    INF = float('inf')

    W = [[INF for _ in range(n)] for __ in range(n)]
    for i in range(n):
        W[i][i] = 0 # add diagnol zeros for self connections

    for u, v, w in edges:
        W[u][v] = w

    return W

def build_next(W):
    n = len(W)
    nxt = [[None for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and W[i][j] != float('inf'):
                nxt[i][j] = j
    return nxt

def floyd_warshall_with_nxt(W):
    n = len(W)
    # the dists copying preserves original weights
    dist = [ row[:] for row in W ]
    nxt = build_next(W)

    for k in range(n):
        for i in range(n):
            dik = dist[i][k]
            if dik == float('inf'):
                continue
            for j in range(n):
                new = dik + dist[k][j]
                if new < dist[i][j]:
                    dist[i][j] = new
                    nxt[i][j] = nxt[i][k]
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist, nxt

def has_neg_cycle(dist):
    return any(dist[v][v] for v in range(len(dist)))

def reconstruct_path(i, j, nxt):
    # return path from i to j [] if unreachable
    if nxt[i][j] is None:
        return []
    path = [i]
    while i != j:
        i = nxt[i][j]
        if i is None:
            return []
        path.append(i)
    return path

edges = [(0,1,3), (1,3,2), (0,2,8), (3,2,1)]
W = build_matrix(4, edges)
dist, nxt = floyd_warshall_with_nxt(W)

print(has_neg_cycle(dist))

print("dist:")
for row in dist:
    print(row)

print("\npaths:")
print("0->2:", reconstruct_path(0,2, nxt))  # expect [0,1,3,2] since 0->4 doesn’t exist but 0->1->3->2 does
print("0->3:", reconstruct_path(0,3, nxt))  # expect [0,1,3]
print("2->0:", reconstruct_path(2,0, nxt))  # expect []

def transitive_closure(n, edges):
    T = [[False for _ in range(n)] for __ in range(n)]
    for i in range(n):
        T[i][i] = True # diagnols
    for u, v in edges:
        T[u][v] = True # connections
    for k in range(n):
        for i in range(n):
            if not T[i][k]:
                continue
            for j in range(n):
                T[i][j] = T[i][j] or (T[i][k] and T[k][j])
    return T

n = 4
edges = [(0,1), (1,3), (3,2)]
T = transitive_closure(n, edges)
for row in T: print(row)

edges = [(0,1,1), (1,2,1), (2,0,-3)]
W = build_matrix(3, edges)
dist = floyd_warshall_with_nxt(W)
print(has_neg_cycle(dist))  # expect: True

# Expect True for 0→1, 0→3, 0→2 (via 1,3), etc.
# Concretely:
# [True, True, True, True]
# [False, True, True, True]
# [False, False, True, False]
# [False, False, True, True]