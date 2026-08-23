"""
=====================================================================
LeetCode 56 : Merge Intervals                                   (Medium)
https://leetcode.com/problems/merge-intervals/
Category   : Intervals
---------------------------------------------------------------------
PROBLEM
    Given an array of intervals [start_i, end_i], merge ALL overlapping
    intervals and return the resulting array.
    Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
---------------------------------------------------------------------
INTUITION
    Two closed intervals overlap iff a.start <= b.end and b.start
    <= a.end. If we SORT by start, touching intervals arrive
    consecutively, so one sweep with a "current block" is enough:
    extend the block's end when the next interval overlaps, else
    open a new block.
---------------------------------------------------------------------
APPROACH 1 — Sort by start + sweep into a result list (BEST)
    Sort ascending. Walk once. If the current interval starts after
    the last block ends -> new block. Else extend the block's end.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Sort by start + in-place compaction
    Same rule, but merged blocks are written back into the FRONT of
    the input list (slot k) and the tail is trimmed — the input array
    itself becomes the answer.
    Time  Complexity : O(n log n)   Space Complexity : O(1) extra
---------------------------------------------------------------------
REAL LIFE
    • Calendar apps collapse overlapping events into blocks.
    • Log analyzers merge timestamp ranges (downtime windows).
    • Load balancers coalesce busy time spans of a server.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Optional

Interval = List[int]


# =====================================================================
# APPROACH 1 : sort by start + sweep into a result list
# =====================================================================
class SolutionOne:
    """
    Purpose : Merge all overlapping intervals.
    Inputs  : intervals — list of [start, end] closed intervals.
    Output  : merged list of non-overlapping, start-sorted intervals.
    """

    def merge(self, intervals: List[Interval]) -> List[Interval]:
        # Sort lexicographically — overlapping intervals become neighbours.
        intervals.sort()

        out: List[Interval] = []
        for it in intervals:
            if not out or out[-1][1] < it[0]:
                # Last block ends BEFORE this one starts -> no overlap
                # (strict '<' : equal points would still touch).
                out.append(it)
            else:
                # Overlap -> absorb it by extending the block's end.
                out[-1][1] = max(out[-1][1], it[1])
        return out


# =====================================================================
# APPROACH 2 : sort by start + in-place compaction
# =====================================================================
class SolutionTwo:
    """
    Purpose : Merge all overlapping intervals, compacting the input
              list in place (no extra result list).
    Inputs  : intervals — list of [start, end] closed intervals.
    Output  : the same list, compacted to the merged blocks.
    """

    def merge(self, intervals: List[Interval]) -> List[Interval]:
        intervals.sort()
        k = 0  # number of merged blocks written to the front
        for i in range(1, len(intervals)):
            if intervals[k][1] >= intervals[i][0]:
                # Block k overlaps intervals[i] -> extend block k in place.
                intervals[k][1] = max(intervals[k][1], intervals[i][1])
            else:
                # No overlap -> promote intervals[i] as the next block.
                k += 1
                intervals[k] = intervals[i]
        del intervals[k + 1:]  # trim the absorbed tail
        return intervals


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, verify + time + memory
# =====================================================================
if __name__ == "__main__":
    # (input) triplets — validator uses point-coverage equality so no
    # reference implementation is needed.
    tests: List[List[Interval]] = [
        [[1, 3], [2, 6], [8, 10], [15, 18]],
        [[1, 4], [4, 5]],
        [[1, 4], [0, 2], [3, 5], [6, 7], [6, 9], [10, 11]],
    ]

    def coverage(ivs: List[Interval]) -> List[int]:
        """Sorted unique set of integer points covered by `ivs`."""
        pts: List[int] = []
        for s, e in ivs:
            pts.extend(range(s, e + 1))
        return sorted(set(pts))

    def valid(res: List[Interval], orig: List[Interval]) -> bool:
        """Result must be sorted, disjoint, and cover the exact same points."""
        for i in range(1, len(res)):
            if res[i][0] <= res[i - 1][1]:
                return False  # overlapping or unsorted
        return coverage(res) == coverage(orig)

    all_pass = True
    for t, case in enumerate(tests, 1):

        # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().merge([iv[:] for iv in case])
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok1 = valid(r1, case)

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().merge([iv[:] for iv in case])
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok2 = valid(r2, case)

        pass_ = ok1 and ok2
        all_pass = all_pass and pass_
        print(f"Test {t} : {'PASS' if pass_ else 'FAIL'}"
              f"  A1={(t1 - t0) * 1e6:.2f}us/{peak1 // 1024}KB"
              f"  A2={(t1b - t0b) * 1e6:.2f}us/{peak2 // 1024}KB"
              f"  merged=[{len(r1)} blocks]")

    print("PASS : both approaches merge all tests correctly."
          if all_pass
          else "FAIL : at least one approach produced a wrong merge.")
