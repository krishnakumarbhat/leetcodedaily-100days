"""
=====================================================================
LeetCode 42 : Trapping Rain Water                              (Hard)
https://leetcode.com/problems/trapping-rain-water/
Category   : Two Pointers
---------------------------------------------------------------------
PROBLEM
    Given an elevation map height[i] (bar width = 1), compute how
    much water it can trap after a rain. Water pools above a bar only
    when both a taller bar to its LEFT and a taller bar to its RIGHT
    exist; it cannot spill past the lower of those two.
---------------------------------------------------------------------
INTUITION
    The water sitting ON TOP of bar i is fully determined by the two
    "walls" that trap it:
        water[i] = max(0, min(maxLeft[i], maxRight[i]) - height[i])
    where maxLeft[i]  = tallest bar in [0 .. i-1]
          maxRight[i] = tallest bar in [i+1 .. n-1]
    Every algorithm for this problem is a way of computing those two
    max-arrays (or the running maxima) and summing the per-bar units.
---------------------------------------------------------------------
APPROACH 1 — Prefix/suffix max arrays (intuitive, O(n) space)
    Pass 1: leftMax[i]  = max(height[0..i])   — build left to right.
    Pass 2: rightMax[i] = max(height[i..n-1]) — build right to left.
    Pass 3: water[i] = min(leftMax[i], rightMax[i]) - height[i] ≥ 0.
    Sum the non-negative values. Three linear passes, dead simple.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Two pointers (BEST, O(1) space)
    Maintain l = 0, r = n-1 plus two running maxima: lMax (tallest
    seen on the left side) and rMax (tallest seen on the right side).
    Invariant: if lMax <= rMax, bar l's true cap equals lMax — we can
    compute water[l] RIGHT NOW and advance l. Symmetric for r. Each
    bar is finalized exactly once.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — why the pointer trick needs NO right-array
    When lMax <= rMax, bar l's right constraint can never be below
    lMax (rMax already exceeds it), and its left constraint IS lMax —
    so min(maxLeft, maxRight) = lMax deterministically. The same
    argument inverts at r. The smaller of the two running maxima is
    always "finalized" — that is the invariant that compresses the
    two O(n) arrays of Approach 1 into two O(1) integers.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

# =====================================================================
# APPROACH 1 : Prefix/suffix max arrays
# =====================================================================
class SolutionOne:
    """
    Purpose : Return total trapped water using left/right max arrays.
    Inputs  : height — elevation map; height[i] is bar height at i.
    Output  : int — total water units trapped between the bars.
    """

    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        # leftMax[i] = tallest bar at or left of i — the left wall.
        left_max: List[int] = [0] * n
        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        # rightMax[i] = tallest bar at or right of i — the right wall.
        right_max: List[int] = [0] * n
        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        # Water on bar i is capped by the LOWER of its two walls.
        # max(0, ...) guards dips where the bar itself is the tallest.
        total = 0
        for i in range(n):
            total += max(0, min(left_max[i], right_max[i]) - height[i])
        return total


# =====================================================================
# APPROACH 2 : Two pointers with running maxima (BEST)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return total trapped water in O(1) extra space.
    Inputs  : height — elevation map; height[i] is bar height at i.
    Output  : int — total water units trapped between the bars.
    """

    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0

        l, r = 0, n - 1
        l_max, r_max = 0, 0
        total = 0

        # Invariant: the pointer whose RUNNING MAX is smaller gets its
        # bar finalized — its true cap is known without any right array.
        while l < r:
            if height[l] < height[r]:
                # Right side is strictly taller → the LEFT bar is the
                # binding side. If l_max already ≥ height[l], water pools;
                # otherwise l_max rises (bar l becomes a wall itself).
                if height[l] >= l_max:
                    l_max = height[l]
                else:
                    total += l_max - height[l]
                l += 1
            else:
                # Symmetric: right bar is binding → finalize bar r.
                if height[r] >= r_max:
                    r_max = height[r]
                else:
                    total += r_max - height[r]
                r -= 1
        return total


# =====================================================================
# BENCHMARK — verify both solutions on real test cases + time/RAM
# =====================================================================
if __name__ == "__main__":
    # Case 1: official example → 6. Case 2: bowl with walls at edges.
    # Case 3: monotonic rise/fall → ZERO water (no basin anywhere).
    tests: List[Tuple[List[int], int]] = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([1, 2, 3, 4, 3, 2, 1], 0),
    ]

    # Aggregate time + peak memory across all cases, per approach.
    time_us: List[float] = [0.0, 0.0]
    peak_kb: List[float] = [0.0, 0.0]
    all_pass = True

    for t, (heights, expected) in enumerate(tests, 1):
        # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().trap(heights)
        t1 = time.perf_counter()
        _, peak_1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[0] += (t1 - t0) * 1e6
        peak_kb[0] = max(peak_kb[0], peak_1 / 1024.0)

        # --- Approach 2: same instrumentation ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().trap(heights)
        t1b = time.perf_counter()
        _, peak_2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[1] += (t1b - t0b) * 1e6
        peak_kb[1] = max(peak_kb[1], peak_2 / 1024.0)

        ok = (r1 == expected) and (r2 == expected)
        all_pass = all_pass and ok
        print(f"Test {t}: prefixSuffix={r1} twoPtr={r2} expected={expected}  {'PASS' if ok else 'FAIL'}")

    print("---")
    print(f"Approach 1 (prefix/suffix max) : {time_us[0]:.2f} µs total, peak {peak_kb[0]:.2f} KB")
    print(f"Approach 2 (two pointers)      : {time_us[1]:.2f} µs total, peak {peak_kb[1]:.2f} KB")
    print("PASS : all cases" if all_pass else "FAIL : at least one case")