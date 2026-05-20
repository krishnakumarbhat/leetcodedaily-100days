"""
LeetCode 128: Longest Consecutive Sequence
Link: https://leetcode.com/problems/longest-consecutive-sequence/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Sorting =============
# Algorithm: Sort the array first. Iterate through, counting consecutive numbers.
# Reset the counter when the sequence breaks (i.e. diff > 1). Keep track of the max.
# Time Complexity: O(n log n)   Space Complexity: O(1)
class Solution_v1:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        nums.sort()
        longest = 1
        current = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                continue
            if nums[i] == nums[i - 1] + 1:
                current += 1
            else:
                current = 1
            longest = max(longest, current)
        return longest

# ============= Variation 2: Hash Set =============
# Algorithm: Add all numbers to a hash set for O(1) lookups. Iterate through the set.
# If `num - 1` is not in the set, `num` is the start of a sequence. Count upwards 
# to find the length of the sequence. This ensures O(n) overall time.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0
        for num in num_set:
            if num - 1 not in num_set:  # start of sequence
                current = num
                streak = 1
                while current + 1 in num_set:
                    current += 1
                    streak += 1
                longest = max(longest, streak)
        return longest

# ============= Variation 3: Union Find =============
# Algorithm: Treat each number as a node. Connect consecutive numbers using Union-Find.
# The maximum component size in the disjoint set is the longest consecutive sequence.
# Time Complexity: O(n α(n))   Space Complexity: O(n)
class Solution_v3:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        parent = {}
        size = {}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px == py: return
            if size[px] < size[py]: px, py = py, px
            parent[py] = px
            size[px] += size[py]

        for num in nums:
            if num not in parent:
                parent[num] = num
                size[num] = 1
                if num - 1 in parent: union(num, num - 1)
                if num + 1 in parent: union(num, num + 1)

        return max(size.values()) if size else 0

# ============= Benchmarking =============
if __name__ == "__main__":
    nums = [100, 4, 200, 1, 3, 2, 5, 6, 7, 8]
    solutions = [Solution_v1, Solution_v2, Solution_v3]
    names = ["Sorting", "Hash Set", "Union Find"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().longestConsecutive(nums[:])
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 1792 bytes and time = 30.26 µs
# var2 mem = 1488 bytes and time = 15.22 µs
# var3 mem = 3456 bytes and time = 41.32 µs
