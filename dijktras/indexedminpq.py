class IndexedMinPQ:
    def __init__(self, keys):
        # keys is a reference to the dist[] array
        self.keys = keys
        self.heap = []        # holds vertex ids
        self.pos = [-1] * len(keys)  # pos[v] = index in heap, or -1 if not present

    def __len__(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    # helper: swap heap[i] and heap[j] AND update pos[...] accordingly
    def _swap(self, i, j):
        vi = self.heap[i]
        vj = self.heap[j]
        temp = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = temp
        self.pos[vi] = j
        self.pos[vj] = i

    # classic heap ops
    def _sift_up(self, i):
        # while i has a parent and key at i is smaller than key at parent, swap
        p = (i - 1) // 2
        while i > 0:
            p = (i - 1) // 2
            if self.keys[self.heap[i]] < self.keys[self.heap[p]]:
                self._swap(i, p)
                i = p
            else:
                break


    def _sift_down(self, i):
        # while i has a child with smaller key, swap with the smaller child
        n = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < n and self.keys[self.heap[left]] < self.keys[self.heap[smallest]]:
                smallest = left
            if right < n and self.keys[self.heap[right]] < self.keys[self.heap[smallest]]:
                smallest = right
            
            if smallest == i:
                break

            self._swap(i, smallest)
            i = smallest

    def push(self, v):
        # insert vertex v if not present
        if self.pos[v] != -1:
            return
        self.heap.append(v)
        self.pos[v] = len(self.heap) - 1
        self._sift_up(self.pos[v])

    def pop_min(self):
        # remove and return vertex with smallest key
        if self.is_empty():
            raise IndexError("pop from empty PQ")
        min_v = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self.pos[last] = 0
            self._sift_down(0)
        self.pos[min_v] = -1
        return min_v

    def decrease_key(self, v):
        # key already changed in self.keys[v]; just bubble it up
        self._sift_up(self.pos[v])