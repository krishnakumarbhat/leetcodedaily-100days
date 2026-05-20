"""
LeetCode 167: Two Sum II - Input Array Is Sorted
Link: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Iterate blindly every combination to see if `nums[i] + nums[j] == target`.
# The 1-based indices are constructed at the end.
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] + numbers[j] == target:
                    return [i + 1, j + 1]
        return []

# ============= Variation 2: Binary Search =============
# Algorithm: The array is sorted! So for each base element `numbers[i]`, we binary 
# search bounds checking `target - numbers[i]` on elements from `i+1` onwards.
# Time Complexity: O(n log n)   Space Complexity: O(1)
class Solution_v2:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        for i in range(len(numbers)):
            comp = target - numbers[i]
            lo, hi = i + 1, len(numbers) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if numbers[mid] == comp: return [i + 1, mid + 1]
                elif numbers[mid] < comp: lo = mid + 1
                else: hi = mid - 1
        return []

# ============= Variation 3: Two Pointers =============
# Algorithm: Place L at the start and R at the back. Sum them. If the sum is explicitly 
# too big, shrink R. If too small, grow L. O(n) scan.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v3:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1
        while l < r:
            s = numbers[l] + numbers[r]
            if s == target: return [l + 1, r + 1]
            elif s < target: l += 1
            else: r -= 1
        return []

# ============= Benchmarking =============
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 15]
    target = 17
    solutions = [Solution_v1, Solution_v2, Solution_v3]
    names = ["Brute Force", "Binary Search", "Two Pointers"]
    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().twoSum(numbers[:], target)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 728 bytes and time = 27.04 µs
# var2 mem = 776 bytes and time = 11.29 µs
# var3 mem = 592 bytes and time = 4.61 µs
