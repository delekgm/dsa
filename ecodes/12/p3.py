from functools import cache
from collections import deque

grid = [list(map(int, line)) for line in open("input.txt").read().splitlines()]

blobs = {}

for r in range(len(grid)):
    for c in range(len(grid[r])):
        if (r, c) in blobs: continue

        blob = {(r, c)}
        queue = deque(blob)

        while len(queue) > 0:
            cr, cc = queue.popleft()
            for nr, nc in [(cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)]:
                if nr < 0 or nr >= len(grid): continue
                if nc < 0 or nc >= len(grid[nr]): continue
                if grid[nr][nc] != grid[cr][cc]: continue
                if (nr, nc) in blob: continue
                blob.add((nr, nc))
                queue.append((nr, nc))
        for cr, cc in blob:
            blobs[(cr, cc)] = blob

@cache
def solve(r, c):
    total = set(blobs[(r, c)])
    for cr, cc in list(total):
        for nr, nc in [(cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)]:
            if nr < 0 or nr >= len(grid): continue
            if nc < 0 or nc >= len(grid[nr]): continue
            if grid[nr][nc] >= grid[cr][cc]: continue
            total |= solve(nr, nc)
    return total

total = set()
options = [solve(r, c ) for r in range(len(grid)) for c in range(len(grid[r]))]

for _ in range(3):
    best = max(options, key=lambda option: len(option - total))
    total |= best

print(len(total))