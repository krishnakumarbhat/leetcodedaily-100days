"""
=====================================================================
LeetCode 268 : Missing Number                                     (Easy)
https://leetcode.com/problems/missing-number/
Category   : Bit Manipulation
---------------------------------------------------------------------
PROBLEM
    Given an array `nums` containing n DISTINCT numbers taken from
    0, 1, 2, ..., n, return the ONE number that is missing from the
    range. Example: [3,0,1] → 2. Must run in O(n) time and O(1)
    extra space.
---------------------------------------------------------------------
INTUITION
    The array plus the missing value forms the full set {0..n}. Two
    algebraic lenses see the hole instantly:
      • SUM: the full range sums to n(n+1)/2; subtract the array's
        sum — the difference IS the missing number.
      • XOR: xor every index with every value. Every present
        (index, value) pair cancels (x ^ x = 0, the 0136 trick),
        leaving the index that never found a matching value.
---------------------------------------------------------------------
APPROACH 1 — XOR of all indices and values (BEST)
    acc = n; for i: acc ^= i ^ nums[i]. Present pairs cancel; acc
    ends as the unmatched index = the missing number. No overflow.
    Time  Complexity : O(n)   Space Complexity : O(1)
    WHY it works: acc = n ^ 0 ^ nums[0] ^ 1 ^ nums[1] ^ ...
    Every present value v meets its own index v and cancels; the
    index m whose value is absent survives alone. Same machinery
    as 0136 Single Number — same proof, new hat.
---------------------------------------------------------------------
APPROACH 2 — Sum formula
    expected = n(n+1)/2; return expected − sum(nums).
    Time  Complexity : O(n)   Space Complexity : O(1)
    WARNING: n(n+1)/2 grows quadratically — in C++ it overflows
    int32 for n > 65535 (Python's unbounded ints dodge that, which
    is exactly why the XOR variant is the portable winner).
---------------------------------------------------------------------
REAL LIFE
    • Database consistency: detecting a missing sequential key (an
      auto-increment column with a deleted row) is sum-difference
      checking on a million-row table.
    • Network packet sequencing: missing packet numbers in a stream
      are found with the same range-difference identity.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : XOR of all indices and values — pairs cancel (best)
# =====================================================================
class Solution_1:
    """
    Purpose : Find the single value missing from 0..n in `nums`.
    Inputs  : nums — n distinct integers from the range 0..n.
    Output  : int — the missing value.
    """

    def missingNumber(self, nums: List[int]) -> int:
        # Start with n: the only index with no counterpart a priori
        # (the array spans indices 0..n-1).
        acc = len(nums)

        # Pair every index with the value living at it. Present pairs
        # cancel to 0; the missing index never finds its partner.
        for i, num in enumerate(nums):
            acc ^= i ^ num
        return acc


# =====================================================================
# APPROACH 2 : Sum formula — full range minus the array
# =====================================================================
class Solution_2:
    """
    Purpose : Find the missing value using the arithmetic-series
              formula (n(n+1)/2 minus the array sum).
    Inputs  : nums — n distinct integers from the range 0..n.
    Output  : int — the missing value.
    """

    def missingNumber(self, nums: List[int]) -> int:
        # Full range {0..n} sums to n(n+1)/2. Python ints are
        # unbounded, so the quadratic growth never overflows here —
        # but note the C++ int32 equivalent would break at n > 65535.
        n = len(nums)
        expected = n * (n + 1) // 2

        # The difference between what SHOULD be there and what IS
        # there is exactly the missing value.
        return expected - sum(nums)


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test table: {array, expected missing value} — official examples
    # plus a large-range case where the sum grows quadratically.
    tests: List[Tuple[List[int], int]] = [
        ([3, 0, 1], 2),
        ([0, 1], 2),
        ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
        (list(range(0, 100001))[:77777] + list(range(77778, 100001)), 77777),
    ]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok_1 = True
    for arr, exp in tests:
        got = Solution_1().missingNumber(arr)
        pass_ = got == exp
        ok_1 = ok_1 and pass_
        print(f"  A1 missingNumber({len(arr)} elems) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok_2 = True
    for arr, exp in tests:
        got = Solution_2().missingNumber(arr)
        pass_ = got == exp
        ok_2 = ok_2 and pass_
        print(f"  A2 missingNumber({len(arr)} elems) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Summary lines: time in µs, peak memory in KB.
    print(f"Approach 1 (XOR pairs)       : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.2f} KB")
    print(f"Approach 2 (sum formula)     : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.2f} KB")

    print("PASS : both approaches find every missing number."
          if ok_1 and ok_2
          else "FAIL : at least one test mismatched.")
