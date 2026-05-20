"""LeetCode 295: Find Median from Data Stream - Hard"""
import time, tracemalloc
import heapq, bisect

# Variation 1: Two heaps (max-heap for lower half, min-heap for upper half)
class MedianFinder_v1:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap
    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        # Ensure small's max <= large's min
        if self.small and self.large and -self.small[0] > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        # Balance sizes (diff <= 1)
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small) + 1:
            heapq.heappush(self.small, -heapq.heappop(self.large))
    def findMedian(self) -> float:
        if len(self.small) > len(self.large): return -self.small[0]
        if len(self.large) > len(self.small): return self.large[0]
        return (-self.small[0] + self.large[0]) / 2.0

# Variation 2: Sorted list with bisect (simpler, slower insert)
class MedianFinder_v2:
    def __init__(self): self.data = []
    def addNum(self, num: int) -> None:
        bisect.insort(self.data, num)
    def findMedian(self) -> float:
        n = len(self.data)
        if n % 2: return float(self.data[n // 2])
        return (self.data[n // 2 - 1] + self.data[n // 2]) / 2.0

if __name__ == "__main__":
    ops = [1, 2, 3, 4, 5]
    for Vi, Cls in enumerate([MedianFinder_v1, MedianFinder_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        mf = Cls()
        results = []
        for v in ops:
            mf.addNum(v); results.append(mf.findMedian())
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: medians={results}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
