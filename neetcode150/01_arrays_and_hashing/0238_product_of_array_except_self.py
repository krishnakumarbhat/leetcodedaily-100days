"""
LeetCode 238: Product of Array Except Self
Link: https://leetcode.com/problems/product-of-array-except-self/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: For each element at index i, compute the product of all other elements at 
# index j where j != i. This uses two nested loops.
# Time Complexity: O(n^2)   Space Complexity: O(n)
class Solution_v1:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n
        for i in range(n):
            for j in range(n):
                if i != j:
                    result[i] *= nums[j]
        return result

# ============= Variation 2: Prefix & Suffix Arrays =============
# Algorithm: Calculate standard prefix and suffix products using two separate arrays. 
# Re-iterate through the arrays to multiply prefix[i] and suffix[i] for the answer.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        prefix = [1] * n
        suffix = [1] * n
        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]
        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]
        return [prefix[i] * suffix[i] for i in range(n)]

# ============= Variation 3: Optimized O(1) Space =============
# Algorithm: Compute the prefix product directly into the results array. 
# Then, make a second pass backwards, keeping a running suffix product and 
# multiplying it into the results array. This avoids allocating extra arrays.
# Time Complexity: O(n)   Space Complexity: O(1) (output not counted)
class Solution_v3:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]
        return result

# ============= Benchmarking =============
if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    solutions = [Solution_v1, Solution_v2, Solution_v3]
    names = ["Brute Force", "Prefix+Suffix", "Optimized O(1)"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().productExceptSelf(nums[:])
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 2260 bytes and time = 55.47 µs
# var2 mem = 2468 bytes and time = 38.14 µs
# var3 mem = 1092 bytes and time = 19.25 µs
