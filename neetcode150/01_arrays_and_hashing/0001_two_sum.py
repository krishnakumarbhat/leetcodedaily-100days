"""
LeetCode 1: Two Sum
Link: https://leetcode.com/problems/two-sum/
Difficulty: Easy
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Iterate through each element in the array. For each element, iterate through
# the remaining elements to check if their sum equals the target.
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

# ============= Variation 2: Two-pass Hash Map =============
# Algorithm: In the first pass, insert each element's value and its index into a hash map.
# In the second pass, check if each element's complement (target - element) exists in the 
# hash map. If it does, return the current index and complement's index.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for i, num in enumerate(nums):
            hashmap[num] = i
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hashmap and hashmap[complement] != i:
                return [i, hashmap[complement]]
        return []

# ============= Variation 3: One-pass Hash Map =============
# Algorithm: Iterate through the array once. Check if the complement of the current 
# element exists in the hash map. If yes, return the pair. If not, add the current 
# element to the hash map and continue.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v3:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in hashmap:
                return [hashmap[complement], i]
            hashmap[num] = i
        return []

# ============= Variation 4: Sort + Two Pointers =============
# Algorithm: Store original indices alongside values, then sort the array. 
# Use a left and right pointer. Sum the values; if the sum is too small, increment 
# the left pointer. If it's too large, decrement the right pointer. Repeat until found.
# Time Complexity: O(n log n)   Space Complexity: O(n)
class Solution_v4:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        nums_sorted = sorted([(num, i) for i, num in enumerate(nums)])
        l, r = 0, len(nums) - 1
        while l < r:
            curr_sum = nums_sorted[l][0] + nums_sorted[r][0]
            if curr_sum == target:
                return [nums_sorted[l][1], nums_sorted[r][1]]
            elif curr_sum < target:
                l += 1
            else:
                r -= 1
        return []

# ============= Benchmarking =============
if __name__ == "__main__":
    nums = [2, 7, 11, 15, 1, 3, 5, 8, 4, 6]
    target = 9
    solutions = [Solution_v1, Solution_v2, Solution_v3, Solution_v4]
    names = ["Brute Force", "Two-pass HashMap", "One-pass HashMap", "Sort + Two Pointers"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().twoSum(nums[:], target)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 728 bytes and time = 16.80 µs
# var2 mem = 1184 bytes and time = 15.42 µs
# var3 mem = 720 bytes and time = 8.38 µs
# var4 mem = 1968 bytes and time = 20.56 µs
