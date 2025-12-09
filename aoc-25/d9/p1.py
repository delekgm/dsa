tiles = [list(map(int, tile.split(","))) for tile in open("input.txt").read().splitlines()]

max = 0
for i in range(len(tiles)):
    x1, y1 = tiles[i]
    for j in range(i+1, len(tiles)):
        x2, y2 = tiles[j]

        if x1 == x2 or y1 == y2: # 0 rect
            continue

        dx = abs(x1-x2)
        dy = abs(y1-y2)

        area = (dx + 1) * (dy + 1)
        if area > max:
            max = area
print(max)