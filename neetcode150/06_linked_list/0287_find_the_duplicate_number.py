"""
=====================================================================
LeetCode 287 : Find the Duplicate Number                     (Medium)
https://leetcode.com/problems/find-the-duplicate-number/
Category   : Linked List
---------------------------------------------------------------------
PROBLEM
    nums has n+1 integers in [1, n]; exactly ONE value repeats.
    Find it WITHOUT modifying nums and with O(1) extra space.
---------------------------------------------------------------------
INTUITION
    Treat the array as a function f(i) = nums[i]. Chasing values
    (i → nums[i] → nums[nums[i]] → …) walks an IMPLICIT linked
    list of indices. A repeated value means two indices point at
    the same value → the walk must cycle, and the cycle's ENTRY
    is the duplicate. Floyd's detection (0141) in a new skin.
---------------------------------------------------------------------
APPROACH 1 — Floyd's tortoise and hare on the array (BEST)
    slow = nums[slow], fast = nums[nums[fast]] until they meet;
    then slow and a fresh pointer from 0 advance equally and meet
    at the cycle entry = the answer.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Hash set of seen values
    First value seen twice is the answer.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Duplicate/integrity detection in ID registries where the
      dataset is too big for a hash set (the O(1)-space win).
    • Any "find the repeated element" where the values form a
      functional graph (pointers, deduplication pipelines).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List


# =====================================================================
# APPROACH 1 : Floyd's tortoise and hare on the index graph (best)
# =====================================================================
class Solution_Floyd:
    """
    Purpose : Find the duplicated value in O(1) extra space.
    Inputs  : nums — n+1 values in [1, n], exactly one duplicate.
    Output  : The duplicated value.
    """

    def findDuplicate(self, nums: List[int]) -> int:
        # Phase 1 — DETECT the cycle: slow 1 hop, fast 2 hops.
        # A cycle exists, so the pointers MUST eventually meet.
        slow = 0
        fast = 0
        while True:
            slow = nums[slow]           # 1 hop: i → nums[i]
            fast = nums[nums[fast]]     # 2 hops
            if slow == fast:
                break

        # Phase 2 — FIND the entry: from index 0 and from the meeting
        # point, advance at EQUAL speed → collision at the entry,
        # whose VALUE is the duplicate.
        slow2 = 0
        while slow != slow2:
            slow = nums[slow]
            slow2 = nums[slow2]
        return slow


# =====================================================================
# APPROACH 2 : Hash set of seen values
# =====================================================================
class Solution_HashSet:
    """
    Purpose : Find the duplicated value with a hash set.
    Inputs  : nums — n+1 values in [1, n], exactly one duplicate.
    Output  : The duplicated value.
    Note    : O(n) space — the set.
    """

    def findDuplicate(self, nums: List[int]) -> int:
        seen: set[int] = set()           # Python set = open addressing
        for v in nums:
            if v in seen:                # second sighting → duplicate
                return v
            seen.add(v)
        return -1                        # unreachable per statement


# =====================================================================
# BENCHMARK — 3 tests, both approaches, time + peak memory
# =====================================================================
if __name__ == "__main__":
    tests: list[list[int]] = [
        [1, 3, 4, 2, 2],                 # official example 1 → 2
        [3, 1, 3, 4, 2],                 # official example 2 → 3
        [3, 3, 3, 3, 3],                 # all duplicates → 3
    ]
    expected = [2, 3, 3]

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok1 = all(Solution_Floyd().findDuplicate(t) == e for t, e in zip(tests, expected))
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok2 = all(Solution_HashSet().findDuplicate(t) == e for t, e in zip(tests, expected))
    t1b = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("0287 Find the Duplicate Number")
    print(f"Approach 1 (Floyd)    : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (hash set) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches found the duplicate on all 3 tests."
          if ok1 and ok2 else "FAIL : at least one test returned the wrong value.")
