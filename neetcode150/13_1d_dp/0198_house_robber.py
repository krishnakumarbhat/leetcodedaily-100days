"""
=====================================================================
LeetCode 198 : House Robber                                     (Medium)
https://leetcode.com/problems/house-robber/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    Houses on a street hold cash nums[i] each. Adjacent houses share
    an alarm → you may NOT rob two neighbours. Maximise total loot.
---------------------------------------------------------------------
INTUITION
    Walk the street left→right. At house i the optimal plan is either
    "skip i" (best loot from houses 0..i-1) or "rob i" (cash[i] plus
    best loot from houses 0..i-2 — i-1 is now forbidden). The better
    of the two decisions at i becomes the answer for every later
    house → optimal substructure with overlapping subproblems.
---------------------------------------------------------------------
APPROACH 1 — Bottom-up with rolling variables (BEST)
    dp[i] = max loot from houses 0..i.
    Recurrence : dp[i] = max(dp[i-1], nums[i] + dp[i-2])
                 dp[0] = nums[0], dp[1] = max(nums[0], nums[1])
    State space : i ∈ [0, n) → n states on array dp[n]; cell i reads
                  only i-1 and i-2 → collapse to two rolling variables
                  (prev2, prev1) → O(1) space.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Top-down memoized recursion
    f(i) = max loot from houses 0..i; same recurrence, solved on
    demand and cached in memo[i].
    Trade-off : readability and natural derivation; costs recursion
    depth n and memo lookup per state.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Job / task scheduling with exclusion constraints (no two
      adjacent time slots), resource harvesting on a timeline.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : bottom-up with two rolling variables
# =====================================================================
class SolutionOne:
    """
    Purpose : Maximise loot without robbing adjacent houses.
    Inputs  : nums — cash in each house.
    Output  : int — maximum total loot.
    """

    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0                     # empty street → nothing to take
        if len(nums) == 1:
            return nums[0]               # single house → take it
        # Rolling window: prev2 = dp[i-2], prev1 = dp[i-1].
        prev2, prev1 = nums[0], max(nums[0], nums[1])
        for i in range(2, len(nums)):
            cur = max(prev1, nums[i] + prev2)  # skip i vs rob i
            prev2, prev1 = prev1, cur          # slide the window right
        return prev1  # dp[n-1]


# =====================================================================
# APPROACH 2 : top-down memoized recursion
# =====================================================================
class SolutionTwo:
    """
    Purpose : Maximise loot without robbing adjacent houses (memoized).
    Inputs  : nums — cash in each house.
    Output  : int — maximum total loot.
    """

    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        memo: List[int] = [-1] * n  # -1 = house range not solved yet

        def f(i: int) -> int:
            if i < 0:
                return 0                 # no houses left → no loot
            if memo[i] != -1:
                return memo[i]           # overlapping subproblem → reuse
            # skip i  vs  rob i + best from i-2 (i-1 is forbidden).
            memo[i] = max(f(i - 1), nums[i] + f(i - 2))
            return memo[i]

        return f(n - 1)


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (nums, expected loot). Both solutions must match.
    tests: List[Tuple[List[int], int]] = [
        ([1, 2, 3, 1], 4),      # rob 1 + 3
        ([2, 7, 9, 3, 1], 12),  # rob 2 + 9 + 1
        ([2, 1, 1, 2], 4),      # rob 2 + 2 (ends — NOT adjacent)
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
        print(f"nums={str(nums):22} A1={r1:3} A2={r2:3} expected={expected:3} "
              f"{'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches match every expected output."
          if all_pass
          else "FAIL : at least one answer is wrong.")