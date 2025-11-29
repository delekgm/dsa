nums = [int(num) for num in open("input.txt").read().split(",")]

# total = sum(90 // n for n in nums)
# print(total)

spell = []

while any(n > 0 for n in nums):
    index = [n > 0 for n in nums].index(True)
    spell.append(index + 1)
    for i in range(index, len(nums), index + 1):
        nums[i] -= 1

blocks = 202520252025000

lo = 0
hi = blocks

while lo < hi:
    mid = (lo + hi) // 2
    block_count = sum(mid // n for n in spell)
    if block_count == mid:
        break
    if lo == mid or hi == mid:
        break
    if block_count > blocks:
        hi = mid
    else:
        lo = mid

print(lo)