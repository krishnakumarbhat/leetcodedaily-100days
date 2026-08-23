"""
=====================================================================
LeetCode 70 : Climbing Stairs                                   (Easy)
https://leetcode.com/problems/climbing-stairs/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    You climb a staircase of `n` steps. Each move takes either 1 step
    or 2 steps. Count the DISTINCT ways to reach the top.
---------------------------------------------------------------------
INTUITION
    The only way to LAND on step i is from step i-1 (one 1-step) or
    from step i-2 (one 2-step). Every path to i extends a path to i-1
    or a path to i-2 → ways(i) = ways(i-1) + ways(i-2) — the Fibonacci
    sequence. Overlapping subproblems (ways(3) is needed by both
    ways(4) and ways(5)) → textbook dynamic programming.
---------------------------------------------------------------------
APPROACH 1 — Bottom-up tabulation with rolling variables (BEST)
    dp[i] = distinct ways to reach step i.
    Recurrence : dp[i] = dp[i-1] + dp[i-2]     dp[0] = dp[1] = 1
    State space : i ∈ [0, n] → n+1 states mapped onto array dp[n+1],
                  filled left→right. Cell i reads only i-1 and i-2.
    Space optimization : only the last TWO values are ever needed →
                  two rolling variables replace the table → O(1).
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Top-down memoized recursion
    f(i) = f(i-1) + f(i-2), memo[i] caches every solved state so the
    naive exponential recursion collapses to O(n) work.
    Trade-off : easier to derive; each call costs a stack frame + memo
    lookup; very deep n risks Python's recursion limit.
    Time  Complexity : O(n)   Space Complexity : O(n) (memo + stack)
---------------------------------------------------------------------
REAL LIFE
    • Rabbit populations (Fibonacci's 1202 breeding model).
    • Grid path counting, tiling counts, branching processes.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : bottom-up with two rolling variables (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Count distinct ways to climb `n` stairs (1 or 2 per move).
    Inputs  : n — number of steps.
    Output  : int — total number of distinct ways.
    """

    def climbStairs(self, n: int) -> int:
        # Rolling window: prev2 = dp[i-2], prev1 = dp[i-1].
        prev2, prev1 = 1, 1   # dp[0] = dp[1] = 1
        for i in range(2, n + 1):
            cur = prev1 + prev2   # dp[i] = dp[i-1] + dp[i-2]
            prev2, prev1 = prev1, cur  # slide the window right
        return prev1  # dp[n]


# =====================================================================
# APPROACH 2 : top-down memoized recursion
# =====================================================================
class SolutionTwo:
    """
    Purpose : Count distinct ways to climb `n` stairs via memoized DFS.
    Inputs  : n — number of steps.
    Output  : int — total number of distinct ways.
    """

    def climbStairs(self, n: int) -> int:
        memo: List[int] = [-1] * (n + 1)   # -1 = state not solved yet

        def f(i: int) -> int:
            # Base case: one way to reach steps 0 and 1.
            if i <= 1:
                return 1
            # Overlapping subproblem already solved → reuse it.
            if memo[i] != -1:
                return memo[i]
            # The recurrence, cached before returning.
            memo[i] = f(i - 1) + f(i - 2)
            return memo[i]

        return f(n)


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (n, expected ways). Both solutions must match.
    tests: List[Tuple[int, int]] = [
        (2, 2),    # 1+1, 2
        (3, 3),    # 1+1+1, 1+2, 2+1
        (10, 89),  # Fibonacci: F(11) with F(1)=F(2)=1 → 89
    ]

    total_us_1 = total_us_2 = 0.0
    total_kb_1 = total_kb_2 = 0
    all_pass = True

    for n, expected in tests:
        # --- Approach 1: perf_counter for time, tracemalloc for RAM ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().climbStairs(n)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_1 += (t1 - t0) * 1e6
        total_kb_1 += peak1 // 1024

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().climbStairs(n)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_2 += (t1b - t0b) * 1e6
        total_kb_2 += peak2 // 1024

        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"n={n:2} A1={r1:3} A2={r2:3} expected={expected:3} "
              f"{'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches match every expected output."
          if all_pass
          else "FAIL : at least one answer is wrong.")