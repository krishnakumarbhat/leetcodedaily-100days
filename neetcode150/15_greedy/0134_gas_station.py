"""
=====================================================================
LeetCode 134 : Gas Station                                     (Medium)
https://leetcode.com/problems/gas-station/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    n gas stations in a circle; from i you gain gas[i] and the ride
    to i+1 costs cost[i]. Starting with an EMPTY tank, find the start
    index that allows a full circle, else -1. The answer is unique
    if it exists.
---------------------------------------------------------------------
INTUITION
    net[i] = gas[i] - cost[i]. Feasible circle ⟺ total sum ≥ 0.
    While walking with a running `tank`, the moment tank < 0 at j,
    NO station inside [start, j] can be a valid start: each of them
    carries a prefix at least as bad as the full negative window.
    Reset start = j+1. One reset per dead window → O(n) total.
---------------------------------------------------------------------
APPROACH 1 — Total sum + single-pass candidate (BEST)
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Brute force O(n²)
    Try every start and simulate n stops; the quadratic retry wastes
    the prefix-dead insight.
    Time  Complexity : O(n²)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — why discarding a negative prefix is provably safe
    Let P < 0 be the net-sum of [start, j]. For any s in that window
    the tank at j when starting at s is (P − prefix[start..s)) ≤ P < 0
    — every inner candidate dies at or before j. The remaining tail
    [j+1..] is identical for all candidates, so the whole window is
    dead → resetting to j+1 loses nothing. The total ≥ 0 guarantee
    ensures a live window always survives to the end.
---------------------------------------------------------------------
REAL LIFE
    • Bus / drone / EV route planning: can a fleet complete a
      circular route given per-stop charge and consumption?
    • Circular conveyor/line balancing: buffer levels in ring
      manufacturing lines.
    • RAID/disk rotation scheduling: balancing workloads around a
      cyclic timeline.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Total sum + single-pass candidate reset (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Find the unique start station that completes a circle.
    Inputs  : gas  — list of ints, gas[i] gained at station i.
              cost — list of ints, cost[i] spent riding i → i+1.
    Output  : int — valid start index, or -1 if none exists.
    """

    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total = 0   # Σ net — is the WHOLE circle feasible?
        tank = 0    # running fuel from the current candidate start
        start = 0   # current best candidate

        for i in range(len(gas)):
            net = gas[i] - cost[i]
            total += net     # global balance
            tank += net      # local balance since `start`

            if tank < 0:
                # Prefix [start..i] is net-negative → every station in
                # that window dies (see DEEP DIVE) → reset window.
                start = i + 1
                tank = 0     # fresh candidate starts with empty tank

        return start if total >= 0 else -1

# =====================================================================
# APPROACH 2 : Brute force — simulate every candidate (O(n²))
# =====================================================================
class SolutionTwo:
    """
    Purpose : Find the unique start station that completes a circle.
    Inputs  : gas  — list of ints, gas[i] gained at station i.
              cost — list of ints, cost[i] spent riding i → i+1.
    Output  : int — valid start index, or -1 if none exists.
    """

    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)

        # Try every station as start — the naive quadratic scan.
        for start in range(n):
            tank = 0
            ok = True
            for step in range(n):
                i = (start + step) % n   # wrap around the circle
                tank += gas[i] - cost[i]
                if tank < 0:             # died mid-trip → try next start
                    ok = False
                    break
            if ok:
                return start             # survived all n stops
        return -1                        # no station works


# =====================================================================
# BENCHMARK — both approaches, time + peak memory per approach
# =====================================================================
if __name__ == "__main__":
    # Official examples + impossible circle + single-station edge.
    gas_tests: List[List[int]] = [
        [1, 2, 3, 4, 5],    # → 3
        [2, 3, 4],          # → -1
        [5],                # → 0
        [1, 2, 3, 4, 5, 6], # → 3
    ]
    cost_tests: List[List[int]] = [
        [3, 4, 5, 1, 2],    # → 3
        [3, 4, 3],          # → -1
        [4],                # → 0
        [6, 5, 4, 3, 2, 1], # → 3 (unique start per problem guarantee)
    ]
    expected = [3, -1, 0, 3]

    def run_all(solve) -> tuple[bool, float, int]:
        """Time one solver over every test; return (allPass, µs, peakBytes)."""
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = all(solve(g, c) == e for g, c, e in zip(gas_tests, cost_tests, expected))
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return ok, (t1 - t0) * 1e6, peak

    ok1, us1, peak1 = run_all(lambda g, c: SolutionOne().canCompleteCircuit(g, c))
    ok2, us2, peak2 = run_all(lambda g, c: SolutionTwo().canCompleteCircuit(g, c))

    print(f"Approach 1 (prefix reset)  : {'PASS' if ok1 else 'FAIL'}  time = {us1:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (brute force)   : {'PASS' if ok2 else 'FAIL'}  time = {us2:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches find the correct start station."
          if ok1 and ok2
          else "FAIL : at least one approach is wrong.")
