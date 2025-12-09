banks = [list(map(int, bank)) for bank in open("input.txt").read().splitlines()]

total = 0

for bank in banks:
    # There must be at least 2 digits per bank
    best = -1
    best_left = bank[0]   # best digit seen so far to the left

    for j in range(1, len(bank)):
        # Use the best left digit with this right digit
        candidate = 10 * best_left + bank[j] # combines the numbers 9 * 10 = 90 + 8 = 98
        if candidate > best:
            best = candidate

        # Update best_left to include bank[j]
        if bank[j] > best_left:
            best_left = bank[j]

    total += best

print(total)
