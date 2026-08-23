"""
=====================================================================
LeetCode 213 : House Robber II                                  (Medium)
https://leetcode.com/problems/house-robber-ii/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    Same as 0198, but the houses form a CIRCLE: house 0 and house n-1
    are adjacent, so robbing both is forbidden.
---------------------------------------------------------------------
INTUITION
    The only NEW constraint is the pair (0, n-1). A feasible plan can
    never contain both, so the optimum is the better of:
        • rob houses 0..n-2 (exclude the last)   → linear problem
        • rob houses 1..n-1 (exclude the first)  → linear problem
    Both cases are the plain 0198 recurrence on a LINE → decompose the
    circle into two lines and reuse the linear solver.
---------------------------------------------------------------------
APPROACH 1 — Two linear passes, rolling variables (BEST)
    ans = max( robLine(nums[0..n-2]), robLine(nums[1..n-1]) )
    robLine uses the 0198 recurrence with rolling variables.
    State space : two independent 1D runs, each O(n) states → O(1)
                  rolling space per run.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Two passes with FULL dp tables (contrast)
    Identical split, but each run materialises the full dp[] array so
    the recurrence→array mapping is visible cell by cell.
    Trade-off : same O(n) time, O(n) space — teaches why rolling
    variables exist: dp[i] only reads i-1, i-2, so the table is
    over-allocated.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Circular scheduling problems: ring topologies (token rings,
      round-robin load balancing), circular corridors, any 0198 with
      wraparound adjacency.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : split the circle into two lines, rolling variables
# =====================================================================
class SolutionOne:
    """
    Purpose : Maximise loot on a CIRCLE of houses (0 adjacent to n-1).
    Inputs  : nums — cash in each house.
    Output  : int — maximum total loot.
    """

    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]        # a single house: no circle to worry about

        def rob_line(start: int, end: int) -> int:
            """Linear 0198 solver over nums[start:end] (exclusive end)."""
            prev2, prev1 = 0, 0
            for i in range(start, end):
                # cur = max(skip i, rob i + loot from i-2).
                cur = max(prev1, nums[i] + prev2)
                prev2, prev1 = prev1, cur
            return prev1

        # Case A: rob houses 0..n-2 (drop the last) — first is allowed.
        # Case B: rob houses 1..n-1 (drop the first) — last is allowed.
        return max(rob_line(0, n - 1), rob_line(1, n))


# =====================================================================
# APPROACH 2 : same split, but with explicit full dp tables
# =====================================================================
class SolutionTwo:
    """
    Purpose : Maximise loot on a CIRCLE (full-table variant).
    Inputs  : nums — cash in each house.
    Output  : int — maximum total loot.
    """

    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        def rob_table(arr: List[int]) -> int:
            """Linear solver storing the whole dp array (O(len(arr)) space)."""
            m = len(arr)
            if m == 0:
                return 0
            dp: List[int] = [0] * m
            dp[0] = arr[0]
            if m > 1:
                dp[1] = max(arr[0], arr[1])
            for i in range(2, m):
                dp[i] = max(dp[i - 1], arr[i] + dp[i - 2])
            return dp[m - 1]

        # The table version makes the two linear cases explicit.
        return max(rob_table(nums[:n - 1]), rob_table(nums[1:]))


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (nums, expected loot). Both solutions must match.
    tests: List[Tuple[List[int], int]] = [
        ([2, 3, 2], 3),     # rob 2 (first) or 2 (last) — 3 neighbours both alarms
        ([1, 2, 3, 1], 4),  # rob 1 + 3
        ([1], 1),           # single house
    ]

    total_us_1 = total_us_2 = 0.0
    total_kb_1 = total_kb_2 = 0
    all_pass = True

    for nums, expected in tests:
        # --- Approach 1: perf_counter for time, tracemalloc for RAM ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().rob(nums)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_1 += (t1 - t0) * 1e6
        total_kb_1 += peak1 // 1024

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().rob(nums)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_2 += (t1b - t0b) * 1e6
        total_kb_2 += peak2 // 1024

        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"nums={str(nums):14} A1={r1:3} A2={r2:3} expected={expected:3} "
              f"{'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches match every expected output."
          if all_pass
          else "FAIL : at least one answer is wrong.")