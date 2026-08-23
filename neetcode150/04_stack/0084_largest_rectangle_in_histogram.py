"""
=====================================================================
LeetCode 84 : Largest Rectangle in Histogram                   (Hard)
https://leetcode.com/problems/largest-rectangle-in-histogram/
Category   : Stack (monotonic)
---------------------------------------------------------------------
PROBLEM
    Given `heights` (bar heights of a histogram, width 1 each), return
    the area of the largest rectangle that can be drawn inside the
    histogram — every rectangle sits on the baseline and may span
    several consecutive bars, bounded by the shortest bar inside it.
---------------------------------------------------------------------
INTUITION
    Every maximal rectangle is "anchored" by one bar h: it extends
    left and right exactly until it meets a bar SHORTER than h. If we
    knew, for every bar, the nearest shorter bar on each side, the
    answer would be max over i of heights[i] × (right[i] − left[i] − 1).
    A MONOTONIC STACK finds both bounds in one pass: while heights
    ascend we cannot know the right bound; the moment a shorter bar
    appears, every taller bar above it gets its right bound resolved.
---------------------------------------------------------------------
APPROACH 1 — Monotonic increasing stack (BEST)
    Invariant: stack indices hold STRICTLY INCREASING heights. For
    each new bar h: pop every index whose height is > h. Each popped
    bar p has h as its first-shorter bar to the RIGHT; the new stack
    top is the first-shorter bar to its LEFT → width resolved, area
    computed once, never again. A sentinel 0 at the end forces every
    bar to be popped exactly once.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Brute force (contrast)
    For every pair (i, j) of bars, the best rectangle spanning them
    has height min(heights[i..j]); take the max over all pairs.
    Correct but quadratic — no structure used.
    Time  Complexity : O(n²)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — the monotonic stack invariant
    A monotonic stack keeps its elements in sorted order — ascending
    here. It is the canonical tool for "nearest smaller/greater
    neighbour" problems (0084, 0739, 0853). The invariant is
    re-established on every push: pop WHILE the top violates order,
    then push. Each element pays O(1) amortized (one push, one pop),
    so the whole sweep is linear — the pattern's power.
---------------------------------------------------------------------
REAL LIFE
    • Skyline / floor-plan optimisation: largest empty rectangle in
      a city block or warehouse racking layout.
    • Charting libraries compute the widest "flat" highlight range;
      graphics pipelines use the same sweep for area union.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Monotonic increasing stack (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Largest rectangle area under the histogram.
    Inputs  : heights — bar heights, each bar has width 1.
    Output  : the maximum area of any axis-aligned rectangle.
    """

    def largestRectangleArea(self, heights: List[int]) -> int:
        st: List[int] = []      # indices; heights[st] strictly increasing
        best = 0

        # Sentinel height 0 appended: strictly shorter than every bar,
        # so it resolves (pops) every remaining rectangle at the end.
        h = heights + [0]

        for i, h_i in enumerate(h):
            # While the new bar is SHORTER than the stack-top bar, the
            # top bar's rectangle is complete: h[i] is its first
            # shorter neighbour on the right.
            while st and heights[st[-1]] > h_i:
                # height of the rectangle = the popped bar itself.
                height = heights[st.pop()]

                # width: right bound = i, left bound = new stack top
                # (empty stack → the bar stretched to index 0).
                width = i if not st else i - st[-1] - 1

                # Candidate area; keep the global maximum.
                best = max(best, height * width)

            # Invariant restored → this bar's own bound is unresolved,
            # so it enters the stack to be resolved by a future bar.
            st.append(i)

        return best


# =====================================================================
# APPROACH 2 : Brute force over all pairs (contrast)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Largest rectangle area under the histogram.
    Inputs  : heights — bar heights, each bar has width 1.
    Output  : the maximum area of any axis-aligned rectangle.
    """

    def largestRectangleArea(self, heights: List[int]) -> int:
        n = len(heights)
        best = 0

        # Every rectangle is determined by its left edge i and right
        # edge j; its height is the minimum bar in between.
        for i in range(n):
            min_h = heights[i]

            # Extend the right edge: width grows, height can only fall.
            for j in range(i, n):
                min_h = min(min_h, heights[j])   # shrink bound
                best = max(best, min_h * (j - i + 1))

        return best


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Correctness tests ---
    tests = [
        ([2, 1, 5, 6, 2, 3], 10),   # official example → 10
        ([2, 4], 4),                # two bars, tallest alone wins
        ([2, 1, 2], 3),             # valley forces width-2 rectangle
        ([], 0),                    # empty histogram
        ([5], 5)                    # single bar
    ]

    all_ok = True
    for heights, expect in tests:
        r1 = SolutionOne().largestRectangleArea(heights)
        r2 = SolutionTwo().largestRectangleArea(heights)
        ok = r1 == expect and r2 == expect
        if not ok:
            all_ok = False
        print(f"{'PASS' if ok else 'FAIL'} : histogram size {len(heights)}"
              f"  monotonic={r1}  brute={r2}  expect={expect}")

    # --- Benchmark: worst-case monotonic ramp forces max pops ---
    # (8k bars: brute force is O(n²) in pure Python — keep it modest)
    big = [1000000 - i for i in range(8000)]

    tracemalloc.start()
    t0 = time.perf_counter()
    rb1 = SolutionOne().largestRectangleArea(big)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t0b = time.perf_counter()
    rb2 = SolutionTwo().largestRectangleArea(big)
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (monotonic stack) : {rb1}  time = {(t1 - t0) * 1e6:.2f} µs"
          f"  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (brute force)     : {rb2}  time = {(t1b - t0b) * 1e6:.2f} µs"
          f"  peak-mem = {peak_2} bytes")

    print("PASS : all tests" if all_ok else "FAIL : a test was wrong")