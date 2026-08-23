"""
=====================================================================
LeetCode 128 : Longest Consecutive Sequence                    (Medium)
https://leetcode.com/problems/longest-consecutive-sequence/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Given an unsorted array, return the length of the longest run of
    consecutive integers (e.g. [100,4,200,1,3,2] → 4 for 1,2,3,4).
    MUST run in O(n) time.
---------------------------------------------------------------------
INTUITION
    A run like 1,2,3,4 can be grown from its FIRST element only:
    count up while (x+1) exists — an O(1) hash-set lookup. To avoid
    restarting from the middle of an existing run, only start
    counting at numbers whose predecessor (x-1) is NOT in the set.
    Every number is then touched O(1) times amortized → O(n) total.
---------------------------------------------------------------------
APPROACH 1 — Hash set + head-of-run growth (BEST)
    Time  Complexity : O(n)   Space Complexity : O(n)
    WHY the "x-1 in set?" guard matters: without it, [1,2,3,4] would
    trigger counting from 1,2,3,4 → O(n²). With it, only 1 counts.
    Python set = open addressing + linear probing: h(k,i) =
    (hash(k)+i) mod m → one contiguous table, great cache locality.
---------------------------------------------------------------------
APPROACH 2 — Sort + linear scan
    Time  Complexity : O(n log n)   Space Complexity : O(1)
    Wins when memory is tight; loses the O(n) requirement.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List


# =====================================================================
# APPROACH 1 : Hash set + head-of-run growth — O(n)
# =====================================================================
class Solution_HashSet:
    """
    Purpose : Return the longest run of consecutive integers.
    Inputs  : nums — unsorted array of integers.
    Output  : length of the longest consecutive sequence.
    """

    def longestConsecutive(self, nums: List[int]) -> int:
        # Throw everything into a set: O(1) "does x exist?" later.
        # Python's set = dict without values (linear probing table).
        seen = set(nums)

        # best : longest run discovered so far.
        best = 0

        # Inspect every distinct number exactly once.
        for x in seen:
            # Only start a run at its HEAD: x-1 must be absent.
            # This single guard keeps the whole algorithm O(n).
            if x - 1 in seen:
                continue  # x is mid-run → some smaller head owns it

            # Grow the run upward while consecutive numbers exist.
            length = 1
            while x + length in seen:
                length += 1  # extend the run by one

            # Keep the global maximum.
            best = max(best, length)

        return best


# =====================================================================
# APPROACH 2 : Sort + linear scan — O(n log n)
# =====================================================================
class Solution_SortScan:
    """
    Purpose : Return the longest run of consecutive integers.
    Inputs  : nums — unsorted array of integers.
    Output  : length of the longest consecutive sequence.
    """

    def longestConsecutive(self, nums: List[int]) -> int:
        # Sorting groups each run into a contiguous stretch — O(n log n).
        nums.sort()

        # Edge case: empty input has no run at all.
        if not nums:
            return 0

        # cur/best : run length ending here / global maximum.
        cur = 1
        best = 1

        # Sweep the sorted array once.
        for i in range(1, len(nums)):
            # Duplicates do not extend a run — skip them silently.
            if nums[i] == nums[i - 1]:
                continue

            # Consecutive value → the current run grows by one.
            if nums[i] == nums[i - 1] + 1:
                cur += 1
            else:
                # Gap → the run broke; start a fresh run of length 1.
                cur = 1

            # Track the global maximum after every element.
            best = max(best, cur)

        return best


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    # Official example (1,2,3,4 → 4).
    nums = [100, 4, 200, 1, 3, 2]

    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_HashSet().longestConsecutive(nums)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t2 = time.perf_counter()
    r2 = Solution_SortScan().longestConsecutive(nums)
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (hash set, head-of-run) : {r1}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (sort + scan)           : {r2}  time = {(t3 - t2) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree." if r1 == r2 else "FAIL : approaches disagree.")