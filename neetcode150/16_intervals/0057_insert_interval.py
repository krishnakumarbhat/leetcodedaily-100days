"""
=====================================================================
LeetCode 57 : Insert Interval                                  (Medium)
https://leetcode.com/problems/insert-interval/
Category   : Intervals
---------------------------------------------------------------------
PROBLEM
    Given a SORTED, non-overlapping interval list and one
    `new_interval`, insert it, merging any overlaps, and return the
    list still sorted and non-overlapping.
    Example: [[1,3],[6,9]] + [2,5] -> [[1,5],[6,9]]
---------------------------------------------------------------------
INTUITION
    The sortedness splits the list into three zones around the new
    interval: intervals ending before new.start (untouched), the
    contiguous merge window that touches new_interval, and intervals
    starting after new.end (untouched). Melt the middle window into
    one block [min start, max end].
---------------------------------------------------------------------
APPROACH 1 — Three-phase linear sweep (BEST)
    Phase A: copy intervals with end < new.start. Phase B: absorb
    every interval with start <= new.end, extending new_interval.
    Phase C: copy the rest.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Binary-search the merge window, then splice
    left  = first index whose end   >= new.start (bisect_left over ends)
    right = last  index whose start <= new.end  (bisect_right over starts)
    The whole merge zone is [left, right]; splice around it.
    Time  Complexity : O(log n + n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Booking systems: insert a new reservation into a sorted room
      schedule without breaking the disjoint invariant.
    • IP whitelist / firewall rules maintained as disjoint ranges.
    • Calendar imports that must merge a new event into an existing
      timeline.
=====================================================================
"""

from __future__ import annotations

import bisect
import time
import tracemalloc
from typing import List

Interval = List[int]


# =====================================================================
# APPROACH 1 : three-phase linear sweep
# =====================================================================
class SolutionOne:
    """
    Purpose : Insert new_interval into a sorted disjoint interval list.
    Inputs  : intervals    — sorted, non-overlapping [start, end] list.
              new_interval — the interval to insert.
    Output  : merged sorted interval list.
    """

    def insert(self, intervals: List[Interval], new_interval: Interval) -> List[Interval]:
        out: List[Interval] = []
        i, n = 0, len(intervals)

        # Phase A : strictly BEFORE — ends before new.start mean no contact.
        while i < n and intervals[i][1] < new_interval[0]:
            out.append(intervals[i])
            i += 1

        # Phase B : the merge zone. Overlap test: start <= new.end.
        # Absorbing grows new.end, so chain merges fall out for free.
        while i < n and intervals[i][0] <= new_interval[1]:
            new_interval[0] = min(new_interval[0], intervals[i][0])
            new_interval[1] = max(new_interval[1], intervals[i][1])
            i += 1
        out.append(new_interval)

        # Phase C : strictly AFTER — everything remaining is untouched.
        out.extend(intervals[i:])
        return out


# =====================================================================
# APPROACH 2 : binary-search the merge window, then splice
# =====================================================================
class SolutionTwo:
    """
    Purpose : Insert new_interval via binary search + splice.
    Inputs  : intervals    — sorted, non-overlapping interval list.
              new_interval — the interval to insert.
    Output  : merged sorted interval list.
    """

    def insert(self, intervals: List[Interval], new_interval: Interval) -> List[Interval]:
        ends = [iv[1] for iv in intervals]     # O(n) scan for the searches
        starts = [iv[0] for iv in intervals]

        # left = first index whose end >= new.start (candidate to merge).
        left = bisect.bisect_left(ends, new_interval[0])
        # right = last index whose start <= new.end.
        right = bisect.bisect_right(starts, new_interval[1]) - 1

        out: List[Interval] = intervals[:left]      # untouched BEFORE window
        if left <= right:
            # Melt the whole window [left, right] into new_interval.
            new_interval[0] = min(new_interval[0], intervals[left][0])
            new_interval[1] = max(new_interval[1], intervals[right][1])
        out.append(new_interval)                    # the merged block
        out.extend(intervals[right + 1:])           # untouched AFTER window
        return out


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, verify + time + memory
# =====================================================================
if __name__ == "__main__":
    tests: List[tuple] = [
        ([[1, 3], [6, 9]], [2, 5]),
        ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),
        ([[1, 3], [4, 5]], [6, 7]),
    ]

    def coverage(ivs: List[Interval]) -> List[int]:
        """Sorted unique point set covered by `ivs`."""
        pts: List[int] = []
        for s, e in ivs:
            pts.extend(range(s, e + 1))
        return sorted(set(pts))

    def valid(res: List[Interval], base: List[Interval], ni: Interval) -> bool:
        """Result sorted/disjoint and covering base ∪ {ni} exactly."""
        for i in range(1, len(res)):
            if res[i][0] <= res[i - 1][1]:
                return False
        return coverage(res) == coverage(base + [ni])

    all_pass = True
    for t, (case, ni) in enumerate(tests, 1):

        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().insert([iv[:] for iv in case], ni[:])
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok1 = valid(r1, case, ni)

        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().insert([iv[:] for iv in case], ni[:])
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok2 = valid(r2, case, ni)

        pass_ = ok1 and ok2
        all_pass = all_pass and pass_
        print(f"Test {t} : {'PASS' if pass_ else 'FAIL'}"
              f"  A1={(t1 - t0) * 1e6:.2f}us/{peak1 // 1024}KB"
              f"  A2={(t1b - t0b) * 1e6:.2f}us/{peak2 // 1024}KB"
              f"  merged=[{len(r1)} blocks]")

    print("PASS : both approaches insert correctly on all tests."
          if all_pass
          else "FAIL : at least one approach produced a wrong insert.")
