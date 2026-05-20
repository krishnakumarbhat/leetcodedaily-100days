"""
LeetCode 42: Trapping Rain Water
Link: https://leetcode.com/problems/trapping-rain-water/
Difficulty: Hard
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: For each bar at index i, calculate the max height to its left and right. 
# The water trapped on top of it is min(left_max, right_max) - height[i].
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def trap(self, height: List[int]) -> int:
        water = 0
        for i in range(len(height)):
            left_max = max(height[:i + 1]) if i >= 0 else 0
            right_max = max(height[i:]) if i < len(height) else 0
            water += min(left_max, right_max) - height[i]
        return water

# ============= Variation 2: Prefix Max Arrays =============
# Algorithm: Pre-compute left and right maximum boundaries into array maps `left` 
# and `right`. The bottleneck max bound at any index `i` is obtained instantly in O(1).
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def trap(self, height: List[int]) -> int:
        if not height: return 0
        n = len(height)
        left_max = [0] * n
        right_max = [0] * n
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])
        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])
        water = 0
        for i in range(n):
            water += min(left_max[i], right_max[i]) - height[i]
        return water

# ============= Variation 3: Two Pointers =============
# Algorithm: Maintain left and right pointers. Calculate which bound is strictly 
# smaller between left/right_max. Move pointer to smaller boundary inwards, storing water.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v3:
    def trap(self, height: List[int]) -> int:
        if not height: return 0
        l, r = 0, len(height) - 1
        left_max, right_max = height[l], height[r]
        water = 0
        while l < r:
            if left_max < right_max:
                l += 1
                left_max = max(left_max, height[l])
                water += left_max - height[l]
            else:
                r -= 1
                right_max = max(right_max, height[r])
                water += right_max - height[r]
        return water

# ============= Variation 4: Stack =============
# Algorithm: Use a monotonically decreasing stack. When a height greater than the 
# stack's top is found, pop elements. The popped element forms a "valley".
# Calculate bounded volume.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v4:
    def trap(self, height: List[int]) -> int:
        stack = []
        water = 0
        for i in range(len(height)):
            while stack and height[i] > height[stack[-1]]:
                top = stack.pop()
                if not stack: break
                distance = i - stack[-1] - 1
                bounded_height = min(height[i], height[stack[-1]]) - height[top]
                water += distance * bounded_height
            stack.append(i)
        return water

# ============= Benchmarking =============
if __name__ == "__main__":
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    solutions = [Solution_v1, Solution_v2, Solution_v3, Solution_v4]
    names = ["Brute Force", "Prefix Max", "Two Pointers", "Stack"]
    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().trap(height[:])
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 808 bytes and time = 52.55 µs
# var2 mem = 1136 bytes and time = 49.77 µs
# var3 mem = 656 bytes and time = 13.32 µs
# var4 mem = 760 bytes and time = 20.96 µs
