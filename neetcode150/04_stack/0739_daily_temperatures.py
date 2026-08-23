"""
=====================================================================
LeetCode 739 : Daily Temperatures                           (Medium)
https://leetcode.com/problems/daily-temperatures/
Category   : Stack (monotonic)
---------------------------------------------------------------------
PROBLEM
    Given an array of daily temperatures, return an answer array where
    answer[i] = the number of days you must wait for a WARMER day, or
    0 if no warmer day ever follows.
---------------------------------------------------------------------
INTUITION
    For every day i we ask "when does the next strictly-greater value
    appear?" Walking left→right, while temperatures only cool down we
    cannot answer any day yet — their answers are still pending. The
    moment a warmer day arrives, ALL cooler days behind it get their
    answers resolved at once. Pending days form a stack; the first
    pending day is the most recent cooler one — LIFO again.
---------------------------------------------------------------------
APPROACH 1 — Monotonic decreasing stack (BEST)
    Invariant: stack holds indices whose temperatures are STRICTLY
    DECREASING from bottom to top. For each day i: while the stack is
    non-empty and temperatures[i] > temperatures[stack[-1]], the top
    index has found its first warmer day → answer = i − top. Then
    push i. Every index is pushed and popped exactly once.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Brute force (contrast)
    For each day scan forward until a warmer day is found.
    Time  Complexity : O(n²)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — the monotonic stack invariant
    This is the "next greater element" family (0084 uses the mirrored
    "previous smaller", 0853 the same ordering trick on times). The
    invariant "stack holds indices in decreasing temperature order"
    is re-established before every push: pop WHILE the top is cooler,
    resolve its answer, then push. Because each index lives on the
    stack for a single contiguous period, total pops = total pushes
    = n → the sweep is linear. Same pattern, three problems.
---------------------------------------------------------------------
REAL LIFE
    • "How long until this request gets served?" — waiting-time
      distributions in queues (support tickets, print jobs) are the
      same next-greater computation: each pending item waits until a
      "hotter" event appears.
    • Stock/price analytics: days until a higher close = this exact
      monotonic sweep, run on every ticker in your screener.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Monotonic decreasing stack (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Days until the next warmer day, per input day.
    Inputs  : temperatures — daily temperatures in order.
    Output  : List where out[i] is the wait (0 = never warmer).
    """

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)

        # answer : one slot per day, default 0 (never warmer).
        answer = [0] * n

        # st : indices of days whose warmer day is still pending;
        # temperatures strictly DECREASING from bottom to top.
        st: List[int] = []

        # Single left→right pass — the whole O(n) work.
        for i, temp in enumerate(temperatures):

            # Day i is warmer than the pending top → the top's wait is
            # over: its next warmer day is EXACTLY day i.
            while st and temperatures[st[-1]] < temp:

                # Day count between the pending day and day i.
                answer[st[-1]] = i - st[-1]
                st.pop()   # resolved — remove from the pending stack

            # Day i itself is now pending (nothing warmer seen yet).
            st.append(i)

        return answer


# =====================================================================
# APPROACH 2 : Brute force (contrast)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Days until the next warmer day, per input day.
    Inputs  : temperatures — daily temperatures in order.
    Output  : List where out[i] is the wait (0 = never warmer).
    """

    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n

        # For every day, scan forward until a strictly warmer day.
        for i in range(n):
            for j in range(i + 1, n):

                # First warmer day found → distance is the wait.
                if temperatures[j] > temperatures[i]:
                    answer[i] = j - i
                    break   # stop scanning this i
            # No warmer day found → answer[i] stays 0.

        return answer


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Correctness tests ---
    tests = [
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),   # always warmer
        ([90, 80, 70, 60], [0, 0, 0, 0])    # monotone cooling
    ]

    all_ok = True
    for temps, expect in tests:
        r1 = SolutionOne().dailyTemperatures(temps)
        r2 = SolutionTwo().dailyTemperatures(temps)
        ok = r1 == expect and r2 == expect
        if not ok:
            all_ok = False
        print(f"{'PASS' if ok else 'FAIL'} : {len(temps)} days"
              f"  monotonic={r1}  brute={r2}")

    # --- Benchmark: descending ramp — worst case for brute force ---
    # (8k days: brute force is O(n²) in pure Python — keep it modest)
    big = list(range(8000, 0, -1))

    tracemalloc.start()
    t0 = time.perf_counter()
    rb1 = SolutionOne().dailyTemperatures(big)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t0b = time.perf_counter()
    rb2 = SolutionTwo().dailyTemperatures(big)
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (monotonic stack) : {rb1[0]}…  time = {(t1 - t0) * 1e6:.2f} µs"
          f"  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (brute force)     : {rb2[0]}…  time = {(t1b - t0b) * 1e6:.2f} µs"
          f"  peak-mem = {peak_2} bytes")

    print("PASS : all tests" if all_ok else "FAIL : a test was wrong")