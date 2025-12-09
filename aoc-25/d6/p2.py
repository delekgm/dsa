lines = open("input.txt").read().splitlines()

digit_rows = lines[:-1]
op_row = lines[-1]

width = max(len(r) for r in lines)
digit_rows = [r.ljust(width) for r in digit_rows]
op_row = op_row.ljust(width)

def col_is_blank(col):
    return all(row[col] == ' ' for row in digit_rows) and op_row[col] == ' '

def col_value(col):
    digits = [row[col] for row in digit_rows]
    digits = ''.join(d for d in digits if d != ' ')
    return int(digits) if digits else 0

# group columns into problems
problems = []
cur = []
for c in range(width-1, -1, -1):
    if col_is_blank(c):
        if cur:
            problems.append(cur)
            cur = []
    else:
        cur.append(c)
if cur:
    problems.append(cur)

total = 0
for cols in problems:
    nums = [col_value(c) for c in cols]
    op = next(op_row[c] for c in cols if op_row[c] in '+*')
    if op == '*':
        r = 1
        for n in nums: r *= n
    else:
        r = sum(nums)
    total += r

print(total)
