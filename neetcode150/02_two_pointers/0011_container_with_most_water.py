"""
=====================================================================
LeetCode 11 : Container With Most Water                        (Medium)
https://leetcode.com/problems/container-with-most-water/
Category   : Two Pointers
---------------------------------------------------------------------
PROBLEM
    Given an array `height` where height[i] is the vertical wall at
    index i, find two walls that together with the x-axis enclose the
    LARGEST rectangle of water. Water cannot overflow the shorter wall:
        area(l, r) = min(height[l], height[r]) * (r - l)
---------------------------------------------------------------------
INTUITION
    The area is a product of TWO factors: the width (r - l) and the
    limiting height min(h[l], h[r]). At every step we must sacrifice
    the factor that costs us the least — move the SHORTER wall inward.
    The shorter wall caps the area, so keeping it guarantees we never
    improve; moving it is the only move that CAN improve the next area.
---------------------------------------------------------------------
APPROACH 1 — Brute force (baseline, O(n²))
    Try EVERY pair of walls (i, j), compute the enclosed area, keep the
    maximum. Correct but wasteful: n² pairs, most dominated by a taller
    wall elsewhere.
    Time  Complexity : O(n²)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Two pointers (BEST, O(n))
    Start l = 0, r = n-1 (maximal width). Compute the area. Then move
    ONLY the shorter of the two walls inward:
      • If h[l] <= h[r], advancing l can only make the area grow (the
        limiting height might rise) — advancing r can never beat this.
      • Else advance r.
    Both pointers meet after exactly n-1 moves → O(n) total areas.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — why moving the SHORTER wall is provably safe
    Fix l and r. If h[l] <= h[r], the best container still using l as
    its left wall has height at most h[l] and width at most (r - l),
    so it cannot beat the current area. Every r' < r yields:
        area = min(h[l], h[r']) * (r' - l) <= h[l] * (r - l)
    Hence l can be discarded forever — monotonicity turns the O(n²)
    search into a single O(n) sweep measuring only n-1 rectangles.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Brute force — every pair of walls
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the max water area over ALL pairs of walls.
    Inputs  : height — wall heights; height[i] is wall i.
    Output  : int — the largest area min(h[i],h[j]) * (j-i).
    """

    def maxArea(self, height: List[int]) -> int:
        best = 0
        # Enumerate every ordered pair (l, r) with r strictly right of l.
        for l in range(len(height)):
            for r in range(l + 1, len(height)):
                # The shorter wall decides how high the water can rise.
                area = min(height[l], height[r]) * (r - l)
                best = max(best, area)
        return best


# =====================================================================
# APPROACH 2 : Two pointers — shrink from the outside in (BEST)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the max water area using the O(n) two-pointer sweep.
    Inputs  : height — wall heights; height[i] is wall i.
    Output  : int — the largest area min(h[i],h[j]) * (j-i).
    """

    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        best = 0

        # The pointers converge; each iteration discards one candidate
        # wall, so at most n-1 areas are ever measured.
        while l < r:
            # Current width is the widest remaining; the short wall caps it.
            area = min(height[l], height[r]) * (r - l)
            best = max(best, area)

            if height[l] < height[r]:
                # Left wall is the bottleneck: ANY right-side partner with
                # this left wall fits ≤ h[l]*(r-l) — l is provably useless
                # now, drop it.
                l += 1
            else:
                # Right wall is the bottleneck (or tie) — drop it instead.
                # A tie is symmetric: moving either side cannot lose the
                # optimum since the equal wall still caps future areas.
                r -= 1
        return best


# =====================================================================
# BENCHMARK — verify both solutions on real test cases + time/RAM
# =====================================================================
if __name__ == "__main__":
    # Case 1: official example → 49. Case 2: monotonic rise → the answer
    # is the pair (0, n-1). Case 3: short walls in the middle — the
    # two-pointer must jump over the middle plateau.
    tests: List[tuple] = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 2, 3, 4, 5, 6, 7, 8], 16),
        ([4, 3, 1, 1, 1, 3, 4], 24),
    ]

    # Aggregate time + peak memory across all cases, per approach.
    time_us: List[float] = [0.0, 0.0]
    peak_kb: List[float] = [0.0, 0.0]
    all_pass = True

    for t, (heights, expected) in enumerate(tests, 1):
        # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().maxArea(heights)
        t1 = time.perf_counter()
        _, peak_1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[0] += (t1 - t0) * 1e6
        peak_kb[0] = max(peak_kb[0], peak_1 / 1024.0)

        # --- Approach 2: same instrumentation ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().maxArea(heights)
        t1b = time.perf_counter()
        _, peak_2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[1] += (t1b - t0b) * 1e6
        peak_kb[1] = max(peak_kb[1], peak_2 / 1024.0)

        ok = (r1 == expected) and (r2 == expected)
        all_pass = all_pass and ok
        print(f"Test {t}: brute={r1} twoPtr={r2} expected={expected}  {'PASS' if ok else 'FAIL'}")

    print("---")
    print(f"Approach 1 (brute force)  : {time_us[0]:.2f} µs total, peak {peak_kb[0]:.2f} KB")
    print(f"Approach 2 (two pointers) : {time_us[1]:.2f} µs total, peak {peak_kb[1]:.2f} KB")
    print("PASS : all cases" if all_pass else "FAIL : at least one case")