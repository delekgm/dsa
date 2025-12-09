input = [line for line in open("input.txt").read().splitlines()]
full_parsed = [int(dir[1:]) * -1 if dir[0] == 'L' else int(dir[1:]) for dir in input]

start = 50
total = 0
for dir in full_parsed:
    start = (start + (dir)) % 100
    if start == 0:
        total += 1
print(total)