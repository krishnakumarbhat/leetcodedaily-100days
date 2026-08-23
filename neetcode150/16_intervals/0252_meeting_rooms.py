"""
=====================================================================
LeetCode 252 : Meeting Rooms                                     (Easy)
https://leetcode.com/problems/meeting-rooms/
Category   : Intervals
---------------------------------------------------------------------
PROBLEM
    Given an array of meeting intervals [start, end), return True if
    ONE person can attend ALL meetings (no two may overlap). Half-open
    intervals: ending at 4 and starting at 4 do NOT overlap.
---------------------------------------------------------------------
INTUITION
    After sorting by start, overlaps only occur between NEIGHBOURS:
    if intervals i < j overlap, then i and i+1 already overlap along
    the chain. So one adjacent-pair check suffices — provably.
---------------------------------------------------------------------
APPROACH 1 — Sort by start + adjacent overlap check (BEST)
    Sort. Walk once: if next.start < prev.end the previous meeting is
    still running -> False. Strict '<' encodes half-open semantics.
    Time  Complexity : O(n log n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Chronological event sweep (sweep-line)
    Flatten meetings into events (time, +1 start / -1 end). Sort by
    time with ENDS before STARTS at equal times. active += delta;
    active > 1 at any moment -> False.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Calendar clash detection before scheduling a new meeting.
    • Single-gym / single-instructor slot validation.
    • Stream scheduling: one worker, can jobs overlap?
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Tuple

Interval = List[int]


# =====================================================================
# APPROACH 1 : sort by start + adjacent overlap check
# =====================================================================
class SolutionOne:
    """
    Purpose : Report whether all meetings fit one room.
    Inputs  : intervals — [start, end) meetings.
    Output  : True iff no two meetings overlap.
    """

    def can_attend_meetings(self, intervals: List[Interval]) -> bool:
        # Sort by start — overlaps become adjacent afterwards.
        intervals.sort()
        for i in range(1, len(intervals)):
            # Half-open: next meeting starts BEFORE previous ends -> clash.
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True


# =====================================================================
# APPROACH 2 : chronological event sweep (sweep-line)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Report whether all meetings fit one room (event sweep).
    Inputs  : intervals — [start, end) meetings.
    Output  : True iff no two meetings overlap.
    """

    def can_attend_meetings(self, intervals: List[Interval]) -> bool:
        # events (time, delta). Sort key (time, kind) with kind 0 for
        # END (-1) and 1 for START (+1): ends sort first at equal times,
        # which is exactly the half-open "free at end" rule.
        events: List[Tuple[int, int]] = []
        for s, e in intervals:
            events.append((s, 1))
            events.append((e, 0))
        events.sort()

        active = 0
        for _, kind in events:
            active += 1 if kind == 1 else -1
            if active > 1:
                return False  # two meetings live simultaneously
        return True


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, verify + time + memory
# =====================================================================
if __name__ == "__main__":
    tests: List[List[Interval]] = [
        [[0, 30], [5, 10], [15, 20]],            # False
        [[7, 10], [2, 4]],                       # True
        [[0, 5], [5, 10], [10, 15], [3, 8]],     # False
    ]

    def brute(ivs: List[Interval]) -> bool:
        """Pairwise half-open overlap check — the definition itself."""
        for i in range(len(ivs)):
            for j in range(i + 1, len(ivs)):
                if ivs[i][0] < ivs[j][1] and ivs[j][0] < ivs[i][1]:
                    return False
        return True

    all_pass = True
    for t, case in enumerate(tests, 1):

        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().can_attend_meetings([iv[:] for iv in case])
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok1 = r1 == brute(case)

        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().can_attend_meetings([iv[:] for iv in case])
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok2 = r2 == brute(case)

        pass_ = ok1 and ok2
        all_pass = all_pass and pass_
        print(f"Test {t} : {'PASS' if pass_ else 'FAIL'}"
              f"  A1={(t1 - t0) * 1e6:.2f}us/{peak1 // 1024}KB"
              f"  A2={(t1b - t0b) * 1e6:.2f}us/{peak2 // 1024}KB"
              f"  can_attend={r1}")

    print("PASS : both approaches agree with the brute-force overlap check."
          if all_pass
          else "FAIL : at least one approach disagrees with brute force.")
