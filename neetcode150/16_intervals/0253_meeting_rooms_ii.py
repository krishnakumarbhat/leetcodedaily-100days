"""
=====================================================================
LeetCode 253 : Meeting Rooms II                                (Medium)
https://leetcode.com/problems/meeting-rooms-ii/
Category   : Intervals
---------------------------------------------------------------------
PROBLEM
    Given an array of meeting intervals [start, end), return the
    MINIMUM number of conference rooms required. Rooms free at end
    times (half-open: [0,5] and [5,10] share one room).
---------------------------------------------------------------------
INTUITION
    The answer is the maximum number of meetings ALIVE at one moment.
    Sweeping by start time, we only need to know which OPEN meeting
    ends first — a min-heap of end times answers that in O(log n)
    and always holds exactly the active meetings.
---------------------------------------------------------------------
APPROACH 1 — Sort by start + min-heap of end times (BEST)
    Sort by start. For each meeting: if the earliest-ending active
    meeting is over (heap top <= start), pop it (room reused). Push
    this meeting's end. Answer = max heap size.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Two pointers over sorted starts & ends
    Sort starts and ends SEPARATELY. If the next start precedes the
    earliest free time (starts[s] < ends[e]) a new room is needed;
    otherwise the room at ends[e] frees -> advance e.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Conference room booking across a company's calendar.
    • Database connection pool sizing from query timings.
    • Network bandwidth allocation: peak concurrent users.
=====================================================================
"""

from __future__ import annotations

import heapq
import time
import tracemalloc
from typing import List

Interval = List[int]


# =====================================================================
# APPROACH 1 : sort by start + min-heap of end times
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the minimum number of rooms for all meetings.
    Inputs  : intervals — [start, end) meetings.
    Output  : int — peak number of simultaneously active meetings.
    """

    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        intervals.sort()  # by start

        # Min-heap of END times of currently active meetings.
        ends: List[int] = []
        rooms = 0

        for s, e in intervals:
            # Reuse: the active meeting ending earliest is over (half-open
            # frees at its end time e_old <= s).
            if ends and ends[0] <= s:
                heapq.heappop(ends)  # that room is now free
            heapq.heappush(ends, e)  # this meeting occupies a room until e

            # heap size == meetings alive right now == rooms in use.
            rooms = max(rooms, len(ends))
        return rooms


# =====================================================================
# APPROACH 2 : two pointers over separately sorted starts/ends
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the minimum number of rooms (two-pointer sweep).
    Inputs  : intervals — [start, end) meetings.
    Output  : int — peak number of simultaneously active meetings.
    """

    def min_meeting_rooms(self, intervals: List[Interval]) -> int:
        starts = sorted(s for s, _ in intervals)
        ends = sorted(e for _, e in intervals)

        rooms = 0
        active = 0
        e = 0
        for s in range(len(starts)):
            # Close every room whose meeting finished by this start.
            while e < len(ends) and ends[e] <= starts[s]:
                active -= 1
                e += 1
            active += 1  # open the current meeting
            rooms = max(rooms, active)
        return rooms


# =====================================================================
# BENCHMARK — run both approaches on 3 tests, verify + time + memory
# =====================================================================
if __name__ == "__main__":
    tests: List[List[Interval]] = [
        [[0, 30], [5, 10], [15, 20]],                    # 2 rooms
        [[7, 10], [2, 4]],                               # 1 room
        [[0, 5], [5, 10], [10, 15], [15, 20], [3, 8]],   # 2 rooms
    ]

    def brute(ivs: List[Interval]) -> int:
        """Max number of meetings covering any single point (≥ 1 room)."""
        best = 1 if ivs else 0
        for i, (s, e) in enumerate(ivs):
            # half-open overlap with a DIFFERENT meeting (skip self)
            count = sum(s < b[1] and b[0] < e for j, b in enumerate(ivs) if j != i)
            best = max(best, count)
        return best

    all_pass = True
    for t, case in enumerate(tests, 1):

        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().min_meeting_rooms([iv[:] for iv in case])
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok1 = r1 == brute(case)

        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().min_meeting_rooms([iv[:] for iv in case])
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok2 = r2 == brute(case)

        pass_ = ok1 and ok2
        all_pass = all_pass and pass_
        print(f"Test {t} : {'PASS' if pass_ else 'FAIL'}"
              f"  A1={(t1 - t0) * 1e6:.2f}us/{peak1 // 1024}KB"
              f"  A2={(t1b - t0b) * 1e6:.2f}us/{peak2 // 1024}KB"
              f"  rooms={r1}")

    print("PASS : both approaches return the brute-force peak occupancy."
          if all_pass
          else "FAIL : at least one approach disagrees with brute force.")
