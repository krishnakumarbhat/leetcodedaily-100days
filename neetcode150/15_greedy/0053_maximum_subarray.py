"""
=====================================================================
LeetCode 53 : Maximum Subarray                                 (Medium)
https://leetcode.com/problems/maximum-subarray/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    Given an integer array `nums`, find the CONTIGUOUS subarray with
    the largest sum and return that sum.
---------------------------------------------------------------------
INTUITION
    For every index i we only need: "what is the best sum of a
    subarray that ENDS at i?" It either starts fresh at i or extends
    the best subarray ending at i-1. Keep only the better option —
    the local choice — and it provably composes into the global
    optimum because any subarray ending at i extends the best suffix
    ending at i-1 (optimal substructure).
---------------------------------------------------------------------
APPROACH 1 — Kadane's algorithm (BEST)
    Invariant: `ending` = best sum ending exactly at current index;
    `best` = champion over all end positions.
        ending = max(nums[i], ending + nums[i])
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Prefix sums + minimum prefix
    sum(l..r) = prefix[r] - prefix[l-1]; maximize by pairing each
    prefix with the SMALLEST prefix before it.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — when is local-optimum greedy globally optimal?
    Safe here: optimal substructure. The decision "extend or restart"
    at i depends only on the best suffix at i-1 — the future can
    never invalidate it (exchange argument: any optimal subarray is
    built by repeatedly taking the max-extension). Greedy FAILS on
    e.g. 0/1 knapsack precisely because a local pick can block a
    better global combination.
---------------------------------------------------------------------
REAL LIFE
    • Stock-trading: largest profit window in a price series
      (max subarray of daily deltas).
    • Audio / signal processing: loudest burst in a waveform.
    • Genomics: highest-scoring segment of an alignment.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Kadane's algorithm (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the largest sum of any contiguous subarray.
    Inputs  : nums — list of integers to search inside.
    Output  : int — the maximum subarray sum.
    """

    def maxSubArray(self, nums: List[int]) -> int:
        # Invariant: `ending` = best sum ending at the current index,
        # `best` = champion over every end position so far.
        ending = nums[0]
        best = nums[0]

        # Each element decides: restart at i, or extend the winner
        # ending at i-1. A negative `ending` never helps future sums.
        for i in range(1, len(nums)):
            ending = max(nums[i], ending + nums[i])  # extend-or-restart
            best = max(best, ending)                 # track global champion
        return best

# =====================================================================
# APPROACH 2 : Prefix sums + minimum prefix seen so far
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the largest sum of any contiguous subarray.
    Inputs  : nums — list of integers to search inside.
    Output  : int — the maximum subarray sum.
    """

    def maxSubArray(self, nums: List[int]) -> int:
        # sum(l..r) = prefix[r] - prefix[l-1]. For a fixed r the best
        # partner is the smallest prefix that appears BEFORE r.
        pref = 0       # running prefix sum
        min_pref = 0   # smallest prefix strictly before current index
        best = nums[0]

        for x in nums:
            pref += x                    # grow the prefix by one element
            best = max(best, pref - min_pref)  # max vertical drop ending here
            min_pref = min(min_pref, pref)     # tighten the floor for later
        return best


# =====================================================================
# BENCHMARK — both approaches, time + peak memory per approach
# =====================================================================
if __name__ == "__main__":
    # Official samples + a single-element edge case + all-positive run.
    tests: List[List[int]] = [
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],  # → 6
        [1],                              # → 1
        [5, 4, -1, 7, 8],                 # → 23
    ]
    expected = [6, 1, 23]

    def run_all(solve) -> tuple[bool, float, int]:
        """Time one solver over every test; return (allPass, µs, peakBytes)."""
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = all(solve(t) == e for t, e in zip(tests, expected))
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return ok, (t1 - t0) * 1e6, peak

    ok1, us1, peak1 = run_all(lambda t: SolutionOne().maxSubArray(t))
    ok2, us2, peak2 = run_all(lambda t: SolutionTwo().maxSubArray(t))

    print(f"Approach 1 (Kadane)      : {'PASS' if ok1 else 'FAIL'}  time = {us1:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (prefix drop)  : {'PASS' if ok2 else 'FAIL'}  time = {us2:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches return the correct max subarray sum."
          if ok1 and ok2
          else "FAIL : at least one approach is wrong.")
