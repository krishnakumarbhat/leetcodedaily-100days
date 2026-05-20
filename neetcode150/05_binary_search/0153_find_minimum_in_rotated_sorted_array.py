"""
LeetCode 153: Find Minimum in Rotated Sorted Array
Link: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Linear Scan =============
# Algorithm: Use the built-in `min()` function. 
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v1:
    def findMin(self, nums: List[int]) -> int:
        return min(nums)

# ============= Variation 2: Binary Search =============
# Algorithm: Check if the current range is already sorted (`nums[l] < nums[r]`). 
# If not, use `mid` to determine which side contains the pivot/minimum.
# Time Complexity: O(log n)   Space Complexity: O(1)
class Solution_v2:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        result = nums[0]
        while l <= r:
            if nums[l] < nums[r]: result = min(result, nums[l]); break
            mid = (l + r) // 2
            result = min(result, nums[mid])
            if nums[mid] >= nums[l]: l = mid + 1
            else: r = mid - 1
        return result

if __name__ == "__main__":
    nums = [3, 4, 5, 1, 2]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Linear", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().findMin(nums[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 544 bytes and time = 17.17 µs
# var2 mem = 648 bytes and time = 10.23 µs
