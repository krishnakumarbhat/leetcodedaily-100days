"""
=====================================================================
LeetCode 0033 : Search in Rotated Sorted Array                   (Medium)
https://leetcode.com/problems/search-in-rotated-sorted-array/
Category   : Binary Search
---------------------------------------------------------------------
PROBLEM
    A sorted array is rotated at an unknown pivot (e.g. [0,1,2,4,5,6,7]
    becomes [4,5,6,7,0,1,2]). Given the rotated array and a `target`,
    return its index or -1. All values are UNIQUE. Must run in O(log n).

---------------------------------------------------------------------
INTUITION
    One rotation = two ascending runs glued together. In ANY window
    [lo, hi] at least ONE side of mid is fully sorted — that side is
    a normal binary-search sub-problem. Decide which side the target
    belongs to; halving still works, so O(log n) survives the rotation.

---------------------------------------------------------------------
APPROACH 1 — Direct BS: find the sorted half, decide, discard
    Invariant: target, if present, is in [lo, hi]. Per iteration:
      1. mid = lo + (hi-lo)//2; hit → return.
      2. If nums[lo] <= nums[mid], the LEFT half is sorted:
           target in [nums[lo], nums[mid]) → hi = mid-1, else lo = mid+1.
      3. Else the RIGHT half is sorted:
           target in (nums[mid], nums[hi]] → lo = mid+1, else hi = mid-1.
    The `<=` in step 2 is the off-by-one: with a 2-element window
    [x, y], mid == lo and the left half [x] IS sorted — test it.
    Time  Complexity : O(log n)   Space Complexity : O(1)

---------------------------------------------------------------------
APPROACH 2 — Find the pivot, then plain BS in the right segment
    The pivot is the minimum element — the only place the array drops.
    Locate it with the 0153 trick: while nums[mid] > nums[hi] the
    pivot is to the right (lo = mid+1), else hi = mid. After the loop
    lo IS the pivot. Compare target with nums[0] to pick the segment,
    then run plain 704-style BS inside it.
    Time  Complexity : O(log n)   Space Complexity : O(1)

---------------------------------------------------------------------
DEEP DIVE — the predicate invariant in a rotated world
    Plain BS works because P(x) = "x < target" is monotone. Rotation
    BREAKS that monotonicity at the pivot: Approach 1 repairs it
    locally (each iteration restores a monotone predicate on the
    sorted half); Approach 2 repairs it globally (find the pivot —
    the single transition of the circular predicate "nums[i] >
    nums[i+1]" — rotate the index space back, then 0704 applies).
    The same "find the predicate flip, then search the restored
    domain" pattern powers 0153 (minimum) and 0875 (feasible speed).
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Optional

# =====================================================================
# APPROACH 1 : Direct binary search on the sorted half
# =====================================================================
class Solution_SortedHalf:
    """
    Purpose : Return the index of `target` in a rotated sorted array.
    Inputs  : nums   — rotated sorted List[int] (unique values).
              target — integer value being searched for.
    Output  : int index of target, or -1 when absent.
    """

    def search(self, nums: List[int], target: int) -> int:
        # Invariant: target, if present, lies inside [lo, hi].
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            # Overflow-safe midpoint of the inclusive window.
            mid = lo + (hi - lo) // 2

            if nums[mid] == target:
                return mid                # probe hit — done.

            if nums[lo] <= nums[mid]:
                # LEFT half [lo..mid] is sorted (<= handles the
                # 2-element window where mid == lo).
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1          # target lives in sorted left.
                else:
                    lo = mid + 1          # not there → right half.
            else:
                # RIGHT half [mid..hi] is sorted.
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1          # target lives in sorted right.
                else:
                    hi = mid - 1          # not there → left half.

        return -1                         # window inverted → absent.

# =====================================================================
# APPROACH 2 : Find pivot (0153 trick), then plain BS in one segment
# =====================================================================
class Solution_PivotThenSearch:
    """
    Purpose : Return the index of `target` in a rotated sorted array.
    Inputs  : nums   — rotated sorted List[int] (unique values).
              target — integer value being searched for.
    Output  : int index of target, or -1 when absent.
    """

    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)

        # --- Phase 1: locate the pivot (the minimum element) ---
        # Predicate "nums[mid] > nums[n-1]" is true on the left run,
        # false on the right run → shrink toward the single transition.
        lo, hi = 0, n - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1              # pivot is to the right.
            else:
                hi = mid                  # mid may BE the pivot.
        pivot = lo                        # index of the minimum.

        # --- Phase 2: pick the segment, then plain binary search ---
        # Segments: [0, pivot) and [pivot, n). nums[0] decides which
        # one can hold target.
        lo = 0 if target >= nums[0] else pivot
        hi = pivot - 1 if target >= nums[0] else n - 1

        while lo <= hi:                   # ordinary 704 loop.
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

        return -1                         # absent from both segments.


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test cases: target in the left run, in the right run, and absent.
    tests = [
        ([4, 5, 6, 7, 0, 1, 2], 0),   # expect index 4
        ([4, 5, 6, 7, 0, 1, 2], 6),   # expect index 2
        ([4, 5, 6, 7, 0, 1, 2], 3)    # absent — expect -1
    ]

    all_ok = True
    for t_idx, (nums, target) in enumerate(tests):
        # Ground truth: linear scan (the O(n) referee).
        expect = next((i for i, v in enumerate(nums) if v == target), -1)

        # --- Approach 1: time + tracemalloc peak ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = Solution_SortedHalf().search(nums, target)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + tracemalloc peak ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = Solution_PivotThenSearch().search(nums, target)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == expect and r2 == expect
        all_ok = all_ok and ok
        print(f"Test {t_idx+1}: target {target} | A1 sorted-half = {r1} "
              f"({(t1-t0)*1e6:.2f} µs, {peak1} B) | A2 pivot+BS = {r2} "
              f"({(t1b-t0b)*1e6:.2f} µs, {peak2} B) | {'PASS' if ok else 'FAIL'}")

    print("PASS : both approaches agree with ground truth on all tests."
          if all_ok else "FAIL : at least one answer is wrong.")