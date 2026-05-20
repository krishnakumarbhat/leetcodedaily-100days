"""LeetCode 703: Kth Largest Element in a Stream - Easy"""
import time, tracemalloc
import heapq
from typing import List

# Variation 1: Min-heap of size k
class KthLargest_v1:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []
        for n in nums: self.add(n)
    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k: heapq.heappop(self.heap)
        return self.heap[0]

# Variation 2: Sorted list insertion (brute force baseline)
class KthLargest_v2:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.data = sorted(nums, reverse=True)
    def add(self, val: int) -> int:
        import bisect
        bisect.insort(self.data, -val)  # store negated for desc order
        return -self.data[self.k - 1]

if __name__ == "__main__":
    ops = [3, 5, 10, 9, 4]
    for Vi, Cls in enumerate([KthLargest_v1, KthLargest_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        kl = Cls(3, [4, 5, 8, 2])
        results = [kl.add(v) for v in ops]
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {results}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
