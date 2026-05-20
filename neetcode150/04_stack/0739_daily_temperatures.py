"""
LeetCode 739: Daily Temperatures
Link: https://leetcode.com/problems/daily-temperatures/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: For each temperature, scan all following indices for a higher temperature. 
# Calculate the index difference and result.
# Time Complexity: O(n^2)   Space Complexity: O(n)
class Solution_v1:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures); result = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if temperatures[j] > temperatures[i]:
                    result[i] = j - i; break
        return result

# ============= Variation 2: Monotonic Stack =============
# Algorithm: Use a decreasing stack to store indices. When seeing a hotter day, 
# pop indices and calculate the wait time as `current_idx - popped_idx`.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures); result = [0] * n; stack = []
        for i in range(n):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                idx = stack.pop(); result[idx] = i - idx
            stack.append(i)
        return result

if __name__ == "__main__":
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Mono Stack"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().dailyTemperatures(temps[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 840 bytes and time = 28.54 µs
# var2 mem = 912 bytes and time = 21.80 µs
