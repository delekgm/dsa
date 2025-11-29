import random

def merge_sort(arr):
    n = len(arr)
    a0 = arr
    a1 = [0] * n
    m = 1
    while m < n:
        i = 0
        while i < n:
            left = i
            right = min(i + m, n)
            end = min(i + (m << 1), n)
            merge(a0, a1, left, right, end)
            i += m << 1
        a0, a1 = a1, a0
        m <<= 1
    
    if arr == a1:
        for i in range(n):
            arr[i] = a0[i]

def merge(a0, a1, left, right, end):
    i0 = left
    i1 = right

    for j in range(left, end):
        if i0 < right and (i1 >= end or a0[i0] <= a0[i1]):
            a1[j] = a0[i0]
            i0 += 1
        else:
            a1[j] = a0[i1]
            i1 += 1

arr = random.sample(range(1, 11), 10)
print(arr)
merge_sort(arr)
print(arr)
