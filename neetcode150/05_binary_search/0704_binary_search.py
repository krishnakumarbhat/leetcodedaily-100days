"""
=====================================================================
LeetCode 704 : Binary Search                                       (Easy)
https://leetcode.com/problems/binary-search/
Category   : Binary Search
---------------------------------------------------------------------
PROBLEM
    Given a SORTED array of integers `nums` and an integer `target`,
    return the index of `target`, or -1 if it is not present.

---------------------------------------------------------------------
INTUITION
    Sorted data lets every probe discard half of the remaining window.
    One comparison with `nums[mid]` answers "left, right, or here?"
    → log2(n) probes instead of n scans.

---------------------------------------------------------------------
APPROACH 1 — Classic lo <= hi loop (find ANY hit)
    Invariant: target (if present) lives in [lo, hi]. Probe
    mid = lo + (hi-lo)//2. On a hit return immediately; otherwise
    discard the half that cannot contain target. Loop exits with
    lo > hi — the window inverted ⇒ element absent.
    Time  Complexity : O(log n)   Space Complexity : O(1)
    WHY `<=`: a single-element window [k, k] still needs one probe,
    so the loop must run while the window is non-empty.

---------------------------------------------------------------------
APPROACH 2 — lo < hi loop (lower bound, then verify)
    Half-open window [lo, hi) shrinking toward the FIRST index whose
    value >= target (this is std::lower_bound semantics):
        nums[mid] >= target → hi = mid   (mid may be the answer)
        nums[mid] <  target → lo = mid+1 (mid is definitely too small)
    Loop ends with lo == hi; one final check distinguishes an exact
    hit from "absent". This predicate pattern (false…false → true…true)
    is the invariant that generalizes to 0033, 0153, 0875, 0981.
    Time  Complexity : O(log n)   Space Complexity : O(1)

---------------------------------------------------------------------
DEEP DIVE — the invariant and the off-by-one
    Both loops maintain "the answer is inside the window"; they only
    shrink differently:
      • lo <= hi : INCLUSIVE window, each step removes mid → window can
        reach size 0 → loop must permit a final probe of size 1.
      • lo <  hi : HALF-OPEN window; hi = mid never skips mid → window
        shrinks to size ≥ 1 → loop stops with lo == hi, check after.
    Predicate view: for sorted data P(x) = "answer ≤ x" is monotone
    (false…false → true…true). BS finds the FIRST true index — exactly
    what C++ std::lower_bound (first element >= key) and
    std::upper_bound (first element > key) implement internally.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Optional

# =====================================================================
# APPROACH 1 : Classic inclusive-window binary search (lo <= hi)
# =====================================================================
class Solution_ClassicLoop:
    """
    Purpose : Return the index of `target` in sorted `nums`, else -1.
    Inputs  : nums   — sorted List[int] to search inside.
              target — integer value being searched for.
    Output  : Optional[int] index of target, or -1 when absent.
    """

    def search(self, nums: List[int], target: int) -> int:
        # lo/hi bound the inclusive window [lo, hi] that may hold target.
        lo, hi = 0, len(nums) - 1

        # `<=` keeps a size-1 window [k, k] alive for its final probe.
        while lo <= hi:
            # mid = lo + (hi-lo)//2 — never overflows, unlike (lo+hi)//2.
            mid = lo + (hi - lo) // 2

            if nums[mid] == target:
                return mid                # exact hit — done in one probe.
            if nums[mid] < target:
                lo = mid + 1              # discard left half entirely.
            else:
                hi = mid - 1              # discard right half entirely.

        # Window inverted (lo > hi) → every candidate eliminated.
        return -1

# =====================================================================
# APPROACH 2 : Half-open lower-bound loop (lo < hi) + final check
# =====================================================================
class Solution_LowerBound:
    """
    Purpose : Return the index of `target` in sorted `nums`, else -1.
    Inputs  : nums   — sorted List[int] to search inside.
              target — integer value being searched for.
    Output  : int index of target, or -1 when absent.
    """

    def search(self, nums: List[int], target: int) -> int:
        # Half-open window [lo, hi): all candidates live inside.
        lo, hi = 0, len(nums)

        # `lo < hi` + hi = mid ⇒ window never empties, mid never reprobed.
        while lo < hi:
            mid = lo + (hi - lo) // 2

            if nums[mid] >= target:
                # mid qualifies as "first >= target" — keep it in scope.
                hi = mid
            else:
                # mid is strictly too small — safe to discard it.
                lo = mid + 1

        # lo == hi == first index with nums[lo] >= target.
        # One final O(1) check distinguishes hit from miss.
        if lo < len(nums) and nums[lo] == target:
            return lo
        return -1


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test cases: hit in the middle, a miss, and a single element.
    tests = [
        ([-1, 0, 3, 5, 9, 12], 9),   # hit — expect index 4
        ([-1, 0, 3, 5, 9, 12], 2),   # miss — expect -1
        ([5], 5)                     # single element — expect 0
    ]

    all_ok = True
    for t_idx, (nums, target) in enumerate(tests):
        # Ground truth: linear scan (the O(n) referee).
        expect = next((i for i, v in enumerate(nums) if v == target), -1)

        # --- Approach 1: time + tracemalloc peak ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = Solution_ClassicLoop().search(nums, target)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + tracemalloc peak ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = Solution_LowerBound().search(nums, target)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == expect and r2 == expect
        all_ok = all_ok and ok
        print(f"Test {t_idx+1}: target {target} | A1 classic = {r1} "
              f"({(t1-t0)*1e6:.2f} µs, {peak1} B) | A2 lower_bound = {r2} "
              f"({(t1b-t0b)*1e6:.2f} µs, {peak2} B) | {'PASS' if ok else 'FAIL'}")

    print("PASS : both approaches agree with ground truth on all tests."
          if all_ok else "FAIL : at least one answer is wrong.")