"""
=====================================================================
LeetCode 0004 : Median of Two Sorted Arrays                        (Hard)
https://leetcode.com/problems/median-of-two-sorted-arrays/
Category   : Binary Search
---------------------------------------------------------------------
PROBLEM
    Given two sorted arrays `nums1` and `nums2` of sizes m and n,
    return the median of the two merged arrays. Must run in
    O(log(m + n)) — that constraint forces binary search.

---------------------------------------------------------------------
INTUITION
    Median = the value that splits the combined data so the LEFT half
    and RIGHT half hold the same number of elements. Instead of
    merging (O(m+n)), ask: "where does the cut go in the SMALLER
    array?" — the cut in the other array is then FORCED by the
    half-count equation. Each probe validates the cut or discards
    half of the remaining positions.

---------------------------------------------------------------------
APPROACH 1 — Merge, then pick the middle (baseline, O(m+n))
    Walk both arrays with two pointers, always appending the smaller
    head — the merge step of merge sort. Then:
      • odd total  → the middle element.
      • even total → average of the two middle elements.
    Correct and simple; too slow for the O(log(m+n)) requirement but
    a perfect ground-truth referee.
    Time  Complexity : O(m+n)   Space Complexity : O(m+n)

---------------------------------------------------------------------
APPROACH 2 — Binary search on the partition (BEST, O(log min(m,n)))
    Let A be the SMALLER array (minimizes probes). The median cut is:
    i elements from A's left, j = (m+n+1)//2 - i from B's left.
    Probe i with binary search; the cut is valid when
    A[i-1] <= B[j] AND B[j-1] <= A[i]. If A[i-1] > B[j] the cut is
    too far right in A → search left; otherwise search right. When
    balanced, read the median off the boundary elements.
    Time  Complexity : O(log(min(m, n)))   Space Complexity : O(1)

---------------------------------------------------------------------
DEEP DIVE — why i + j = (m+n+1)//2 and where the +1 comes from
    The cut divides combined data into left (i + j elements) and
    right (m+n-i-j). For the median we need i + j = ⌈(m+n)/2⌉, and
    (m+n+1)//2 IS that ceiling in integer arithmetic — the +1 makes
    ODD totals put the extra element on the left, so the median is
    max(left side); even totals average the two middle boundaries.
    i and j are COUNTS of elements on the left (while A[i] and B[j]
    are VALUES, 0-based) — so j is derived, not probed:
    j = (m+n+1)//2 - i falls out of the count equation. Edge cuts (i=0 or i=m) use ∓∞
    sentinels so the comparisons stay well-defined. The +1 is THE
    classic off-by-one of this problem — get the half equation right
    and the whole solution falls out.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Merge with two pointers, then read the middle
# =====================================================================
class Solution_Merge:
    """
    Purpose : Return the median of two sorted arrays by merging.
    Inputs  : nums1, nums2 — sorted Lists of ints.
    Output  : float median of the combined data.
    """

    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged: List[int] = []
        i, j = 0, 0

        # Two-pointer merge: always append the smaller current head.
        while i < len(nums1) and j < len(nums2):
            if nums1[i] <= nums2[j]:
                merged.append(nums1[i])       # take from nums1.
                i += 1
            else:
                merged.append(nums2[j])       # take from nums2.
                j += 1

        # Drain whichever array still has leftovers (already sorted).
        merged.extend(nums1[i:])
        merged.extend(nums2[j:])

        # Median: middle element (odd) or mean of two middles (even).
        n = len(merged)
        if n % 2 == 1:
            return float(merged[n // 2])
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0

# =====================================================================
# APPROACH 2 : Binary search the partition in the SMALLER array
# =====================================================================
class Solution_BS_Partition:
    """
    Purpose : Return the median of two sorted arrays in O(log min).
    Inputs  : nums1, nums2 — sorted Lists of ints.
    Output  : float median of the combined data.
    """

    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # A = smaller array → binary search domain of size min(m, n).
        A, B = (nums1, nums2) if len(nums1) <= len(nums2) else (nums2, nums1)

        total = len(A) + len(B)
        # THE invariant: the left half must hold ⌈total/2⌉ elements.
        # (total+1)//2 is that ceiling in integer arithmetic — the +1
        # pushes the extra middle element LEFT for odd totals.
        left_count = (total + 1) // 2

        # i = number of A-elements left of the cut; window [0, len(A)]
        # because the cut may sit at either edge of A.
        lo, hi = 0, len(A)
        while lo <= hi:
            i = lo + (hi - lo) // 2       # probe the cut in A.
            # j is FORCED by the invariant: i + j = left_count, so the
            # two left halves together always hold ⌈total/2⌉ elements.
            j = left_count - i

            # Boundary values with ∓∞ sentinels for edge cuts.
            a_left  = A[i - 1] if i >= 1 else float("-inf")
            a_right = A[i] if i < len(A) else float("inf")
            b_left  = B[j - 1] if j >= 1 else float("-inf")
            b_right = B[j] if j < len(B) else float("inf")

            if a_left <= b_right and b_left <= a_right:
                # Cut is BALANCED: every left element ≤ every right one.
                if total % 2 == 1:
                    return max(a_left, b_left)          # odd → max of left.
                return (max(a_left, b_left) + min(a_right, b_right)) / 2.0

            if a_left > b_right:
                hi = i - 1                # too many A-elements on the left.
            else:
                lo = i + 1                # too few — pull more from A.

        return 0.0                        # unreachable with valid input.


# =====================================================================
# BENCHMARK — run both approaches on 4 tests, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test cases: odd total, even total, all-zeros, and mixed sizes.
    tests = [
        ([1, 3], [2]),                 # merged [1,2,3] → 2.0
        ([1, 2], [3, 4]),              # merged [1,2,3,4] → 2.5
        ([0, 0], [0, 0]),              # merged [0,0,0,0] → 0.0
        ([1, 3, 5, 7], [2, 4, 6, 8, 10])  # merged odd → 5.0
    ]

    all_ok = True
    for t_idx, (n1, n2) in enumerate(tests):
        # Ground truth: brute-force merge + sort (the referee).
        merged = sorted(n1 + n2)
        mid = len(merged) // 2
        expect = (merged[mid] if len(merged) % 2 == 1
                  else (merged[mid - 1] + merged[mid]) / 2.0)

        # --- Approach 1: time + tracemalloc peak ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = Solution_Merge().findMedianSortedArrays(n1, n2)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + tracemalloc peak ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = Solution_BS_Partition().findMedianSortedArrays(n1, n2)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == expect and r2 == expect
        all_ok = all_ok and ok
        print(f"Test {t_idx+1}: |A|={len(n1)} |B|={len(n2)} | A1 merge = {r1} "
              f"({(t1-t0)*1e6:.2f} µs, {peak1} B) | A2 BS-partition = {r2} "
              f"({(t1b-t0b)*1e6:.2f} µs, {peak2} B) | expect {expect} "
              f"| {'PASS' if ok else 'FAIL'}")

    print("PASS : both approaches agree with ground truth on all tests."
          if all_ok else "FAIL : at least one answer is wrong.")