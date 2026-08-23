"""
=====================================================================
LeetCode 300 : Longest Increasing Subsequence                    (Medium)
https://leetcode.com/problems/longest-increasing-subsequence/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    Given an integer array `nums`, return the length of the LONGEST
    strictly-increasing SUBSEQUENCE (elements keep order, may skip).
---------------------------------------------------------------------
INTUITION
    Look at each element as the END of a subsequence. The longest
    increasing subsequence ending AT nums[i] is built by appending
    nums[i] to the best sequence ending at some EARLIER nums[j] <
    nums[i] → dp[i] = 1 + max(dp[j]). Overlapping subproblems: dp[j]
    is reused by every later i with nums[i] > nums[j].
    Greedy alternative: a sorted array `tails` where tails[k] = the
    smallest possible LAST element of an increasing subsequence of
    length k+1 — each new number either extends the longest sequence
    or improves a shorter one.
---------------------------------------------------------------------
APPROACH 1 — O(n²) DP (BEST when n ≤ 2000)
    dp[i] = length of LIS ending at index i.
    Recurrence : dp[i] = 1 + max( dp[j] for j < i and nums[j] < nums[i] )
                 base dp[i] = 1 (the element alone)
    State space : i ∈ [0, n) → n states on array dp[n]; cell i scans
                  every earlier cell j → full table required.
    Time  Complexity : O(n²)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Patience sorting + binary search (BEST for big n)
    tails array stays SORTED; for each num, find the first slot where
    tails[slot] >= num (lower bound) and replace it.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Patience sorting (the card game Solitaire) — this exact
      algorithm is the optimal play strategy.
    • Longest chain in dependency DAGs / job sequences (SIP chains),
      diff algorithms, LCS reduced to LIS.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : O(n²) classic DP
# =====================================================================
class SolutionOne:
    """
    Purpose : Length of the longest strictly increasing subsequence.
    Inputs  : nums — integer array.
    Output  : int — LIS length.
    """

    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        dp: List[int] = [1] * n  # every element alone is length-1 LIS
        best = 1
        for i in range(1, n):
            # Scan all earlier ends; extend the best one that is smaller.
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
            best = max(best, dp[i])
        return best


# =====================================================================
# APPROACH 2 : patience sorting with binary search (O(n log n))
# =====================================================================
class SolutionTwo:
    """
    Purpose : Length of the longest strictly increasing subsequence.
    Inputs  : nums — integer array.
    Output  : int — LIS length.
    """

    def lengthOfLIS(self, nums: List[int]) -> int:
        tails: List[int] = []  # tails[k] = smallest tail of a k+1-length LIS
        for num in nums:
            # lower_bound: first index with tails[idx] >= num.
            lo, hi = 0, len(tails)
            while lo < hi:
                mid = (lo + hi) // 2
                if tails[mid] < num:
                    lo = mid + 1   # extend-past candidates stay
                else:
                    hi = mid       # shrink the insertion window
            if lo == len(tails):
                tails.append(num)  # num extends the longest sequence
            else:
                tails[lo] = num    # num improves slot lo (smaller tail)
        return len(tails)


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (nums, expected LIS). Both solutions must match.
    tests: List[Tuple[List[int], int]] = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),  # [2,3,7,101]
        ([0, 1, 0, 3, 2, 3], 4),            # [0,1,2,3]
        ([7, 7, 7, 7], 1),                  # strictly increasing → no ties
    ]

    total_us_1 = total_us_2 = 0.0
    total_kb_1 = total_kb_2 = 0
    all_pass = True

    for nums, expected in tests:
        # --- Approach 1: perf_counter for time, tracemalloc for RAM ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().lengthOfLIS(nums)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_1 += (t1 - t0) * 1e6
        total_kb_1 += peak1 // 1024

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().lengthOfLIS(nums)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_2 += (t1b - t0b) * 1e6
        total_kb_2 += peak2 // 1024

        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"nums={str(nums):28} A1={r1} A2={r2} expected={expected} "
              f"{'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches match every expected output."
          if all_pass
          else "FAIL : at least one answer is wrong.")