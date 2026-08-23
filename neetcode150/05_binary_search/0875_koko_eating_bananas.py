"""
=====================================================================
LeetCode 0875 : Koko Eating Bananas                                (Medium)
https://leetcode.com/problems/koko-eating-bananas/
Category   : Binary Search (on the ANSWER space)
---------------------------------------------------------------------
PROBLEM
    Koko must eat `piles[i]` bananas from pile i; she eats at most `k`
    bananas per hour, takes ceil(piles[i]/k) hours per pile, and may
    not move on until a pile is finished. Return the MINIMUM k that
    lets her finish all piles within `h` hours.

---------------------------------------------------------------------
INTUITION
    The speed k lives in [1, max(piles)]. "canFinish(k)" is monotone:
    k too small → FALSE; once k is large enough → TRUE forever
    (faster never needs MORE hours). The answer is the FIRST TRUE
    speed — a textbook lower-bound binary search. This is the
    "binary search on the answer" pattern: the data is not searched
    directly; the PREDICATE over the answer space is.

---------------------------------------------------------------------
APPROACH 1 — Binary search on speed (BEST, O(n log M))
    lo = 1, hi = max(piles). Probe mid and evaluate canFinish(mid)
    in O(n) by summing ceil(piles[i]/mid):
      • hours <= h → feasible → optimum is mid or less (hi = mid).
      • hours >  h → too slow → lo = mid + 1.
    The `lo < hi` loop collapses onto the smallest feasible speed.
    Time  Complexity : O(n log M)   M = max(piles); log M probes,
                        each an O(n) sweep.
    Space Complexity : O(1)

---------------------------------------------------------------------
APPROACH 2 — Linear sweep of speeds (contrast, O(n·M))
    Try every k from 1 to max(piles); return the first feasible one.
    Identical result, but with max(piles) = 1e9 that is a billion
    sweeps — the log M probe count is what scales.
    Time  Complexity : O(n·M)   Space Complexity : O(1)

---------------------------------------------------------------------
DEEP DIVE — searching the ANSWER space, not the data
    In 0704 the predicate was "nums[i] == target" over indices; here
    it is "canFinish(k)" over SPEEDS. Both are monotone, so the same
    halving loop applies. You only need (1) a bounded monotone answer
    range and (2) an O(f(n)) feasibility oracle. That combination
    powers rate limiting ("fastest rate that still passes QoS"),
    congestion control, job scheduling ("minimum throughput that
    meets the deadline"), and capacity planning.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Binary search on the speed (minimize feasible k)
# =====================================================================
class Solution_BinarySearchSpeed:
    """
    Purpose : Return the minimum eating speed that finishes in h hours.
    Inputs  : piles — List[int] of bananas per pile.
              h     — hours available (h >= len(piles)).
    Output  : int minimum feasible speed k.
    """

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # The answer lives in [1, max(piles)] — the speed space.
        lo, hi = 1, max(piles)

        # `lo < hi` + hi = mid collapses onto the FIRST feasible k.
        while lo < hi:
            mid = lo + (hi - lo) // 2      # probe a speed.

            # canFinish(mid): sum of ceil(pile/mid) must be <= h.
            # ceil(a/b) = (a + b - 1) // b — integer division trick.
            hours = sum((p + mid - 1) // mid for p in piles)

            if hours <= h:
                hi = mid                   # feasible → try slower.
            else:
                lo = mid + 1               # too slow → speed up.

        return lo                          # smallest feasible speed.

# =====================================================================
# APPROACH 2 : Linear sweep of speeds (contrast)
# =====================================================================
class Solution_LinearSpeed:
    """
    Purpose : Return the minimum eating speed that finishes in h hours.
    Inputs  : piles — List[int] of bananas per pile.
              h     — hours available (h >= len(piles)).
    Output  : int minimum feasible speed k.
    """

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # Try every speed from 1 upward; first feasible one wins.
        for k in range(1, max(piles) + 1):
            hours = sum((p + k - 1) // k for p in piles)
            if hours <= h:
                return k                   # smallest feasible speed.

        return max(piles)                  # unreachable per constraints.


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test cases from the official examples.
    tests = [
        ([3, 6, 7, 11], 8),      # expect 4
        ([30, 11, 23, 4, 20], 5),  # expect 30
        ([30, 11, 23, 4, 20], 6)   # expect 23
    ]

    all_ok = True
    for t_idx, (piles, h) in enumerate(tests):
        # --- Approach 1: time + tracemalloc peak ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = Solution_BinarySearchSpeed().minEatingSpeed(piles, h)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + tracemalloc peak ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = Solution_LinearSpeed().minEatingSpeed(piles, h)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == r2                     # both must agree.
        all_ok = all_ok and ok
        print(f"Test {t_idx+1}: h={h} | A1 BS-speed = {r1} "
              f"({(t1-t0)*1e6:.2f} µs, {peak1} B) | A2 linear = {r2} "
              f"({(t1b-t0b)*1e6:.2f} µs, {peak2} B) | {'PASS' if ok else 'FAIL'}")

    print("PASS : both approaches agree on all tests."
          if all_ok else "FAIL : at least one answer is wrong.")