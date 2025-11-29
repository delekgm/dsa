import random

def quicksort(arr, left, right):
    if left < right -1:
        pivot = left + right >> 1
        pivot = partition(arr, left, right, pivot)
        quicksort(arr, left, pivot)
        quicksort(arr, pivot+1, right)

def partition(arr, left, right, pivot):
    pivot_val = arr[pivot]
    right -= 1
    swap(arr, pivot, right)
    for i in range(left, right):
        if arr[i] < pivot_val:
            swap(arr, i, left)
            left += 1
    swap(arr, left, right)
    return left # this is the new sorted pivot index

def swap(arr, idx_from, idx_to): #
    temp = arr[idx_to]
    arr[idx_to] = arr[idx_from]
    arr[idx_from] = temp

array = random.sample(range(1, 11), 10)
print(array)
quicksort(array, 0, len(array))
print(array)