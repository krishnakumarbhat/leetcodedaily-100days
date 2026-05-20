"""
LeetCode 704: Binary Search
Link: https://leetcode.com/problems/binary-search/
Difficulty: Easy
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Iterative =============
# Algorithm: Standard `left` and `right` pointer logic. Calculates `mid` and 
# narrows search range until target is found or pointers cross.
# Time Complexity: O(log n)   Space Complexity: O(1)
class Solution_v1:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            elif nums[mid] < target: l = mid + 1
            else: r = mid - 1
        return -1

# ============= Variation 2: Recursive =============
# Algorithm: Same as iterative but uses function calls. Base case is `l > r`.
# Time Complexity: O(log n)   Space Complexity: O(log n)
class Solution_v2:
    def search(self, nums: List[int], target: int) -> int:
        def bs(l, r):
            if l > r: return -1
            mid = (l + r) // 2
            if nums[mid] == target: return mid
            elif nums[mid] < target: return bs(mid + 1, r)
            else: return bs(l, mid - 1)
        return bs(0, len(nums) - 1)

if __name__ == "__main__":
    nums, target = [-1, 0, 3, 5, 9, 12], 9
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Iterative", "Recursive"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().search(nums[:], target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1560 bytes and time = 10.41 µs
# var2 mem = 1728 bytes and time = 14.66 µs
