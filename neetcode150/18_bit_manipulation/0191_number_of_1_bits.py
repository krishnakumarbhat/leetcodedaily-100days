"""
=====================================================================
LeetCode 191 : Number of 1 Bits                                   (Easy)
https://leetcode.com/problems/number-of-1-bits/
Category   : Bit Manipulation
---------------------------------------------------------------------
PROBLEM
    Given an unsigned 32-bit integer, return the number of '1' bits
    in its binary representation (the Hamming weight / popcount).
    Example: 11 = 1011₂ → 3.
---------------------------------------------------------------------
INTUITION
    Counting needs a way to "remove one set bit per step". The trick
    x & (x - 1) clears exactly the LOWEST set bit of x — repeated
    application makes x zero in exactly popcount(x) steps, so the
    round count IS the answer. No iteration is wasted on zeros.
---------------------------------------------------------------------
APPROACH 1 — Kernighan's algorithm (BEST)
    count = 0; while n: n &= n - 1; count += 1. One round per SET
    bit. Derivation of x & (x - 1):
        x     = ...1 0 0 0   (lowest 1-bit at position k)
        x - 1 = ...0 1 1 1   (borrow: bit k → 0, below → all 1s)
        x & (x-1) = ...1·1 ··· 0 ··· 0·1 = x minus its lowest 1-bit
    Time  Complexity : O(popcount) ≤ O(32) = O(1)
    Space Complexity : O(1)
    PYTHON NOTE: n is unbounded — without a 32-bit mask, Kernighan
    also strips set bits above bit 31 (fine: they aren't in the
    input's 32-bit lane) but the count never exceeds 32 either way.
---------------------------------------------------------------------
APPROACH 2 — Scan all 32 bit positions
    count = 0; for i in range(32): count += n & 1; n >>= 1.
    Checks every position including zeros — simple, 32 fixed rounds.
    Time  Complexity : O(32) = O(1)   Space Complexity : O(1)
---------------------------------------------------------------------
REAL LIFE
    • Parity bits & error detection: popcount parity of a byte decides
      the stored parity bit in ECC memory and serial links.
    • Population statistics: IPv4 subnet masks, Hamming distance in
      similarity engines (Bitcoin mining chips count ones too).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

MASK32 = 0xFFFFFFFF  # emulates the 32-bit hardware lane in Python


# =====================================================================
# APPROACH 1 : Kernighan — one iteration per SET bit (best)
# =====================================================================
class Solution_1:
    """
    Purpose : Count the set bits (Hamming weight) of a 32-bit value.
    Inputs  : n — the value to count bits of.
    Output  : int — the number of 1-bits in n (0..32).
    """

    def hammingWeight(self, n: int) -> int:
        count = 0

        # Each round wipes exactly ONE set bit (the lowest one), so
        # the loop runs popcount(n) times — zero bits cost nothing.
        # The mask keeps Python's unbounded int inside the 32-bit lane
        # so the loop provably terminates for any input.
        n &= MASK32
        while n != 0:
            n &= n - 1   # clears the lowest set bit (see deep dive)
            count += 1
        return count


# =====================================================================
# APPROACH 2 : Scan all 32 bit positions
# =====================================================================
class Solution_2:
    """
    Purpose : Count the set bits by examining every one of the 32
              positions, including the zero bits.
    Inputs  : n — the value to count bits of.
    Output  : int — the number of 1-bits in n (0..32).
    """

    def hammingWeight(self, n: int) -> int:
        count = 0

        # Fixed 32 rounds: pull the lowest bit off, add it, shift.
        # Masking after the shift keeps the emulated lane 32 bits wide.
        for _ in range(32):
            count += n & 1
            n = (n >> 1) & MASK32
        return count


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test table: {input, expected popcount} — official example,
    # a sparse value, and the all-ones boundary.
    tests: List[Tuple[int, int]] = [
        (11, 3),          # 1011₂ → three 1-bits
        (128, 1),         # 10000000₂ → one 1-bit
        (0xFFFFFFFF, 32), # all ones → thirty-two 1-bits
    ]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok_1 = True
    for inp, exp in tests:
        got = Solution_1().hammingWeight(inp)
        pass_ = got == exp
        ok_1 = ok_1 and pass_
        print(f"  A1 hammingWeight({inp}) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok_2 = True
    for inp, exp in tests:
        got = Solution_2().hammingWeight(inp)
        pass_ = got == exp
        ok_2 = ok_2 and pass_
        print(f"  A2 hammingWeight({inp}) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Summary lines: time in µs, peak memory in KB.
    print(f"Approach 1 (Kernighan)      : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.2f} KB")
    print(f"Approach 2 (32-bit scan)    : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.2f} KB")

    print("PASS : both approaches count every test value correctly."
          if ok_1 and ok_2
          else "FAIL : at least one test mismatched.")
