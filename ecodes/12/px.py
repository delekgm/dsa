from collections import deque

grid = [list(map(int, line)) for line in open("input.txt").read().splitlines()]

seen = {(0, 0), (len(grid)-1, len(grid[0])-1)}
queue = deque(seen)

while len(queue):
    r, c = queue.popleft()
    for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
        if nr < 0 or nr >= len(grid): continue
        if nc < 0 or nc >= len(grid[nr]): continue
        if grid[nr][nc] > grid[r][c]: continue
        if (nr, nc) in seen: continue
        seen.add((nr, nc))
        queue.append((nr, nc))
print(len(seen))