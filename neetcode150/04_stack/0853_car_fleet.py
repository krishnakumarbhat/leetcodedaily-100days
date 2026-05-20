"""
LeetCode 853: Car Fleet
Link: https://leetcode.com/problems/car-fleet/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Sort + Stack =============
# Algorithm: Sort cars by starting position in reverse order. Calculate time needed 
# to reach `target`. If a car reaches earlier or at the same time as the one ahead, 
# it joins the fleet.
# Time Complexity: O(n log n)   Space Complexity: O(n)
class Solution_v1:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pairs = sorted(zip(position, speed), reverse=True)
        stack = []
        for pos, spd in pairs:
            t = (target - pos) / spd
            if not stack or t > stack[-1]:
                stack.append(t)
        return len(stack)

if __name__ == "__main__":
    target, position, speed = 12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]
    tracemalloc.start(); t0 = time.perf_counter()
    result = Solution_v1().carFleet(target, position, speed)
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1 (Sort+Stack): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1048 bytes and time = 37.27 µs
