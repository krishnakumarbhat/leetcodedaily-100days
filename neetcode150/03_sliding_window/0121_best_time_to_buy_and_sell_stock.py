"""
=====================================================================
LeetCode 121 : Best Time to Buy and Sell Stock                  (Easy)
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
Category   : Sliding Window
---------------------------------------------------------------------
PROBLEM
    Given `prices` where prices[i] is the price on day i, choose ONE
    day to buy and ONE LATER day to sell, maximizing profit
    (sell − buy). Return the max profit, or 0 if none exists.
---------------------------------------------------------------------
INTUITION
    The constraint is ORDER: buy index < sell index. This is a
    degenerate sliding window: as the "sell" pointer r advances,
    the best "buy" pointer is just the index of the minimum price
    seen so far. Profit(day r) = prices[r] − min(prices[0..r−1]).
    The answer is the max over all r — no backtracking needed.
---------------------------------------------------------------------
APPROACH 1 — Brute force (all buy/sell pairs)
    For every buy day i, try every later sell day j and take the
    best difference. Correct but explores every pair.
    Time  Complexity : O(n²)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — One pass, track the minimum price (BEST)
    Walk the array once. Keep min_price = cheapest day seen so far
    (the optimal "buy" for any future "sell"). At each day, the
    best profit selling today is prices[i] − min_price.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — why this is a sliding window with O(1) state
    No hash map needed: the window's summary is exactly ONE integer
    — the minimum inside [0 .. r−1]. It never needs to shrink
    because the minimum is monotone non-increasing:
        min([0..r]) = min(min([0..r−1]), prices[r])
    The same "running best" trick appears in Kadane's algorithm
    (maximum subarray) — a single pass variable that absorbs each
    new element in O(1). This is the simplest possible window:
    left edge = argmin so far, right edge = current day.
---------------------------------------------------------------------
REAL LIFE
    • Any single-slot optimization over a time series: cheapest
      restock day vs. best sale day, min-cost inventory pricing.
    • Stock/currency/crypto trackers compute exactly this metric
      per symbol on every tick — O(1) memory per symbol.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : Brute force — try every (buy, sell) pair
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the maximum profit achievable by buying on one
              day and selling on a strictly later day.
    Inputs  : prices — daily stock prices, oldest first.
    Output  : int — best profit, or 0 if no profitable pair exists.
    """

    def maxProfit(self, prices: List[int]) -> int:
        best: int = 0  # 0 = "no trade" baseline; profit may be negative

        # Buy day i: the outer loop fixes the purchase.
        for i in range(len(prices)):
            # Sell day j: must be AFTER i — the order constraint.
            for j in range(i + 1, len(prices)):
                # Candidate profit for this single pair of days.
                best = max(best, prices[j] - prices[i])
        return best


# =====================================================================
# APPROACH 2 : One pass — track the minimum price seen so far
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the maximum profit achievable by buying on one
              day and selling on a strictly later day.
    Inputs  : prices — daily stock prices, oldest first.
    Output  : int — best profit, or 0 if no profitable pair exists.
    """

    def maxProfit(self, prices: List[int]) -> int:
        min_price: float = float("inf")  # cheapest day visited so far
        best: int = 0                    # best profit discovered so far

        for price in prices:
            # A new candidate buy day: if cheaper than everything
            # before, it becomes the new left edge of the "window".
            min_price = min(min_price, price)
            # Selling TODAY against the best buy so far — the only
            # profit worth considering for this sell day.
            best = max(best, price - int(min_price))
        return best


# =====================================================================
# BENCHMARK — run both approaches on 3 tests + a longer series,
# compare time and peak memory (tracemalloc), print PASS/FAIL.
# =====================================================================
if __name__ == "__main__":
    tests: List[Tuple[List[int], int]] = [
        ([7, 1, 5, 3, 6, 4], 5),  # buy 1 → sell 6 (profit 5)
        ([7, 6, 4, 3, 1], 0),     # strictly falling → never buy
        ([2, 4, 1], 2),           # buy 2 → sell 4 (profit 2)
    ]

    all_pass = True
    for prices, expected in tests:
        r1 = SolutionOne().maxProfit(prices)
        r2 = SolutionTwo().maxProfit(prices)
        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'} prices={prices} expected={expected}  brute={r1}  onePass={r2}")

    # Longer pseudo-random series (zig-zag) so both loops do real work.
    bench: List[int] = [(i * 37) % 1000 if i % 2 == 0 else 1000 - (i * 53) % 1000
                        for i in range(2000)]

    # --- Approach 1: time + peak memory ---
    tracemalloc.start()
    t0 = time.perf_counter()
    b1 = SolutionOne().maxProfit(bench)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t2 = time.perf_counter()
    b2 = SolutionTwo().maxProfit(bench)
    t3 = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (brute force)  : result={b1}  time={(t1 - t0) * 1e6:.2f} µs  peak-mem={peak_1} bytes")
    print(f"Approach 2 (one pass)     : result={b2}  time={(t3 - t2) * 1e6:.2f} µs  peak-mem={peak_2} bytes")

    # Brute force is the ground truth — the O(n) pass must match it.
    all_pass = all_pass and (b1 == b2)
    print("PASS : all test cases and benchmark agree." if all_pass
          else "FAIL : at least one answer is wrong.")
