"""
=====================================================================
LeetCode 48 : Rotate Image                                     (Medium)
https://leetcode.com/problems/rotate-image/
Category   : Math & Geometry
---------------------------------------------------------------------
PROBLEM
    Rotate an n×n matrix 90 degrees CLOCKWISE, in place, using O(1)
    extra memory. Every cell (r, c) must end up at (c, n-1-r).
---------------------------------------------------------------------
INTUITION
    A clockwise 90° rotation is two cheap in-place steps: TRANSPOSE
    (mirror across the main diagonal) followed by REVERSING each row.
    Transpose maps (r,c)→(c,r); row-reverse maps (r,c)→(r,n-1-c).
    Composed: (r,c)→(c,r)→(c,n-1-r) — exactly the 90° rule.
---------------------------------------------------------------------
APPROACH 1 — Transpose + reverse (BEST)
    Step 1: swap (r, c) with (c, r) for r < c only (each pair once).
    Step 2: reverse every row.
    Time  Complexity : O(n²)   Space Complexity : O(1)
    WHY it works: the composition F·T is literally the rotation
    matrix — no angles, no trigonometry, just index arithmetic.
---------------------------------------------------------------------
APPROACH 2 — In-place 4-way ring swaps (single pass)
    Peel the matrix ring by ring. On each ring, each top-edge cell
    (i, j) has a 4-cell orbit:
        (r,c) → (c,n-1-r) → (n-1-r,n-1-c) → (n-1-c,r) → back
    Rotate those 4 partners with one temp variable.
    Time  Complexity : O(n²)   Space Complexity : O(1)
---------------------------------------------------------------------
REAL LIFE
    • Image libraries (PIL, OpenCV) rotate bitmaps by composing
      transposes and flips — the GPU has hardware for both.
    • Matrix layout transforms in linear algebra (row-major ↔
      column-major conversion) are transposes in disguise.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc

from typing import List


# =====================================================================
# APPROACH 1 : Transpose, then reverse every row
# =====================================================================
class SolutionOne:
    """
    Purpose : Rotate an n×n matrix 90° clockwise, in place.
    Inputs  : matrix — n×n list of lists of int, modified in place.
    Output  : None (the input matrix is rotated in place).
    """

    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)

        # STEP 1 — transpose: mirror across the main diagonal.
        # Visit only r < c so each cell pair is swapped exactly once.
        for r in range(n):
            for c in range(r + 1, n):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]

        # STEP 2 — reverse every row (the in-place flip trick).
        for r in range(n):
            lo, hi = 0, n - 1
            while lo < hi:
                matrix[r][lo], matrix[r][hi] = matrix[r][hi], matrix[r][lo]
                lo += 1
                hi -= 1


# =====================================================================
# APPROACH 2 : In-place 4-way ring swaps (single pass)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Rotate an n×n matrix 90° clockwise via ring cycles.
    Inputs  : matrix — n×n list of lists of int, modified in place.
    Output  : None (the input matrix is rotated in place).
    """

    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)

        # Peel ring by ring; ring i spans rows/cols i .. n-1-i.
        for i in range(n // 2):
            last = n - 1 - i
            # j walks along the TOP edge; every cell rotates in an
            # orbit of exactly 4 partners.
            for j in range(i, last):
                offset = j - i            # distance along the edge

                # Save top, then cycle left → top, bottom → left,
                # right → bottom, saved top → right.
                top = matrix[i][j]
                matrix[i][j] = matrix[last - offset][i]
                matrix[last - offset][i] = matrix[last][last - offset]
                matrix[last][last - offset] = matrix[j][last]
                matrix[j][last] = top


# =====================================================================
# BENCHMARK — both approaches on 3 matrices; time + peak memory (KB)
# =====================================================================
if __name__ == "__main__":
    tests = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
        [[1]],
    ]
    expected = [
        [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
        [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]],
        [[1]],
    ]

    def run(label: str, solve) -> bool:
        """
        Purpose : Run one solution class over every test and print a row.
        Inputs  : label — display name of the approach.
                  solve — callable(matrix) rotating it in place.
        Output  : bool — True when every test passed.
        """
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = True
        for i, (mat, want) in enumerate(zip(tests, expected)):
            m = [row[:] for row in mat]     # fresh deep copy per run
            solve(m)
            pass_ = m == want
            ok = ok and pass_
            print(f"  test {i + 1} (n={len(m)}): {m}  {'PASS' if pass_ else 'FAIL'}")
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{label} : {'PASS' if ok else 'FAIL'}  time = {(t1 - t0) * 1e6:.1f} us  peak-mem = {peak // 1024} KB")
        return ok

    ok1 = run("Approach 1 (transpose + reverse)   ", lambda m: SolutionOne().rotate(m))
    ok2 = run("Approach 2 (4-way ring swaps)      ", lambda m: SolutionTwo().rotate(m))

    print("PASS : both approaches produce the exact 90° rotation on all tests."
          if ok1 and ok2
          else "FAIL : at least one test failed.")
