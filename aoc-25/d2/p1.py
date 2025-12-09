input = [ranges for ranges in open("input.txt").read().split(",")]
index_ranges = [[int(i) for i in r.split("-")] for r in input]

def repeating_half_numbers(L, R):
    """
    Return a list of all integers n in [L, R] such that:
      - n has an even number of decimal digits
      - if you split its digits into two equal halves, the halves are identical

    Examples:
      L=11, R=22  -> [11, 22]
      L=98, R=115 -> [99]
    """

    # Final result collector
    result = []

    # Helper: count decimal digits of a non-negative integer
    def num_digits(x):
        return len(str(x))

    lenL = num_digits(L)
    lenR = num_digits(R)

    # We iterate over possible total digit counts between L and R
    # Only EVEN digit counts can possibly qualify.
    for total_digits in range(lenL, lenR + 1):

        # Skip odd digit lengths entirely: they cannot split evenly.
        if total_digits % 2 != 0:
            continue

        # If total_digits = 2k, then each half uses k digits
        k = total_digits // 2

        # base = 10^k, used to glue two halves:
        #   N = half * base + half
        base = 10 ** k

        # --- Base half-range (before tightening) --------------------------
        # We only allow k-digit halves with no leading zero.
        # So the half is in [10^(k-1), 10^k - 1].
        half_min = 10 ** (k - 1)
        half_max = (10 ** k) - 1

        # --- Tighten the lower bound using L (if L has this digit length) ---

        # If L has exactly 'total_digits' digits, it can constrain how small
        # the half (X) can be, because N = X||X must be >= L.
        if num_digits(L) == total_digits:
            # Extract the first k digits of L as an integer.
            # Example: L=98, total_digits=2, k=1 -> left_L = 9
            left_L = L // base

            # Form the candidate N from this half: N = left_L||left_L
            candidate_from_L = left_L * base + left_L

            # If that candidate is still below L, then we need to bump the half up by 1
            # to ensure that N >= L.
            if candidate_from_L < L:
                left_L += 1

            # Now left_L is the smallest half that *might* produce N >= L.
            # We intersect that with the generic half_min.
            if left_L > half_min:
                half_min = left_L

        # --- Tighten the upper bound using R (if R has this digit length) ---

        # Symmetric idea for the upper bound: if R has total_digits digits,
        # then N = X||X must be <= R, so R can limit how large the half can be.
        if num_digits(R) == total_digits:
            # Extract the first k digits of R.
            left_R = R // base

            # Form the candidate N = left_R||left_R
            candidate_from_R = left_R * base + left_R

            # If that candidate is above R, the half is too large.
            # We step it down by 1.
            if candidate_from_R > R:
                left_R -= 1

            # Intersect with the generic half_max.
            if left_R < half_max:
                half_max = left_R

        # After tightening, if the half-range is invalid, no numbers of this
        # digit length can appear in [L, R].
        if half_min > half_max:
            continue

        # --- Generate all valid numbers for this digit length -------------

        # For each possible half in the final tightened range, we construct:
        #   N = half||half
        # This N will automatically have 'total_digits' digits (no leading zeros)
        # and equal halves by construction.
        for half in range(half_min, half_max + 1):
            n = half * base + half

            # This check should be redundant if we tightened correctly,
            # but it's cheap and makes the function robust to mistakes.
            if L <= n <= R:
                result.append(n)

    return result

invalid_indices = []
for i, j in index_ranges:
    invalid_indices.extend(repeating_half_numbers(i, j))
print(sum(invalid_indices))