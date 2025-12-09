grid = [line for line in open("input.txt").read().splitlines()]

for c in range(len(grid[0])):
    if grid[0][c] == 'S':
        start_col = c

active_cols = {start_col}
split_count = 0

for r in range(len(grid)):
    next_active = set()
    for c in active_cols:
        if grid[r][c] == '^':
            split_count += 1
            if c-1 >= 0: next_active.add(c-1)
            if c+1 < len(grid[0]): next_active.add(c+1)
        else:
            next_active.add(c)
    active_cols = next_active

print(split_count)