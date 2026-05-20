"""LeetCode 90: Subsets II - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: Sort + skip duplicates backtracking
class Solution_v1:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort(); res = []
        def bt(i, cur):
            res.append(cur[:])
            for j in range(i, len(nums)):
                if j > i and nums[j] == nums[j - 1]: continue
                cur.append(nums[j]); bt(j + 1, cur); cur.pop()
        bt(0, []); return res

# Variation 2: Use set to deduplicate
class Solution_v2:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort(); seen = set(); res = []
        def bt(i, cur):
            key = tuple(cur)
            if key in seen: return
            seen.add(key); res.append(cur[:])
            for j in range(i, len(nums)):
                cur.append(nums[j]); bt(j + 1, cur); cur.pop()
        bt(0, []); return res

if __name__ == "__main__":
    nums = [1, 2, 2]
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().subsetsWithDup(nums[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {len(r)} unique subsets, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
