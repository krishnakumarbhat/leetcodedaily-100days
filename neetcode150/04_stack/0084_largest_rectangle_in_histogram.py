"""
LeetCode 84: Largest Rectangle in Histogram
Link: https://leetcode.com/problems/largest-rectangle-in-histogram/
Difficulty: Hard
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: For every bar `i`, try all widths `j` from `i` to `n-1`. 
# Track the relative minimum height in that range to calculate area.
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        for i in range(len(heights)):
            min_h = heights[i]
            for j in range(i, len(heights)):
                min_h = min(min_h, heights[j])
                max_area = max(max_area, min_h * (j - i + 1))
        return max_area

# ============= Variation 2: Monotonic Stack =============
# Algorithm: Maintain an increasing stack of indices. When a shorter bar is found, 
# it bounds the previously seen bars. Pop and calculate area using the width 
# between current index `i` and the bar's predecessor in the stack.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []; max_area = 0
        for i, h in enumerate(heights + [0]):
            while stack and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)
        return max_area

if __name__ == "__main__":
    heights = [2, 1, 5, 6, 2, 3]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Mono Stack"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().largestRectangleArea(heights[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 720 bytes and time = 41.10 µs
# var2 mem = 1104 bytes and time = 29.78 µs
