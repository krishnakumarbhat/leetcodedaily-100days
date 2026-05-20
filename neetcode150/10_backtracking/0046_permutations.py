"""LeetCode 46: Permutations - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: Backtracking with used set
class Solution_v1:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []; used = [False] * len(nums)
        def bt(cur):
            if len(cur) == len(nums): res.append(cur[:]); return
            for i in range(len(nums)):
                if used[i]: continue
                used[i] = True; cur.append(nums[i]); bt(cur)
                cur.pop(); used[i] = False
        bt([]); return res

# Variation 2: Swap in-place
class Solution_v2:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        def bt(start):
            if start == len(nums): res.append(nums[:]); return
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                bt(start + 1)
                nums[start], nums[i] = nums[i], nums[start]
        bt(0); return res

# Variation 3: Recursive insertion
class Solution_v3:
    def permute(self, nums: List[int]) -> List[List[int]]:
        if not nums: return [[]]
        res = []
        for i, n in enumerate(nums):
            for p in self.permute(nums[:i] + nums[i+1:]):
                res.append([n] + p)
        return res

if __name__ == "__main__":
    nums = [1, 2, 3]
    for Vi, Cls in enumerate([Solution_v1, Solution_v2, Solution_v3], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().permute(nums[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {len(r)} perms, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
