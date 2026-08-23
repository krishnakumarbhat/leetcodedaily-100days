"""
=====================================================================
LeetCode 703 : Kth Largest Element in a Stream                   (Easy)
https://leetcode.com/problems/kth-largest-element-in-a-stream/
Category   : Heap / Priority queue
---------------------------------------------------------------------
PROBLEM
    Design a class: constructor receives k and an initial list; add(v)
    appends to the stream and returns the current k-th largest.
---------------------------------------------------------------------
INTUITION
    Only the boundary of the top-k matters. A min-heap of size k keeps
    exactly that boundary: heap[0] is the k-th largest, and any value
    below it is permanently irrelevant.
---------------------------------------------------------------------
APPROACH 1 · Min-heap of size k (best)
    Constructor: heapify nums, trim to size k by popping the root.
    add(v): heappush, pop if oversized, return heap[0].
APPROACH 2 · Naive sorted list (baseline)
    Append and re-sort descending on every add; answer is index k-1.
---------------------------------------------------------------------
DEEP DIVE · Why we can reject values forever
    Invariant: heap holds the k largest values of the stream. A new
    value ≤ heap[0] is ≤ every element in the top-k, so no matter how
    many future values arrive, this one can never rise into the
    top-k — discarding it loses nothing. Values > heap[0] replace the
    root (O(log k)) and keep the invariant. This "small values are
    dead on arrival" insight is the whole trick of streaming top-k.
---------------------------------------------------------------------
TIME COMPLEXITY : O(log k) per add ; O(k) construction.
MEMORY COMPLEXITY: O(k).
=====================================================================
"""
import heapq, time, tracemalloc


class Solution_1:
    """Min-heap of size k — constant-size state."""

    def __init__(self, k, nums):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


class Solution_2:
    """Sorted-list baseline: O(n log n) per add."""

    def __init__(self, k, nums):
        self.k = k
        self.data = sorted(nums, reverse=True)[:k]

    def add(self, val):
        self.data.append(val)
        self.data.sort(reverse=True)
        self.data = self.data[:self.k]
        return self.data[self.k - 1]


if __name__ == "__main__":
    steps = [(3, 4), (5, 5), (10, 5), (9, 8), (4, 8)]
    tracemalloc.start()
    t0 = time.perf_counter()
    s1 = Solution_1(3, [4, 5, 8, 2])
    s2 = Solution_2(3, [4, 5, 8, 2])
    ok = True
    for val, want in steps:
        r1, r2 = s1.add(val), s2.add(val)
        ok &= r1 == want and r2 == want
        print(f"add({val}) -> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all adds' if ok else 'FAIL'} | time: {dt * 1e6:.0f} us | mem: {mem:.0f} KB")
