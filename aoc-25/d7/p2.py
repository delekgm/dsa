from functools import cache

grid = [line for line in open("input.txt").read().splitlines()]

for c in range(len(grid[0])):
    if grid[0][c] == 'S':
        start_col = c

ways = [0 for c in range(len(grid[0]))]
ways[start_col] = 1

for r in range(len(grid)):
    new_ways = [0 for c in range(len(grid[0]))]
    for c in range(len(grid[0])):
        count = ways[c]
        if count == 0: continue

        if grid[r][c] == "^":
            if c-1 >= 0:
                new_ways[c-1] += count
            if c+1 < len(grid[0]):
                new_ways[c+1] += count
        else:
            new_ways[c] += count

    ways = new_ways

print(sum(ways))

rows = len(grid)
cols = len(grid[0])

@cache
def dfs(r: int, c: int) -> int:
    """
    Number of distinct timelines starting from cell (r, c),
    where the particle arrives from above.
    """
    # If we've exited the grid downward → completed timeline
    if r >= rows:
        return 1

    cell = grid[r][c]

    if cell == '^':
        # Split
        left = dfs(r + 1, c - 1) if c - 1 >= 0 else 0
        right = dfs(r + 1, c + 1) if c + 1 < cols else 0
        return left + right

    else:
        # Otherwise fall straight down
        return dfs(r + 1, c)

# Start just below S at (start_row + 1, start_col)
print(dfs(1, start_col))
