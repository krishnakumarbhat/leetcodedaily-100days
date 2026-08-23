"""
=====================================================================
LeetCode 217 : Contains Duplicate                              (Easy)
https://leetcode.com/problems/contains-duplicate/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Return true if any value appears at least twice in the array,
    false if every element is distinct.
---------------------------------------------------------------------
INTUITION
    "Seen it before?" is literally the job of a hash set: O(1)
    insert + O(1) membership test. Scan once, remember everything,
    and the first repeat answers the question.
---------------------------------------------------------------------
APPROACH 1 — Hash set (BEST)
    Time  Complexity : O(n)   Space Complexity : O(n)
    Python `set` = dict without values (open addressing + linear
    probing, h(k,i) = (hash(k)+i) mod m) — one contiguous table,
    tiny memory, great cache locality.
---------------------------------------------------------------------
APPROACH 2 — Sort + adjacent scan (zero extra memory)
    Time  Complexity : O(n log n)   Space Complexity : O(1)
    Wins when memory is critical; loses the O(n) time bound.
---------------------------------------------------------------------
REAL LIFE
    • Login systems: is this username taken? (uniqueness check)
    • Deduplicating logs, inventory SKUs, search-engine crawlers.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List


# =====================================================================
# APPROACH 1 : Hash set — remember everything you have seen
# =====================================================================
class Solution_HashSet:
    """
    Purpose : Detect whether any value repeats inside `nums`.
    Inputs  : nums — array of integers to inspect.
    Output  : True if a duplicate exists, False otherwise.
    """

    def containsDuplicate(self, nums: List[int]) -> bool:
        # seen : every distinct value we have walked past so far.
        seen = set()

        # Walk every element exactly once.
        for num in nums:
            # If this value is already stored → second occurrence → True.
            if num in seen:
                return True

            # First occurrence → remember it for the future.
            seen.add(num)

        # Loop finished with no repeats → every element was distinct.
        return False


# =====================================================================
# APPROACH 2 : Sort + adjacent scan — zero extra memory
# =====================================================================
class Solution_SortAdjacent:
    """
    Purpose : Detect whether any value repeats inside `nums`.
    Inputs  : nums — array of integers to inspect.
    Output  : True if a duplicate exists, False otherwise.
    """

    def containsDuplicate(self, nums: List[int]) -> bool:
        # Sorting groups equal values side by side — the O(n log n) step.
        # Timsort is in-place (needs O(1) aux memory for small inputs).
        nums.sort()

        # Walk the sorted array comparing each element with its neighbour.
        for i in range(1, len(nums)):
            # Two equal neighbours = a duplicate exists.
            if nums[i] == nums[i - 1]:
                return True

        # No equal neighbours anywhere → all distinct.
        return False


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    # Sample with duplicates sprinkled in.
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 3]

    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_HashSet().containsDuplicate(nums)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t2 = time.perf_counter()
    r2 = Solution_SortAdjacent().containsDuplicate(nums)
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (hash set)          : {r1}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (sort + adjacent)   : {r2}  time = {(t3 - t2) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree." if r1 == r2 else "FAIL : approaches disagree.")