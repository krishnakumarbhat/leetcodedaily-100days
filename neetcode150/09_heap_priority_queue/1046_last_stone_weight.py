"""LeetCode 1046: Last Stone Weight - Easy"""
import time, tracemalloc
import heapq
from typing import List

# Variation 1: Max-heap (negate for min-heap)
class Solution_v1:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = [-s for s in stones]
        heapq.heapify(heap)
        while len(heap) > 1:
            a = -heapq.heappop(heap)
            b = -heapq.heappop(heap)
            if a != b: heapq.heappush(heap, -(a - b))
        return -heap[0] if heap else 0

# Variation 2: Sorted list (brute force)
class Solution_v2:
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones = sorted(stones)
        while len(stones) > 1:
            a, b = stones.pop(), stones.pop()
            if a != b:
                import bisect; bisect.insort(stones, a - b)
        return stones[0] if stones else 0

# Variation 3: Counting sort (when values bounded)
class Solution_v3:
    def lastStoneWeight(self, stones: List[int]) -> int:
        max_val = max(stones)
        count = [0] * (max_val + 1)
        for s in stones: count[s] += 1
        cur = max_val
        while cur > 0:
            if count[cur] == 0: cur -= 1; continue
            if count[cur] % 2 == 0: cur -= 1; continue
            # one stone left at cur, smash with next largest
            j = cur - 1
            while j > 0 and count[j] == 0: j -= 1
            if j == 0: return cur
            count[cur] -= 1; count[j] -= 1; count[cur - j] += 1
            cur = max(cur, cur - j)
        return 0

if __name__ == "__main__":
    stones = [2, 7, 4, 1, 8, 1]
    for Vi, Cls in enumerate([Solution_v1, Solution_v2, Solution_v3], 1):
        import copy; s = copy.deepcopy(stones)
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().lastStoneWeight(s)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: result={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
