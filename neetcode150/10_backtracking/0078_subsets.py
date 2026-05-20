"""LeetCode 78: Subsets - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: Iterative bitmask - iterate and duplicate
class Solution_v1:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = [[]]
        for n in nums:
            res += [s + [n] for s in res]
        return res

# Variation 2: Backtracking DFS
class Solution_v2:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        def bt(i, cur):
            res.append(cur[:])
            for j in range(i, len(nums)):
                cur.append(nums[j]); bt(j + 1, cur); cur.pop()
        bt(0, []); return res

# Variation 3: Binary bitmask (2^n subsets)
class Solution_v3:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums); res = []
        for mask in range(1 << n):
            res.append([nums[i] for i in range(n) if mask & (1 << i)])
        return res

if __name__ == "__main__":
    nums = [1, 2, 3]
    for Vi, Cls in enumerate([Solution_v1, Solution_v2, Solution_v3], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().subsets(nums[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {len(r)} subsets, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
