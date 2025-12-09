banks = [line.strip() for line in open("input.txt") if line.strip()]

TARGET_LEN = 12
total = 0

for bank in banks:
    digits = list(map(int, bank))
    n = len(digits)
    k = n - TARGET_LEN  # how many digits we must drop

    stack = []

    for d in digits:
        # Greedily drop smaller previous digits while we can
        while stack and k > 0 and stack[-1] < d:
            stack.pop()
            k -= 1
        stack.append(d)

    # If we still have deletions left, drop from the end
    if k > 0:
        stack = stack[:-k]

    # Take exactly TARGET_LEN digits (safety slice)
    result_digits = stack[:TARGET_LEN]
    value = int("".join(map(str, result_digits)))
    total += value

    # print(f"{bank} -> {''.join(map(str, result_digits))} ({value})")

print("Total:", total)
