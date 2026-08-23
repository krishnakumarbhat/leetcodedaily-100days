"""
=====================================================================
LeetCode 435 : Non-overlapping Intervals                      (Medium)
https://leetcode.com/problems/non-overlapping-intervals/
Category   : Intervals
---------------------------------------------------------------------
PROBLEM
    Given intervals [start, end], return the MINIMUM number to remove
    so the rest are pairwise non-overlapping. Equivalently: keep the
    LARGEST non-overlapping subset. (Closed intervals: [1,2] and
    [2,3] DO overlap at point 2.)
---------------------------------------------------------------------
INTUITION
    Keep the interval that leaves the most room behind it — the one
    ending EARLIEST. Greedy: sort by end, keep it, skip whatever
    overlaps it. Optimality via exchange argument: swap any optimal
    solution's first interval for the earliest-ending one — it ends
    no later, so it conflicts with no more intervals.
---------------------------------------------------------------------
APPROACH 1 — Greedy: sort by END, keep earliest-ending (BEST)
    Sort by end. Track the last KEPT end; intervals starting before
    it overlap the kept interval -> remove. Otherwise keep + advance.
    Time  Complexity : O(n log n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Sort by start + DP
    dp[i] = best kept-count of a subset ending at i:
        dp[i] = 1 + max(dp[j]) for j < i with end[j] <= start[i]
    Answer = n - max(dp). Provably correct, no greedy leap — O(n^2).
    Time  Complexity : O(n^2)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Video editors dropping overlapping clips to make a timeline.
    • Task schedulers dropping lower-priority jobs that clash.
    • Merging partner feeds: deduplicate conflicting ranges.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List

Interval = List[int]


# =====================================================================
# APPROACH 1 : greedy by end time (exchange-argument optimal)
# =====================================================================
class SolutionOne:
    """
    Purpose : Minimum removals so the rest are non-overlapping.
    Inputs  : intervals — [start, end] closed intervals.
    Output  : int — number of intervals that must be removed.
    """

    def erase_overlap_intervals(self, intervals: List[Interval]) -> int:
        if not intervals:
            return 0

        # Sort by END — the greedy key: finish early, leave room.
        intervals.sort(key=lambda iv: iv[1])

        kept = 1                    # the first interval is always kept
        last_end = intervals[0][1]  # end of the last KEPT interval
        for i in range(1, len(intervals)):
            if intervals[i][0] < last_end:
                # Starts before the kept interval ends -> overlap
                # (closed intervals -> strict '<') -> must remove it.
                continue
            # Disjoint from everything kept so far -> keep it.
            kept += 1
            last_end = intervals[i][1]
        return len(intervals) - kept


# =====================================================================
# APPROACH 2 : sort by start + O(n^2) DP
# =====================================================================
class SolutionTwo:
    """
    Purpose : Minimum removals, computed with interval-scheduling DP.
    Inputs  : intervals — [start, end] closed intervals.
    Output  : int — number of intervals that must be removed.
    """

    def erase_overlap_intervals(self, intervals: List[Interval]) -> int:
        n = len(intervals)
        if n == 0:
            return 0

        intervals.sort()  # by start

        # dp[i] = best kept-count of a subset whose LAST element is i.
        dp = [1] * n
        best = 1
        for i in range(1, n):
            for j in range(i):
                # closed intervals: j may precede i only if end[j] <= start[i]
                if intervals[j][1] <= intervals[i][0]:
                    dp[i] = max(dp[i], dp[j] + 1)
            best = max(best, dp[i])
        return n - best  # remove everything we did not keep


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, verify + time + memory
# =====================================================================
if __name__ == "__main__":
    tests: List[List[Interval]] = [
        [[1, 2], [2, 3], [3, 4], [1, 3]],       # remove 1
        [[1, 2], [1, 2], [1, 2]],               # remove 2
        [[1, 100], [11, 22], [1, 11], [2, 12]], # remove 1
    ]

    def brute(ivs: List[Interval]) -> int:
        """Exhaustive subset search (tests are small): n - max keepable."""
        n = len(ivs)
        best_keep = 0
        for mask in range(1 << n):
            ok, cnt = True, 0
            for i in range(n):
                if not (mask & (1 << i)):
                    continue
                cnt += 1
                for j in range(i + 1, n):
                    if (mask & (1 << j)) and ivs[i][0] < ivs[j][1] and ivs[j][0] < ivs[i][1]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                best_keep = max(best_keep, cnt)
        return n - best_keep

    all_pass = True
    for t, case in enumerate(tests, 1):

        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().erase_overlap_intervals([iv[:] for iv in case])
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok1 = r1 == brute(case)

        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().erase_overlap_intervals([iv[:] for iv in case])
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok2 = r2 == brute(case)

        pass_ = ok1 and ok2
        all_pass = all_pass and pass_
        print(f"Test {t} : {'PASS' if pass_ else 'FAIL'}"
              f"  A1={(t1 - t0) * 1e6:.2f}us/{peak1 // 1024}KB"
              f"  A2={(t1b - t0b) * 1e6:.2f}us/{peak2 // 1024}KB"
              f"  removals={r1}")

    print("PASS : greedy and DP agree with the exhaustive optimum."
          if all_pass
          else "FAIL : at least one approach disagrees with brute force.")
