grid = [line for line in open("input.txt").read().splitlines()]

rolls = 0
for r in range(len(grid)):
    for c in range(len(grid[0])):
        neighbor_rolls = 0
        for nr, nc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1), (r-1, c-1), (r+1, c-1), (r+1, c+1), (r-1, c+1)]:
            if nr > len(grid)-1: continue
            if nc > len(grid[0])-1: continue
            if nr < 0: continue
            if nc < 0: continue
            if grid[nr][nc] == ".": continue
            if grid[nr][nc] == "@":
                neighbor_rolls += 1
        if neighbor_rolls < 4 and grid[r][c] == "@":
            rolls += 1

print(rolls)