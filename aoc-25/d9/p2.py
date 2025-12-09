from itertools import combinations

# Load red tiles (your polygon path)
with open("input.txt") as f:
    red_tiles = [tuple(map(int, line.split(","))) for line in f.read().splitlines()]

n = len(red_tiles)
edges = list(zip(red_tiles, red_tiles[1:] + red_tiles[:1]))


def point_in_poly(px, py):
    """Ray-casting: is (px, py) inside the polygon? (strict inside)"""
    inside = False
    for (x1, y1), (x2, y2) in edges:
        # Only vertical edges affect a horizontal ray to +x
        if x1 != x2:
            continue
        # Check if edge straddles the horizontal line y = py
        if (y1 > py) != (y2 > py):
            # x position of intersection is x1 (vertical line)
            if x1 > px:
                inside = not inside
    return inside


def rectangle_area_if_valid(p1, p2, best_area_so_far):
    x1, y1 = p1
    x2, y2 = p2

    # Must form a proper rectangle (not a line)
    if x1 == x2 or y1 == y2:
        return 0

    # get an area
    xmin, xmax = sorted((x1, x2))
    ymin, ymax = sorted((y1, y2))

    width = xmax - xmin + 1
    height = ymax - ymin + 1
    area = width * height

    # Prune by current best
    if area <= best_area_so_far:
        return 0

    # 1) Check that the rectangle is "inside" polygon: test its center
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0

    if not point_in_poly(cx, cy):
        return 0

    # 2) Check that polygon boundary does NOT cut through rectangle interior
    for (x3, y3), (x4, y4) in edges:
        if y3 == y4:
            # Horizontal edge
            y0 = y3
            if not (ymin < y0 < ymax):
                continue
            sxmin, sxmax = sorted((x3, x4))
            # Overlap with interior x-interval?
            if max(sxmin, xmin) < min(sxmax, xmax):
                return 0  # boundary passes through interior
        else:
            # Vertical edge
            x0 = x3
            if not (xmin < x0 < xmax):
                continue
            symin, symax = sorted((y3, y4))
            if max(symin, ymin) < min(symax, ymax):
                return 0  # boundary passes through interior

    # If we get here, rectangle is fully inside (or sharing boundary)
    return area


def find_max_rectangle_area(red_tiles):
    best = 0
    # We only need pairs of red tiles as opposite corners
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            # Quick skip: if they share row or column, degenerate
            if x1 == x2 or y1 == y2:
                continue
            area = rectangle_area_if_valid((x1, y1), (x2, y2), best)
            if area > best:
                best = area
    return best


if __name__ == "__main__":
    print(find_max_rectangle_area(red_tiles))
