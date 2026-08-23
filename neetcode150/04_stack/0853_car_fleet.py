"""
=====================================================================
LeetCode 853 : Car Fleet                                      (Medium)
https://leetcode.com/problems/car-fleet/
Category   : Stack (monotonic)
---------------------------------------------------------------------
PROBLEM
    n cars drive to a target mile. Each car starts at `position[i]`
    with `speed[i]` (mph), all moving toward the target. A car NEVER
    passes another: if a faster car catches a slower one AHEAD, it
    slows down and they merge into one FLEET (the fleet keeps the
    speed of the slowest leader). Count the number of fleets that
    arrive at the target.
---------------------------------------------------------------------
INTUITION
    A car at position p reaches the target at time (target − p)/speed.
    Sort cars by position from the target backwards (nearest first).
    The nearest car is its own fleet. Each car BEHIND merges iff its
    arrival time ≤ the time of the fleet in front of it (it would
    catch up before the target). So we walk backwards and keep only
    the arrival times that are STRICTLY GREATER than the last kept
    one — every kept time = one new fleet. A stack stores them.
---------------------------------------------------------------------
APPROACH 1 — Sort + stack of arrival times (BEST)
    Sort (position, speed) pairs by position DESCENDING (nearest to
    the target first). Maintain a stack of arrival times that is
    STRICTLY INCREASING bottom→top. Push t only if t is greater than
    the current top — otherwise the car merges into the fleet ahead.
    Answer = stack size.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Sort + running maximum (no stack)
    Same sort and walk, but the "stack" shrinks to one variable: the
    arrival time of the slowest leader so far (the fleet's time).
    Count a new fleet every time a car's time exceeds it.
    Time  Complexity : O(n log n)   Space Complexity : O(1) extra
---------------------------------------------------------------------
DEEP DIVE — same monotonic invariant again
    The stack of times is MONOTONIC (strictly increasing): pushing a
    smaller/equal time would be pointless because that car merges.
    This is the same "keep only what beats the running extreme"
    pattern as 0084 and 0739 — sorted order turns a geometric chase
    into a linear walk. Float time is exact enough here; merges are
    decided by comparison, and LeetCode tolerates tiny float error.
---------------------------------------------------------------------
REAL LIFE
    • Logistics / truck-platooning simulators: grouping vehicles by
      arrival times at a hub is this exact sweep.
    • Event pipelines: "which events will merge into one batch?"
      (delayed trains, batching API calls) — arrival-time merging.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Tuple

# =====================================================================
# APPROACH 1 : Sort + stack of arrival times (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Count fleets arriving at the target.
    Inputs  : target — mile marker all cars drive toward.
              position — starting mile of each car.
              speed — mph of each car (position[i] pairs with speed[i]).
    Output  : number of distinct fleets that reach the target.
    """

    def carFleet(self, target: int, position: List[int],
                 speed: List[int]) -> int:
        # Pair each car, sorted by position DESCENDING — nearest to
        # the target first (that is the direction fleets form).
        cars = sorted(zip(position, speed), reverse=True)

        # times : arrival times of fleet leaders so far. Values are
        # STRICTLY INCREASING bottom→top (invariant of the walk).
        times: List[float] = []

        for pos, spd in cars:
            # Hours to drive (target − position) miles at `spd` mph.
            t = (target - pos) / spd

            # If this car's arrival time EXCEEDS the fleet in front,
            # it never catches up → it starts its OWN fleet.
            if not times or t > times[-1]:
                times.append(t)
            # Else t ≤ leader time → this car merges: no new fleet,
            # the leader's (slower) time already represents it.

        # Every stack entry is one fleet leader → count = fleets.
        return len(times)


# =====================================================================
# APPROACH 2 : Sort + running maximum (stack replaced by 1 variable)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Count fleets arriving at the target.
    Inputs  : target — mile marker all cars drive toward.
              position — starting mile of each car.
              speed — mph of each car (position[i] pairs with speed[i]).
    Output  : number of distinct fleets that reach the target.
    """

    def carFleet(self, target: int, position: List[int],
                 speed: List[int]) -> int:
        # Same descending sort as approach 1.
        cars = sorted(zip(position, speed), reverse=True)

        # Only the SLOWEST leader time matters for merging decisions —
        # that single value replaces the whole stack.
        slowest: float = 0.0
        fleets = 0

        for pos, spd in cars:
            t = (target - pos) / spd

            # New fleet only when this car cannot catch the current
            # leader; then IT becomes the new (slower) leader.
            if t > slowest:
                fleets += 1
                slowest = t

        return fleets


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Correctness tests ---
    tests = [
        (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 3),   # official example
        (10, [3], [3], 1),                            # single car
        (100, [0, 2, 4], [4, 2, 1], 1),               # all merge
        (100, [0, 2, 4], [4, 2, 3], 2)                # separate arrival
    ]

    all_ok = True
    for target, pos, spd, expect in tests:
        r1 = SolutionOne().carFleet(target, pos, spd)
        r2 = SolutionTwo().carFleet(target, pos, spd)
        ok = r1 == expect and r2 == expect
        if not ok:
            all_ok = False
        print(f"{'PASS' if ok else 'FAIL'} : target={target} n={len(pos)}"
              f"  stack={r1}  maxvar={r2}  expect={expect}")

    # --- Benchmark: 50k random cars ---
    N = 50000
    TARGET = 1000000
    big_pos = [(i * 7919) % TARGET for i in range(N)]
    big_spd = [1 + (i * 104729) % 100 for i in range(N)]

    tracemalloc.start()
    t0 = time.perf_counter()
    rb1 = SolutionOne().carFleet(TARGET, big_pos, big_spd)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t0b = time.perf_counter()
    rb2 = SolutionTwo().carFleet(TARGET, big_pos, big_spd)
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (sort + stack)   : {rb1} fleets  time = {(t1 - t0) * 1e6:.2f} µs"
          f"  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (sort + max var) : {rb2} fleets  time = {(t1b - t0b) * 1e6:.2f} µs"
          f"  peak-mem = {peak_2} bytes")

    print("PASS : all tests" if all_ok else "FAIL : a test was wrong")