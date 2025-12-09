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
    if parent[a] != a:
        parent[a] = find(parent[a])
    return parent[a]

def union(a, b):
    root_a = find(a)
    root_b = find(b)
    if root_a == root_b:
        return
    if size[root_a] < size[root_b]:
        root_a, root_b = root_b, root_a
    parent[root_b] = root_a
    size[root_a] += size[root_b]


for k in range(len(edges)):
    _, i, j = edges[k]
    union(i, j)

components = []
for i in range(n):
    if find(i) == i:
        components.append(size[i])

components.sort(reverse=True)
print(components[0] * components[1] * components[2])