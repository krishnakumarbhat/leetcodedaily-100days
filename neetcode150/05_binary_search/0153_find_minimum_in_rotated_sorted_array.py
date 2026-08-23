"""
=====================================================================
LeetCode 0153 : Find Minimum in Rotated Sorted Array              (Medium)
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
Category   : Binary Search
---------------------------------------------------------------------
PROBLEM
    A sorted array is rotated at an unknown pivot (e.g. [0,1,2,4,5,6,7]
    becomes [4,5,6,7,0,1,2]). All values are UNIQUE. Find the minimum
    element in O(log n).

---------------------------------------------------------------------
INTUITION
    The minimum is the PIVOT — the only element smaller than the one
    before it (the drop point). "Is nums[mid] <= nums[n-1]?" is a
    monotone predicate: FALSE on the left run, TRUE on the right run.
    Binary search finds the first TRUE index — which IS the minimum.

---------------------------------------------------------------------
APPROACH 1 — Binary search: compare mid against the RIGHT edge
    Invariant: the minimum is inside [lo, hi]. Per iteration:
      • nums[mid] > nums[hi] → the drop is strictly to the right of
        mid → lo = mid + 1.
      • nums[mid] <= nums[hi] → mid lies on the right run; the
        minimum is mid or to its left → hi = mid.
    Loop is `lo < hi` because hi = mid keeps the window size >= 1;
    after the loop lo == hi == the pivot.
    Time  Complexity : O(log n)   Space Complexity : O(1)

---------------------------------------------------------------------
APPROACH 2 — Sort, then take the first (cheating contrast)
    Sort a copy and read the front. Correct, trivial, O(n log n) —
    a reminder of WHY the binary-search version matters: at n = 1e6
    the BS does ~20 probes; sorting touches millions of elements.
    Time  Complexity : O(n log n)   Space Complexity : O(n)

---------------------------------------------------------------------
DEEP DIVE — the false→true predicate that makes this work
    Define P(k) = "nums[k] <= nums[n-1]" over the whole array. On the
    left run all values are BIGGER than nums[n-1] → P false; on the
    right run values are <= nums[n-1] → P true. P is monotone:
    false…false TRUE…TRUE, and the FIRST true index is the minimum.
    This is the 0704 invariant in disguise: keep [lo, hi] around the
    false→true boundary, exactly like std::lower_bound finds the
    first element >= key. The same predicate trick powers 0033
    (pivot + segment search) and 0875 (feasible eating speed).
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Binary search on the "mid vs right edge" predicate
# =====================================================================
class Solution_BinarySearch:
    """
    Purpose : Return the minimum of a rotated sorted array.
    Inputs  : nums — rotated sorted List[int] with unique values.
    Output  : int minimum element (the pivot).
    """

    def findMin(self, nums: List[int]) -> int:
        # Invariant: the minimum lives inside [lo, hi].
        lo, hi = 0, len(nums) - 1

        # `lo < hi` (not <=): hi = mid keeps the window from emptying;
        # the loop terminates with lo == hi == pivot.
        while lo < hi:
            mid = lo + (hi - lo) // 2      # overflow-safe midpoint.

            if nums[mid] > nums[hi]:
                # mid sits on the LEFT run (bigger than the right
                # edge) → the drop must be strictly to the right.
                lo = mid + 1
            else:
                # mid sits on the RIGHT run → the minimum is mid or
                # to its left; keep mid in scope (hi = mid).
                hi = mid

        return nums[lo]                    # lo == hi == pivot index.

# =====================================================================
# APPROACH 2 : Sort a copy and take the first element (contrast)
# =====================================================================
class Solution_SortFirst:
    """
    Purpose : Return the minimum of a rotated sorted array.
    Inputs  : nums — rotated sorted List[int] with unique values.
    Output  : int minimum element.
    """

    def findMin(self, nums: List[int]) -> int:
        # Sorting destroys the rotation information entirely.
        sorted_copy = sorted(nums)

        # The minimum of a sorted array is its first element.
        return sorted_copy[0]


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test cases: classic rotation, full-circle (unrotated), 1 element.
    tests = [
        [4, 5, 6, 7, 0, 1, 2],      # expect 0 at index 4
        [11, 13, 15, 17],           # expect 11 (no rotation)
        [3]                         # single element — expect 3
    ]

    all_ok = True
    for t_idx, nums in enumerate(tests):
        expect = min(nums)                 # ground truth: linear min().

        # --- Approach 1: time + tracemalloc peak ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = Solution_BinarySearch().findMin(nums)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + tracemalloc peak ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = Solution_SortFirst().findMin(nums)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == expect and r2 == expect
        all_ok = all_ok and ok
        print(f"Test {t_idx+1}: size {len(nums)} | A1 binary search = {r1} "
              f"({(t1-t0)*1e6:.2f} µs, {peak1} B) | A2 sort-first = {r2} "
              f"({(t1b-t0b)*1e6:.2f} µs, {peak2} B) | expect {expect} "
              f"| {'PASS' if ok else 'FAIL'}")

    print("PASS : both approaches agree with ground truth on all tests."
          if all_ok else "FAIL : at least one answer is wrong.")