blocks = [blocks for blocks in open("input.txt").read().split("\n\n")]

ranges = [tuple(map(int, rng.split("-"))) for rng in blocks[0].split("\n")]
ranges = [range(rng[0], rng[1] + 1) for rng in ranges]
ranges.sort(key=lambda r: r.start)

items = [int(item) for item in blocks[1].split("\n")]

fresh = 0

for item in items:
    for rng in ranges:
        if item in rng:
            fresh += 1
            break

print(fresh)

