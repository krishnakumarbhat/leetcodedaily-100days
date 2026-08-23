"""
=====================================================================
LeetCode 1851 : Minimum Interval to Include Each Query          (Hard)
https://leetcode.com/problems/minimum-interval-to-include-each-query/
Category   : Intervals
---------------------------------------------------------------------
PROBLEM
    Given intervals [start, end] (length = end - start + 1) and
    queries (points), for EVERY query return the length of the
    SHORTEST interval containing that point, or -1 if none does.
    Example: intervals=[[1,4],[2,4],[3,6]], queries=[2,3,4,5]
             -> [3,3,3,4]
---------------------------------------------------------------------
INTUITION
    Answer queries in ASCENDING order: then candidate intervals only
    arrive (start <= q) and expire (end < q) monotonically. Sort
    intervals by start for the arrival pointer; a min-heap of
    (length, end) keeps the shortest candidate on top; expired
    entries are evicted lazily on peek.
---------------------------------------------------------------------
APPROACH 1 — Offline: sort queries + sweep + min-heap (BEST)
    Sort (query, index) pairs. Pointer p walks intervals by start;
    push (length, end) for every start <= q. Pop while top's end < q
    (lazy deletion). Top is the shortest interval covering q.
    Time  Complexity : O((n + q) log n)   Space Complexity : O(n + q)
---------------------------------------------------------------------
APPROACH 2 — Brute force, length-sorted (contrast)
    Sort intervals by length ascending; the first interval containing
    a query is the shortest one for it.
    Time  Complexity : O(n * q) worst case   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Ride-hailing: shortest ride range containing a pickup point.
    • CDN: which cached-file version's validity window covers a
      request timestamp (shortest window wins).
    • Promotions engine: cheapest discount window containing a date.
=====================================================================
"""

from __future__ import annotations

import heapq
import time
import tracemalloc
from typing import List

Interval = List[int]


# =====================================================================
# APPROACH 1 : offline sort + min-heap with lazy deletion
# =====================================================================
class SolutionOne:
    """
    Purpose : Shortest interval length containing each query point.
    Inputs  : intervals — [start, end] (length = end - start + 1).
              queries   — points to answer, in ANY order.
    Output  : answer[i] = min length covering queries[i], else -1.
    """

    def min_interval(self, intervals: List[Interval], queries: List[int]) -> List[int]:
        intervals.sort()  # by start — arrival order for the sweep

        # (query, original_index) — answer in ascending query order,
        # then scatter answers back to their original positions.
        pairs = sorted((q, i) for i, q in enumerate(queries))

        # Min-heap of (length, end): shortest candidate on top.
        heap: List[tuple] = []
        ans = [-1] * len(queries)
        p = 0  # sweep pointer into intervals

        for q, idx in pairs:
            # Add every interval whose start has passed — it can now be
            # an answer for this query AND all later (larger) queries.
            while p < len(intervals) and intervals[p][0] <= q:
                s, e = intervals[p]
                heapq.heappush(heap, (e - s + 1, e))
                p += 1

            # Lazy deletion: while the SHORTEST candidate ends before q,
            # it covers no later query either — evict it.
            while heap and heap[0][1] < q:
                heapq.heappop(heap)

            # Heap top (if any) is the shortest interval covering q.
            if heap:
                ans[idx] = heap[0][0]
        return ans


# =====================================================================
# APPROACH 2 : brute force, length-sorted with early hit
# =====================================================================
class SolutionTwo:
    """
    Purpose : Shortest interval length containing each query point.
    Inputs  : intervals — [start, end] (length = end - start + 1).
              queries   — points to answer, in ANY order.
    Output  : answer[i] = min length covering queries[i], else -1.
    """

    def min_interval(self, intervals: List[Interval], queries: List[int]) -> List[int]:
        # Sort by LENGTH ascending: the first hit per query is optimal.
        intervals.sort(key=lambda iv: iv[1] - iv[0])

        ans = [-1] * len(queries)
        for i, q in enumerate(queries):
            for s, e in intervals:
                if s <= q <= e:
                    ans[i] = e - s + 1  # shortest interval covering q
                    break
        return ans


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, verify + time + memory
# =====================================================================
if __name__ == "__main__":
    tests: List[tuple] = [
        ([[1, 4], [2, 4], [3, 6]], [2, 3, 4, 5]),            # official example
        ([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]),# mixed + miss
        ([[1, 1]], [1, 0, 2]),                               # single point
    ]

    def brute(ivs: List[Interval], qs: List[int]) -> List[int]:
        """For each query, scan every interval — the definition itself."""
        out: List[int] = []
        for q in qs:
            best = -1
            for s, e in ivs:
                if s <= q <= e:
                    best = e - s + 1 if best == -1 else min(best, e - s + 1)
            out.append(best)
        return out

    all_pass = True
    for t, (case, qs) in enumerate(tests, 1):

        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().min_interval([iv[:] for iv in case], qs[:])
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok1 = r1 == brute(case, qs)

        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().min_interval([iv[:] for iv in case], qs[:])
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok2 = r2 == brute(case, qs)

        pass_ = ok1 and ok2
        all_pass = all_pass and pass_
        print(f"Test {t} : {'PASS' if pass_ else 'FAIL'}"
              f"  A1={(t1 - t0) * 1e6:.2f}us/{peak1 // 1024}KB"
              f"  A2={(t1b - t0b) * 1e6:.2f}us/{peak2 // 1024}KB"
              f"  answers={r1}")

    print("PASS : heap-based offline sweep matches brute force on all tests."
          if all_pass
          else "FAIL : at least one approach disagrees with brute force.")
