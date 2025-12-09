points = [list(map(int, ints.split(","))) for ints in open("input.txt").read().splitlines()]

n = len(points)
edges = []

for i in range(n):
    x1, y1, z1 = points[i]
    for j in range(i+1, n):
        x2, y2, z2 = points[j]
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        dist2 = dx*dx + dy*dy + dz*dz
        edges.append((dist2, i, j))

parent = list(range(n))
size = [1] * n


edges.sort(key=lambda edge: edge[0])

def find(a):
    if parent[a] != a: # if the parent is not the currently processed
        parent[a] = find(parent[a]) # recursively find the parent until the root
    return parent[a]

# Disjoint Set Union (Union-Find)
def union(a, b):
    root_a = find(a) # find a's parent
    root_b = find(b) # find b's parent
    if root_a == root_b: # same parent they are already connected
        return False
    if size[root_a] < size[root_b]: # root_a graph's size < root_b graph's size
        root_a, root_b = root_b, root_a # point root_a to the larger graph
    parent[root_b] = root_a # make the parent of root_b also point to root_a so they are connected
    size[root_a] += size[root_b] # adjust the size of graph at root_a
    return True

last_pair = None
for k in range(len(edges)):
    dist2, i, j = edges[k]
    if union(i, j):
        last_pair = (i, j)

i, j = last_pair
x_i = points[i][0]
x_j = points[j][0]
print( x_i * x_j)
