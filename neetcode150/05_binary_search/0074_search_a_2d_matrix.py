"""
=====================================================================
LeetCode 0074 : Search a 2D Matrix                                (Medium)
https://leetcode.com/problems/search-a-2d-matrix/
Category   : Binary Search
---------------------------------------------------------------------
PROBLEM
    Given an m x n matrix where each row is sorted ASCENDING and the
    first value of every row is greater than the last value of the
    previous row (rows are "chained"), search for `target`. Return
    true if found, false otherwise. Must run in O(log(m·n)).

---------------------------------------------------------------------
INTUITION
    Because rows are chained (row[i][0] > row[i-1][n-1]), reading the
    matrix row-by-row yields ONE fully sorted array of m·n elements.
    A single binary search over that virtual array is the whole
    solution; the only trick is mapping the flat index
    mid -> (mid // n, mid % n). It is 0704 with a coordinate lookup.

---------------------------------------------------------------------
APPROACH 1 — Flattened-index binary search (BEST, O(log(m·n)))
    Binary search over [0, m*n). For each probe `mid`, the matrix
    coordinates are row = mid // n, col = mid % n — pure integer
    arithmetic, no copy of the matrix. Compare, then discard half of
    the flattened array exactly like 0704.
    Time  Complexity : O(log(m·n))   Space Complexity : O(1)

---------------------------------------------------------------------
APPROACH 2 — Two-level binary search (O(log m + log n))
    Phase 1: binary search the FIRST COLUMN to find the unique row
    that could hold target (last row with first-value <= target).
    Phase 2: plain 0704 binary search inside that row. Conceptually
    cleaner (two 1D searches), one extra boundary check; log m + log n
    steps vs log(m·n) — asymptotically identical.
    Time  Complexity : O(log m + log n)   Space Complexity : O(1)

---------------------------------------------------------------------
DEEP DIVE — the flat-index invariant
    A m·n matrix is "row-major": virtual index k maps to (k//n, k%n),
    and the chained-rows property makes virtual[k] strictly sorted.
    So the 0704 invariant ("answer in [lo, hi]") transfers verbatim —
    the probe just becomes matrix[k//n][k%n]. The "pretend this
    structure is a flat array" trick generalizes to segment trees,
    sparse tables, and SQL row-wise storage. Approach 2's phase 1 is
    the false→true predicate again: "matrix[r][0] <= target" is false
    then true down column 0.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Single binary search over the flattened index space
# =====================================================================
class Solution_FlattenedBS:
    """
    Purpose : Decide whether `target` exists in the sorted matrix.
    Inputs  : matrix — m x n sorted-and-chained rows of ints.
              target — integer being searched for.
    Output  : bool true if found, false otherwise.
    """

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])

        # Virtual array size = m*n; invariant: target lives in [lo,hi].
        lo, hi = 0, m * n - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2      # probe in the FLAT array.

            # Map flat index → 2D coordinates (row-major order).
            r, c = divmod(mid, n)          # r = mid // n, c = mid % n.
            v = matrix[r][c]               # virtual[mid] = matrix[r][c].

            if v == target:
                return True                # exact hit.
            if v < target:
                lo = mid + 1               # discard left half.
            else:
                hi = mid - 1               # discard right half.

        return False                       # window inverted → absent.

# =====================================================================
# APPROACH 2 : Find the row (first column), then search within it
# =====================================================================
class Solution_TwoLevelBS:
    """
    Purpose : Decide whether `target` exists in the sorted matrix.
    Inputs  : matrix — m x n sorted-and-chained rows of ints.
              target — integer being searched for.
    Output  : bool true if found, false otherwise.
    """

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])

        # --- Phase 1: binary search column 0 for the candidate row ---
        # Predicate "matrix[r][0] <= target" is false→true down the
        # column; we want the LAST true row.
        lo, hi = 0, m - 1
        row = 0
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if matrix[mid][0] <= target:
                row = mid                  # feasible row — keep going down.
                lo = mid + 1
            else:
                hi = mid - 1               # first value too big — go up.

        # --- Phase 2: plain 0704 binary search inside that row ---
        lo, hi = 0, n - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            v = matrix[row][mid]
            if v == target:
                return True
            if v < target:
                lo = mid + 1
            else:
                hi = mid - 1

        return False                       # not in the candidate row.


# =====================================================================
# BENCHMARK — run both approaches on 4 targets, time + peak memory
# =====================================================================
if __name__ == "__main__":
    matrix = [
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60]
    ]
    targets = [3, 13, 60, 1]               # hit, miss, edge hit, corner.

    all_ok = True
    for t_idx, target in enumerate(targets):
        # Ground truth: flatten + membership test (the referee).
        expect = target in [v for row in matrix for v in row]

        # --- Approach 1: time + tracemalloc peak ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = Solution_FlattenedBS().searchMatrix(matrix, target)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + tracemalloc peak ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = Solution_TwoLevelBS().searchMatrix(matrix, target)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == expect and r2 == expect
        all_ok = all_ok and ok
        print(f"Test {t_idx+1}: target {target} | A1 flattened = {r1} "
              f"({(t1-t0)*1e6:.2f} µs, {peak1} B) | A2 two-level = {r2} "
              f"({(t1b-t0b)*1e6:.2f} µs, {peak2} B) | expect {expect} "
              f"| {'PASS' if ok else 'FAIL'}")

    print("PASS : both approaches agree with ground truth on all tests."
          if all_ok else "FAIL : at least one answer is wrong.")