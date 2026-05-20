"""
LeetCode 33: Search in Rotated Sorted Array
Link: https://leetcode.com/problems/search-in-rotated-sorted-array/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Linear Scan =============
# Algorithm: Use the built-in `index` method or a loop to find the target. 
# Simplest approach but doesn't leverage the sorted property.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v1:
    def search(self, nums: List[int], target: int) -> int:
        return nums.index(target) if target in nums else -1

# ============= Variation 2: Binary Search =============
# Algorithm: Identify which half is sorted. Peek at the sorted half to decide 
# whether to search within it or the rotated half.
# Time Complexity: O(log n)   Space Complexity: O(1)
class Solution_v2:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]: r = mid - 1
                else: l = mid + 1
            else:
                if nums[mid] < target <= nums[r]: l = mid + 1
                else: r = mid - 1
        return -1

if __name__ == "__main__":
    nums, target = [4, 5, 6, 7, 0, 1, 2], 0
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Linear", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().search(nums[:], target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1536 bytes and time = 13.21 µs
# var2 mem = 552 bytes and time = 7.99 µs
