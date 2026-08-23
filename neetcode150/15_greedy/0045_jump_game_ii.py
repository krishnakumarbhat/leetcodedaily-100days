"""
=====================================================================
LeetCode 45 : Jump Game II                                     (Medium)
https://leetcode.com/problems/jump-game-ii/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    Start at index 0 of `nums`; from i you can jump at most nums[i]
    steps forward. Return the MINIMUM number of jumps to reach the
    last index. The end is guaranteed reachable.
---------------------------------------------------------------------
INTUITION
    Think in BFS LAYERS over the implicit jump graph. Layer k = all
    positions reachable with ≤ k jumps — always one contiguous
    interval [l, r]. One more jump from any cell in the interval
    reaches at most max(i + nums[i]); the greedy jump maximizes that
    single frontier value, and maximizing every layer's right edge
    minimizes the number of layers needed → minimal jumps.
---------------------------------------------------------------------
APPROACH 1 — BFS-layered greedy (BEST)
    curEnd = current layer's right edge; far = furthest any cell in
    the layer can reach. When i reaches curEnd, one jump is consumed
    and curEnd = far.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Reverse greedy (leftmost reachable, O(n²))
    Work backwards: repeatedly find the LEFTMOST index that can jump
    onto the current target. Landing leftmost leaves the most future
    options open → provably optimal, but re-scans per jump.
    Time  Complexity : O(n²)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — why furthest-per-layer is provably optimal
    Exchange argument: every cell c in layer k satisfies c ≤ r, so
    c + nums[c] ≤ maxReach. The greedy frontier [r, maxReach] CONTAINS
    the frontier any other choice would create → any path a rival
    follows, we can follow too → greedy needs no more jumps than any
    rival. Interval-frontier monotonicity (same as Jump Game I) is the
    mathematical backbone.
---------------------------------------------------------------------
REAL LIFE
    • Router/CDN hop planning: minimum hops to deliver a packet.
    • EV range planning: minimal charging stops given per-stop range.
    • Game speed-run routing: minimal moves to a goal.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : BFS-layered greedy (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the minimum number of jumps to reach the end.
    Inputs  : nums — list of ints, nums[i] = max forward jump length.
    Output  : int — minimal jump count (end guaranteed reachable).
    """

    def jump(self, nums: List[int]) -> int:
        jumps = 0   # layers (jumps) consumed so far
        cur_end = 0 # right edge of the current jump layer
        far = 0     # furthest cell the current layer can reach

        # Last cell never needs processing — arriving there ends it.
        for i in range(len(nums) - 1):
            far = max(far, i + nums[i])  # widen next frontier from here

            if i == cur_end:             # current layer fully swept
                jumps += 1               # must take exactly one more jump
                cur_end = far            # its frontier = next layer
        return jumps

# =====================================================================
# APPROACH 2 : Reverse greedy — hop backwards to leftmost reachable
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the minimum number of jumps to reach the end.
    Inputs  : nums — list of ints, nums[i] = max forward jump length.
    Output  : int — minimal jump count (end guaranteed reachable).
    """

    def jump(self, nums: List[int]) -> int:
        jumps = 0
        pos = len(nums) - 1  # target cell to reach from the left

        # Each pass lands `pos` one jump closer to index 0.
        while pos > 0:
            # Leftmost takeoff cell that can jump onto pos — landing
            # leftmost keeps the most future options open.
            for i in range(pos):
                if i + nums[i] >= pos:
                    pos = i
                    jumps += 1
                    break   # restart the search from the new target
        return jumps


# =====================================================================
# BENCHMARK — both approaches, time + peak memory per approach
# =====================================================================
if __name__ == "__main__":
    # Official examples + all-ones walk + already-at-end + direct hop.
    tests: List[List[int]] = [
        [2, 3, 1, 1, 4],  # → 2
        [2, 3, 0, 1, 4],  # → 2
        [1, 1, 1, 1],     # → 3
        [0],              # → 0
        [1, 2, 3],        # → 2  (0→1→2; jump=1 forbids direct hop)
    ]
    expected = [2, 2, 3, 0, 2]

    def run_all(solve) -> tuple[bool, float, int]:
        """Time one solver over every test; return (allPass, µs, peakBytes)."""
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = all(solve(t) == e for t, e in zip(tests, expected))
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return ok, (t1 - t0) * 1e6, peak

    ok1, us1, peak1 = run_all(lambda t: SolutionOne().jump(t))
    ok2, us2, peak2 = run_all(lambda t: SolutionTwo().jump(t))

    print(f"Approach 1 (BFS-layered)   : {'PASS' if ok1 else 'FAIL'}  time = {us1:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (reverse greedy) : {'PASS' if ok2 else 'FAIL'}  time = {us2:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches return the minimal jump count."
          if ok1 and ok2
          else "FAIL : at least one approach is wrong.")
