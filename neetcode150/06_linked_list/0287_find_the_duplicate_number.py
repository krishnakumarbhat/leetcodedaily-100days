"""
LeetCode 287: Find the Duplicate Number - Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Sorting =============
# Time: O(n log n)   Space: O(1)
class Solution_v1:
    def findDuplicate(self, nums: List[int]) -> int:
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i-1]: return nums[i]

# ============= Variation 2: Floyd's Cycle Detection =============
# Time: O(n)   Space: O(1)
class Solution_v2:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = 0
        while True:
            slow = nums[slow]; fast = nums[nums[fast]]
            if slow == fast: break
        slow2 = 0
        while slow != slow2:
            slow = nums[slow]; slow2 = nums[slow2]
        return slow

if __name__ == "__main__":
    nums = [1, 3, 4, 2, 2]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Sorting", "Floyd"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().findDuplicate(nums[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
