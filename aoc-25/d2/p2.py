input = [ranges for ranges in open("input.txt").read().split(",")]
index_ranges = [[int(i) for i in r.split("-")] for r in input]

def is_invalid_id(n: int) -> bool:
    s = str(n)
    L = len(s)

    # Try all possible block lengths d that divide L, with at least 2 blocks
    for d in range(1, L // 2 + 1):
        if L % d != 0:
            continue

        k = L // d  # number of repeats
        # if k < 2:
        #     continue  # safety; though k>=2 automatically if d <= L//2

        block = s[:d]
        if block * k == s:
            return True

    return False

def invalid_ids_in_range(L: int, R: int):
    """
    Return all invalid IDs n in [L, R], where "invalid" means:
    the decimal representation of n is some digit-block repeated at least twice.
    """
    result = []
    for n in range(L, R + 1):
        if is_invalid_id(n):
            result.append(n)
    return result

invalid = []
for l, r in index_ranges:
    invalid.extend(invalid_ids_in_range(l, r))

print(sum(invalid))