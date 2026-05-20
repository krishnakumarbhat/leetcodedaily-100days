"""
LeetCode 217: Contains Duplicate
Link: https://leetcode.com/problems/contains-duplicate/
Difficulty: Easy
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Compare every element against every other element using two nested loops.
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def containsDuplicate(self, nums: List[int]) -> bool:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False

# ============= Variation 2: Sorting =============
# Algorithm: Sort the array first. If there are duplicates, they will be adjacent.
# Iterate through the array and check if nums[i] == nums[i-1].
# Time Complexity: O(n log n)   Space Complexity: O(1) in-place
class Solution_v2:
    def containsDuplicate(self, nums: List[int]) -> bool:
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return True
        return False

# ============= Variation 3: Hash Set =============
# Algorithm: Use a hash set to keep track of seen elements. Iterating through the array,
# return True if an element is already in the set, otherwise add it.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v3:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

# ============= Benchmarking =============
if __name__ == "__main__":
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    solutions = [Solution_v1, Solution_v2, Solution_v3]
    names = ["Brute Force", "Sorting", "Hash Set"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        data = test_data[:]
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().containsDuplicate(data)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 640 bytes and time = 20.01 µs
# var2 mem = 584 bytes and time = 10.16 µs
# var3 mem = 1264 bytes and time = 8.20 µs
