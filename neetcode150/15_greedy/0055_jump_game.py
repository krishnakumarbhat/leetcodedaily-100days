"""
=====================================================================
LeetCode 55 : Jump Game                                          (Medium)
https://leetcode.com/problems/jump-game/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    Start at index 0 of `nums`. From index i you can jump at most
    nums[i] steps forward. Return True if you can reach the last
    index.
---------------------------------------------------------------------
INTUITION
    Only the FURTHEST reachable index matters. Track one scalar:
        reach = max(reach, i + nums[i])
    If the sweep pointer passes `reach`, that index is unreachable →
    False. Larger reach strictly dominates smaller (exchange
    argument), so this single-number greedy is exact.
---------------------------------------------------------------------
APPROACH 1 — Greedy furthest-reach (BEST)
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — DP frontier O(n²) (why greedy is better)
    reachable[i] = True and stamp every cell i+1 .. i+nums[i]. The
    reachable set is always ONE interval [0, reach] — the DP table
    is n redundant booleans where a single int suffices.
    Time  Complexity : O(n²)   Space Complexity : O(n)
---------------------------------------------------------------------
DEEP DIVE — exchange argument for furthest-reach
    Induction: greedy position after k moves ≥ optimal position after
    k moves. Since our current index is ≥ theirs, our jump options
    cover all of theirs, so we can imitate any winning path. This
    monotone-domination property is the fingerprint of a correct
    greedy: local "go furthest" is never worse than any rival.
---------------------------------------------------------------------
REAL LIFE
    • Game level design: can a player with given max jump widths
      cross a platform set?
    • Network reliability: can packets hop router-to-router given
      per-router max TTL hops?
    • Supply-chain feasibility: max pallet transfers per depot.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Greedy furthest-reach (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether the last index is reachable from index 0.
    Inputs  : nums — list of ints, nums[i] = max forward jump length.
    Output  : bool — True if index len(nums)-1 is reachable.
    """

    def canJump(self, nums: List[int]) -> bool:
        reach = 0  # furthest index reachable so far (frontier)

        # Sweep; the pointer i must never overtake the frontier.
        for i in range(len(nums)):
            if i > reach:
                return False                 # index i is unreachable → stuck
            reach = max(reach, i + nums[i])  # grow frontier from here
            if reach >= len(nums) - 1:
                return True                  # last index covered
        return True

# =====================================================================
# APPROACH 2 : DP reachable[] frontier (O(n²), for contrast)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether the last index is reachable from index 0.
    Inputs  : nums — list of ints, nums[i] = max forward jump length.
    Output  : bool — True if index len(nums)-1 is reachable.
    """

    def canJump(self, nums: List[int]) -> bool:
        reachable = [False] * len(nums)
        reachable[0] = True  # start cell is trivially reachable

        for i in range(len(nums)):
            if not reachable[i]:
                continue                     # dead cell: nothing propagates
            # Stamp every landing cell this jump offers as reachable.
            for j in range(i + 1, min(i + nums[i], len(nums) - 1) + 1):
                reachable[j] = True
        return reachable[-1]


# =====================================================================
# BENCHMARK — both approaches, time + peak memory per approach
# =====================================================================
if __name__ == "__main__":
    # Official examples + a zero-gap trap + never-leaves-start case.
    tests: List[List[int]] = [
        [2, 3, 1, 1, 4],   # → True  (2→3→4)
        [3, 2, 1, 0, 4],   # → False (stuck at index 3)
        [2, 0, 0],         # → True  (lands exactly on the end)
        [0, 1],            # → False (never leaves index 0)
    ]
    expected = [True, False, True, False]

    def run_all(solve) -> tuple[bool, float, int]:
        """Time one solver over every test; return (allPass, µs, peakBytes)."""
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = all(solve(t) == e for t, e in zip(tests, expected))
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return ok, (t1 - t0) * 1e6, peak

    ok1, us1, peak1 = run_all(lambda t: SolutionOne().canJump(t))
    ok2, us2, peak2 = run_all(lambda t: SolutionTwo().canJump(t))

    print(f"Approach 1 (greedy reach) : {'PASS' if ok1 else 'FAIL'}  time = {us1:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (DP frontier)   : {'PASS' if ok2 else 'FAIL'}  time = {us2:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree on every test case."
          if ok1 and ok2
          else "FAIL : at least one approach is wrong.")
