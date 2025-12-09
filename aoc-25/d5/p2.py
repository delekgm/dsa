blocks = [blocks for blocks in open("input.txt").read().split("\n\n")]

ranges = [tuple(map(int, rng.split("-"))) for rng in blocks[0].split("\n")]
ranges = [range(rng[0], rng[1]+1) for rng in ranges]
ranges.sort(key=lambda r: r.start)

def merge_ranges(ranges):
    """
    Merge overlapping (or touching) range objects.
    Assumes ranges are like range(start, stop) with positive step.
    """
    if not ranges:
        return []

    # If not already sorted, sort by start just to be safe
    ranges = sorted(ranges, key=lambda r: r.start)

    merged = []
    current = ranges[0]

    for r in ranges[1:]:
        # Overlap / adjacency check:
        # current: [current.start, current.stop)
        # r:       [r.start, r.stop)
        #
        # If you want to merge only *overlapping* (not just touching),
        # use: r.start < current.stop instead of <=
        if r.start <= current.stop:
            # They overlap or touch; extend the current range
            new_start = current.start
            new_stop = max(current.stop, r.stop)
            current = range(new_start, new_stop)
        else:
            # No overlap; push current and start a new one
            merged.append(current)
            current = r

    merged.append(current)
    return merged

merged = merge_ranges(ranges)

print(merged)

fresh = 0
for r in merged:
    fresh += len(r)
print(fresh)