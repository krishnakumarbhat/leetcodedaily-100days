"""
LeetCode 15: 3Sum
Link: https://leetcode.com/problems/3sum/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Three nested loops to find all combinations of three distinct 
# numbers. Then check if their sum is 0. A set stores sorted triplets to skip duplicates.
# Time Complexity: O(n^3)   Space Complexity: O(n)
class Solution_v1:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = set()
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                for k in range(j + 1, len(nums)):
                    if nums[i] + nums[j] + nums[k] == 0:
                        result.add((nums[i], nums[j], nums[k]))
        return [list(t) for t in result]

# ============= Variation 2: Hash Set =============
# Algorithm: Iterate through elements. For each `nums[i]`, use a hash set 
# inside the inner loop to find two other elements that sum to `-nums[i]`.
# Time Complexity: O(n^2)   Space Complexity: O(n)
class Solution_v2:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]: continue
            seen = set()
            for j in range(i + 1, len(nums)):
                comp = -nums[i] - nums[j]
                if comp in seen:
                    result.append([nums[i], comp, nums[j]])
                    while j + 1 < len(nums) and nums[j] == nums[j + 1]: j += 1
                seen.add(nums[j])
        return result

# ============= Variation 3: Two Pointers =============
# Algorithm: Sort exactly once. Iterate over one variable `nums[i]`.
# Use two pointers (`l`, `r`) starting just after `i` and at the end of the array 
# to find a zero sum. Skip duplicate numbers manually when zero-sum is found.
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v3:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]: continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == 0:
                    result.append([nums[i], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l + 1]: l += 1
                    while l < r and nums[r] == nums[r - 1]: r -= 1
                    l += 1; r -= 1
                elif s < 0: l += 1
                else: r -= 1
        return result

# ============= Benchmarking =============
if __name__ == "__main__":
    nums = [-1, 0, 1, 2, -1, -4, 3, -2, 5, -3]
    solutions = [Solution_v1, Solution_v2, Solution_v3]
    names = ["Brute Force", "Hash Set", "Two Pointers"]
    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().threeSum(nums[:])
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): triplets={len(result)}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 4144 bytes and time = 113.01 µs
# var2 mem = 2576 bytes and time = 52.75 µs
# var3 mem = 1008 bytes and time = 26.10 µs
