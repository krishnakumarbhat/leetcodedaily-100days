"""
LeetCode 11: Container With Most Water
Link: https://leetcode.com/problems/container-with-most-water/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Iterate all pairs of lines. For each pair (i, j), the area relies on 
# the minimum of the two heights multiplied by the distance between them (j - i). 
# Track the maximum area over all possible pairs.
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def maxArea(self, height: List[int]) -> int:
        max_area = 0
        for i in range(len(height)):
            for j in range(i + 1, len(height)):
                area = min(height[i], height[j]) * (j - i)
                max_area = max(max_area, area)
        return max_area

# ============= Variation 2: Two Pointers =============
# Algorithm: Start with a pointer at each end of the array. Callulate area.
# To greedily maximize area, increment the pointer that points to the shorter line 
# inward, hoping to find a taller line. Repeat until pointers cross.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v2:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        max_area = 0
        while l < r:
            area = min(height[l], height[r]) * (r - l)
            max_area = max(max_area, area)
            if height[l] < height[r]: l += 1
            else: r -= 1
        return max_area

# ============= Benchmarking =============
if __name__ == "__main__":
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    solutions = [Solution_v1, Solution_v2]
    names = ["Brute Force", "Two Pointers"]
    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().maxArea(height[:])
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 1584 bytes and time = 60.34 µs
# var2 mem = 680 bytes and time = 17.42 µs
