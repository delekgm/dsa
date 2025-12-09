input = [line for line in open("input.txt").read().splitlines()]
full_parsed = [int(dir[1:]) * -1 if dir[0] == 'L' else int(dir[1:]) for dir in input]

start = 50
total = 0
for dir in full_parsed:
    if dir < 0:
        div, mod = divmod(dir, -100) # full turns plus remaining offset
        total += div
        if start != 0 and start + mod <= 0:
            total += 1
    else:
        div, mod = divmod(dir, 100)
        total += div
        if start + mod >= 100:
            total += 1

    start = (start + (dir)) % 100

print(total)