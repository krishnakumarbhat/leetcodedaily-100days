"""
LeetCode 875: Koko Eating Bananas
Link: https://leetcode.com/problems/koko-eating-bananas/
Difficulty: Medium
"""
import time, tracemalloc, math
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Linearly try every possible speed `k` from 1 up to `max(piles)`.
# Time Complexity: O(max(piles) * n)   Space Complexity: O(1)
class Solution_v1:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        for k in range(1, max(piles) + 1):
            total = sum(math.ceil(p / k) for p in piles)
            if total <= h: return k
        return max(piles)

# ============= Variation 2: Binary Search =============
# Algorithm: Binary search over the range of possible speeds `[1, max(piles)]`. 
# For each `mid`, calculate total hours and adjust boundaries to find minimum `k`.
# Time Complexity: O(n * log(max(piles)))   Space Complexity: O(1)
class Solution_v2:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l, r = 1, max(piles)
        result = r
        while l <= r:
            k = (l + r) // 2
            total = sum(math.ceil(p / k) for p in piles)
            if total <= h: result = k; r = k - 1
            else: l = k + 1
        return result

if __name__ == "__main__":
    piles, h = [3, 6, 7, 11], 8
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().minEatingSpeed(piles[:], h)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 2008 bytes and time = 45.71 µs
# var2 mem = 1328 bytes and time = 20.45 µs
