"""
=====================================================================
LeetCode 295 : Find Median from Data Stream                     (Hard)
https://leetcode.com/problems/find-median-from-data-stream/
Category   : Heap / Priority queue
---------------------------------------------------------------------
PROBLEM
    Design a class: addNum(v) streams integers in any order;
    findMedian() returns the median of everything added so far.
---------------------------------------------------------------------
INTUITION
    Split the stream into a LOWER half (max-heap, store negatives)
    and an UPPER half (min-heap). Balanced heights + ordered tops
    give the median from the boundary in O(1).
---------------------------------------------------------------------
APPROACH 1 · Two heaps (best)
    1. addNum: push to the lower max-heap; rebalance by moving the
       boundary element if lower's top exceeds upper's top.
    2. findMedian: equal sizes -> mean of both tops; else top of
       the taller heap.
APPROACH 2 · Bisect-insert into a sorted list (baseline)
    data.insert(bisect_left(data, v), v) is O(n) per add due to the
    memmove — fine for small n, hopeless at scale.
---------------------------------------------------------------------
DEEP DIVE · The balance invariant
    Invariants after every add:
      (a) len(lower) == len(upper) or len(lower) == len(upper) + 1;
      (b) max(lower) <= min(upper).
    Fixing (b): when lower[-1] (its max, via -lower[0]) > upper[0],
    swap the two tops. Fixing (a): if upper ever gets taller, migrate
    its minimum to the lower heap. Median always reads off the seam.
---------------------------------------------------------------------
TIME COMPLEXITY : O(log n) per addNum ; O(1) findMedian.
MEMORY COMPLEXITY: O(n).
=====================================================================
"""
import heapq, bisect, time, tracemalloc


class Solution_1:
    """Two-heap median — the classic streaming solution."""

    def __init__(self):
        self.lower = []                    # max-heap via negation
        self.upper = []                    # min-heap

    def addNum(self, num):
        heapq.heappush(self.lower, -num)
        if self.lower and self.upper and -self.lower[0] > self.upper[0]:
            heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.lower) > len(self.upper) + 1:
            heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def findMedian(self):
        if len(self.lower) > len(self.upper):
            return -self.lower[0]
        return (-self.lower[0] + self.upper[0]) / 2.0


class Solution_2:
    """Sorted-list baseline: O(n) insert."""

    def __init__(self):
        self.data = []

    def addNum(self, num):
        self.data.insert(bisect.bisect_left(self.data, num), num)

    def findMedian(self):
        n = len(self.data)
        if n % 2:
            return self.data[n // 2]
        return (self.data[n // 2 - 1] + self.data[n // 2]) / 2.0


if __name__ == "__main__":
    steps = [(1, 1.0), (2, 1.5), (3, 2.0), (4, 2.5), (5, 3.0)]
    tracemalloc.start()
    t0 = time.perf_counter()
    s1, s2 = Solution_1(), Solution_2()
    ok = True
    for val, want in steps:
        s1.addNum(val)
        s2.addNum(val)
        r1, r2 = s1.findMedian(), s2.findMedian()
        ok &= r1 == want and r2 == want
        print(f"after {val} -> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all steps' if ok else 'FAIL'} | time: {dt * 1e6:.0f} us | mem: {mem:.0f} KB")
