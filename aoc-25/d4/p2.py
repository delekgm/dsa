grid = [line for line in open("input.txt").read().splitlines()]

def count_neighbors(grid, r, c):
    if grid[r][c] != '@':
        return None

    neighbor_rolls = 0
    for nr, nc in [
        (r+1, c), (r-1, c), (r, c+1), (r, c-1),
        (r-1, c-1), (r+1, c-1), (r+1, c+1), (r-1, c+1)
    ]:
        if nr < 0 or nr >= len(grid): continue
        if nc < 0 or nc >= len(grid[0]): continue
        if grid[nr][nc] == '@':
            neighbor_rolls += 1

    return neighbor_rolls

removed = 0
while True:
    changed = False
    new_grid = [list(row) for row in grid]

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != '@':
                continue

            neighbor_rolls = count_neighbors(grid, r, c)
            if neighbor_rolls < 4:
                new_grid[r][c] = '.' # mutate the new grid
                removed += 1
                changed = True

    grid = ["".join(row) for row in new_grid]

    if not changed:
        break

print(removed)