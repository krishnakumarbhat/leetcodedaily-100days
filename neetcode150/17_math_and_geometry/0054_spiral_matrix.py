"""
=====================================================================
LeetCode 54 : Spiral Matrix                                   (Medium)
https://leetcode.com/problems/spiral-matrix/
Category   : Math & Geometry
---------------------------------------------------------------------
PROBLEM
    Given an m×n matrix, return every element in SPIRAL order:
    right along the top edge, down the right edge, left along the
    bottom, up the left edge — shrinking inward until every cell
    has been visited exactly once.
---------------------------------------------------------------------
INTUITION
    A spiral is repeated BOUNDARY PEELING: walk one full loop around
    the outer rectangle (top → right → bottom → left), then shrink
    the rectangle by one cell on every side and repeat. When the top
    boundary passes the bottom (or left passes right) we are done.
---------------------------------------------------------------------
APPROACH 1 — Boundary shrinking with 4 pointers (BEST)
    Track top, bottom, left, right. Sweep each of the four edges of
    the current layer in turn, shrinking its bound after the sweep.
    Two guards (top <= bottom / left <= right) keep single-row and
    single-column layers from being double-visited.
    Time  Complexity : O(m·n)   Space Complexity : O(1) extra
    (the answer list of m·n values is the required output itself).
---------------------------------------------------------------------
APPROACH 2 — Layer-by-layer recursive peeling
    Same spiral as a recursion: peel the outer layer, recurse on the
    inner (m-2)×(n-2) rectangle. Same O(m·n) work; the recursion
    stack costs O(min(m, n)/2) memory instead of O(1).
    Time  Complexity : O(m·n)   Space Complexity : O(min(m, n)/2)
---------------------------------------------------------------------
REAL LIFE
    • Raster-to-vector scanners and image steganography read pixels
      in spiral order; printers (e.g. test pages) trace spirals.
    • Sparse matrix iterators and proximity searches (k-d tree
      neighbor rings) peel rings in this exact pattern.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc

from typing import List


# =====================================================================
# APPROACH 1 : Boundary shrinking with 4 pointers
# =====================================================================
class SolutionOne:
    """
    Purpose : Return all matrix elements in spiral order.
    Inputs  : matrix — m×n list of lists of int.
    Output  : List[int] with elements in spiral order.
    """

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        out: List[int] = []

        # The four shrinking boundaries of the current layer.
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        # Keep peeling layers until the rectangle collapses.
        while top <= bottom and left <= right:

            # 1) top row, left → right.
            for c in range(left, right + 1):
                out.append(matrix[top][c])
            top += 1                    # top edge consumed → shrink

            # 2) right column, top → bottom.
            for r in range(top, bottom + 1):
                out.append(matrix[r][right])
            right -= 1                  # right edge consumed → shrink

            # 3) bottom row, right → left. Guard: a single-row matrix
            #    would otherwise revisit cells swept in step 1.
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    out.append(matrix[bottom][c])
                bottom -= 1

            # 4) left column, bottom → top. Guard: single-column case.
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    out.append(matrix[r][left])
                left += 1

        return out


# =====================================================================
# APPROACH 2 : Layer-by-layer recursive peeling
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return all matrix elements in spiral order.
    Inputs  : matrix — m×n list of lists of int.
    Output  : List[int] with elements in spiral order.
    """

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        out: List[int] = []
        self._peel(matrix, 0, len(matrix) - 1, 0, len(matrix[0]) - 1, out)
        return out

    def _peel(self, matrix: List[List[int]], t: int, b: int,
              l: int, r: int, out: List[int]) -> None:
        """
        Purpose : Append one spiral layer to `out`, then recurse inward.
        Inputs  : matrix — the grid; t/b/l/r — current layer bounds;
                  out — accumulator filled in spiral order.
        Output  : None (out is appended in place).
        """
        if t > b or l > r:
            return                     # layer collapsed → done

        out.extend(matrix[t][l:r + 1])                     # top →
        out.extend(matrix[row][r] for row in range(t + 1, b + 1))  # right ↓
        if t < b:
            out.extend(matrix[b][c] for c in range(r - 1, l - 1, -1))  # bottom ←
        if l < r:
            out.extend(matrix[row][l] for row in range(b - 1, t, -1))  # left ↑

        # Recurse one layer deeper on every side.
        self._peel(matrix, t + 1, b - 1, l + 1, r - 1, out)


# =====================================================================
# BENCHMARK — both approaches on 3 matrices; time + peak memory (KB)
# =====================================================================
if __name__ == "__main__":
    tests = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
        [[1], [2], [3], [4]],
    ]
    expected = [
        [1, 2, 3, 6, 9, 8, 7, 4, 5],
        [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
        [1, 2, 3, 4],
    ]

    def run(label: str, solve) -> bool:
        """
        Purpose : Run one solution class over every test and print a row.
        Inputs  : label — display name of the approach.
                  solve — callable(matrix) -> List[int].
        Output  : bool — True when every test passed.
        """
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = True
        for i, (mat, want) in enumerate(zip(tests, expected)):
            got = solve(mat)
            pass_ = got == want
            ok = ok and pass_
            print(f"  test {i + 1} ({len(mat)}x{len(mat[0])}): {got}  {'PASS' if pass_ else 'FAIL'}")
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{label} : {'PASS' if ok else 'FAIL'}  time = {(t1 - t0) * 1e6:.1f} us  peak-mem = {peak // 1024} KB")
        return ok

    ok1 = run("Approach 1 (boundary shrinking)    ", lambda m: SolutionOne().spiralOrder(m))
    ok2 = run("Approach 2 (recursive layer peel)  ", lambda m: SolutionTwo().spiralOrder(m))

    print("PASS : both approaches produce the exact spiral order on all tests."
          if ok1 and ok2
          else "FAIL : at least one test failed.")
