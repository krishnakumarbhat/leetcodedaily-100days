"""
=====================================================================
LeetCode 322 : Coin Change                                       (Medium)
https://leetcode.com/problems/coin-change/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    Given coin denominations `coins` (unlimited supply of each) and an
    amount, return the MINIMUM number of coins needed to make that
    amount, or -1 if it is impossible.
---------------------------------------------------------------------
INTUITION
    To make amount X, the LAST coin we add is some coin c; before it
    we must have made amount X-c optimally. So the answer for X is
    1 + min over coins of (answer for X - c) → overlapping subproblems:
    the same amounts reappear from many different coin paths.
    This is the UNBOUNDED KNAPSACK pattern (min version).
---------------------------------------------------------------------
APPROACH 1 — Bottom-up tabulation (BEST)
    dp[x] = min coins to make amount x.
    Recurrence : dp[x] = min( dp[x - c] + 1 ) over coins c ≤ x
                 dp[0] = 0, dp[x] = +∞ until reached
    State space : x ∈ [0, amount] → amount+1 states on array dp[],
                  filled left→right. Cell x reads every dp[x-c] → the
                  whole prefix table must stay (no rolling shortcut).
    Time  Complexity : O(amount × n_coins)   Space : O(amount)
---------------------------------------------------------------------
APPROACH 2 — Top-down memoized recursion
    f(x) = min coins for x; branch over each coin, cache f(x).
    Trade-off : explores only amounts actually reachable; recursion
    depth ≤ amount/cheapest-coin; memo is a full amount-sized array.
    Time  Complexity : O(amount × n_coins)   Space : O(amount)
---------------------------------------------------------------------
REAL LIFE
    • Currency machines / vending change dispensers.
    • Resource-allocation and parcel-fill optimisations (min parts).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

INF = 10**9  # sentinel for "unreachable" in DP tables


# =====================================================================
# APPROACH 1 : bottom-up tabulation
# =====================================================================
class SolutionOne:
    """
    Purpose : Minimum coins to make `amount` with unlimited `coins`.
    Inputs  : coins  — available denominations.
              amount — target sum.
    Output  : int — min coins, or -1 when impossible.
    """

    def coinChange(self, coins: List[int], amount: int) -> int:
        # dp[x] = min coins for x; INF marks unreachable amounts.
        dp: List[int] = [INF] * (amount + 1)
        dp[0] = 0  # zero coins make zero amount
        for x in range(1, amount + 1):
            for c in coins:
                if c <= x and dp[x - c] != INF:
                    dp[x] = min(dp[x], dp[x - c] + 1)
        return dp[amount] if dp[amount] != INF else -1


# =====================================================================
# APPROACH 2 : top-down memoized recursion
# =====================================================================
class SolutionTwo:
    """
    Purpose : Minimum coins to make `amount` with unlimited `coins`.
    Inputs  : coins  — available denominations.
              amount — target sum.
    Output  : int — min coins, or -1 when impossible.
    """

    def coinChange(self, coins: List[int], amount: int) -> int:
        memo: List[int] = [-2] * (amount + 1)  # -2 = unknown, -1 = impossible
        memo[0] = 0

        def f(x: int) -> int:
            if x < 0:
                return INF                # overshot → not a valid path
            if memo[x] != -2:
                return memo[x]            # overlapping subproblem → reuse
            best = INF
            for c in coins:
                best = min(best, f(x - c) + 1)   # add one coin c
            memo[x] = best                # cache before returning
            return best

        ans = f(amount)
        return -1 if ans >= INF else ans


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (coins, amount, expected). Both solutions must match.
    tests: List[Tuple[List[int], int, int]] = [
        ([1, 2, 5], 11, 3),   # 5+5+1
        ([2], 3, -1),         # odd amount, even coins only → impossible
        ([1], 0, 0),          # zero amount needs zero coins
    ]

    total_us_1 = total_us_2 = 0.0
    total_kb_1 = total_kb_2 = 0
    all_pass = True

    for coins, amount, expected in tests:
        # --- Approach 1: perf_counter for time, tracemalloc for RAM ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().coinChange(coins, amount)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_1 += (t1 - t0) * 1e6
        total_kb_1 += peak1 // 1024

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().coinChange(coins, amount)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_2 += (t1b - t0b) * 1e6
        total_kb_2 += peak2 // 1024

        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"coins={str(coins):12} amount={amount:3} A1={r1:3} A2={r2:3} "
              f"expected={expected:3} {'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches match every expected output."
          if all_pass
          else "FAIL : at least one answer is wrong.")