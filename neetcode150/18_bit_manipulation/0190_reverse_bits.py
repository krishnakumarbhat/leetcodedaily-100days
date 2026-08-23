"""
=====================================================================
LeetCode 190 : Reverse Bits                                       (Easy)
https://leetcode.com/problems/reverse-bits/
Category   : Bit Manipulation
---------------------------------------------------------------------
PROBLEM
    Reverse the bits of a given 32-bit unsigned integer. Bit 31 of
    the input becomes bit 0 of the output, bit 30 becomes bit 1, etc.
    Example: 43261596 (00000010100101000001111010011100)
          →  964176192 (00111001011110000010100101000000).
---------------------------------------------------------------------
INTUITION
    Bit reversal mirrors decimal digit reversal: take one bit off the
    right end of the input and place it onto the LEFT end of an
    accumulator, 32 times. Faster: divide & conquer — swap 16-bit
    halves, 8-bit quarters, 4-bit blocks, 2-bit blocks, then adjacent
    bits: five masked swaps, each halving the block size.
---------------------------------------------------------------------
APPROACH 1 — Shift-and-OR assembly, 32 iterations (clear)
    result = 0; 32 times: result = (result << 1) | (n & 1); n >>= 1.
    The input's bits are consumed low → high and emitted high → low.
    Time  Complexity : O(1) — exactly 32 fixed iterations.
    Space Complexity : O(1)
    PYTHON NOTE: ints are unbounded, so a plain `n >>= 1` never
    terminates the loop — mask with `n &= 0xFFFFFFFF` (or work on an
    int and clamp at the end) to emulate the 32-bit hardware lane.
---------------------------------------------------------------------
APPROACH 2 — 5 masked block swaps (divide & conquer)
    Swap halves, then 8-bit quarters, 4-bit blocks, 2-bit blocks,
    adjacent bits — five ops, no loop. Masks isolate every other
    block of the current size:
        0xFF00FF00, 0xF0F0F0F0, 0xCCCCCCCC, 0xAAAAAAAA (and their
        bitwise complements) for sizes 8, 4, 2, 1.
    Time  Complexity : O(1) — FIVE operations.
    Space Complexity : O(1)
---------------------------------------------------------------------
REAL LIFE
    • FFT kernels (FFTW, DSP chips) permute frequency bins with a
      bit-reversal pass before butterflies — the same core routine.
    • Endian conversion, image pixel bit-plane flipping, and
      hash/PRNG finalization mixers (e.g. murmur3's bit reverse).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

MASK32 = 0xFFFFFFFF  # emulates the 32-bit hardware lane in Python


# =====================================================================
# APPROACH 1 : Shift-and-OR assembly — 32 iterations (clear)
# =====================================================================
class Solution_1:
    """
    Purpose : Reverse all 32 bits of an unsigned integer.
    Inputs  : n — the value whose bits must be mirrored.
    Output  : int — the bit-reversed value (unsigned 32-bit range).
    """

    def reverseBits(self, n: int) -> int:
        # Accumulator that the input's bits are poured into, one per
        # round, each arriving at the top of the pile.
        result = 0

        # Exactly 32 rounds — one per bit of the 32-bit lane.
        for _ in range(32):
            # Shift the pile left (making room at bit 0) and OR in the
            # input's current lowest bit.
            result = (result << 1) | (n & 1)
            # Drop the consumed bit AND re-mask: without the mask the
            # right-shift of an unbounded Python int never empties it,
            # and the loop would spin forever past bit 31.
            n = (n >> 1) & MASK32

        # Clamp once: the shift-and-OR could otherwise carry beyond
        # bit 31 for inputs whose top bit was set.
        return result & MASK32


# =====================================================================
# APPROACH 2 : Five masked block swaps (divide & conquer)
# =====================================================================
class Solution_2:
    """
    Purpose : Reverse all 32 bits using 5 halving block swaps.
    Inputs  : n — the value whose bits must be mirrored.
    Output  : int — the bit-reversed value (unsigned 32-bit range).
    """

    def reverseBits(self, n: int) -> int:
        # Mask to the 32-bit lane first so every later op is clean.
        n &= MASK32

        # Stage 1: mirror the two 16-bit halves.
        #     x >> 16 moves the HIGH half down; x << 16 moves the LOW
        #     half up. No mask needed — the halves are exact.
        n = ((n >> 16) | (n << 16)) & MASK32

        # Stage 2: mirror the four 8-bit blocks. 0xFF00FF00 keeps the
        # high byte of each 16-bit pair; its complement keeps the rest.
        n = (((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)) & MASK32

        # Stage 3: mirror the eight 4-bit nibbles.
        n = (((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)) & MASK32

        # Stage 4: mirror the sixteen 2-bit blocks.
        # 0xCCCCCCCC = 1100 1100 ... (every other 2-bit block).
        n = (((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)) & MASK32

        # Stage 5: swap adjacent bits — the finest granularity.
        # 0xAAAAAAAA = 1010 1010 ... (every other single bit).
        n = (((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)) & MASK32

        return n


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test table: {input, expected reversal} — the official example
    # plus its boundary neighbours (0 and all-ones).
    tests: List[Tuple[int, int]] = [
        (43261596, 964176192),
        (0, 0),
        (0xFFFFFFFF, 0xFFFFFFFF),
    ]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok_1 = True
    for inp, exp in tests:
        got = Solution_1().reverseBits(inp)
        pass_ = got == exp
        ok_1 = ok_1 and pass_
        print(f"  A1 reverseBits({inp}) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok_2 = True
    for inp, exp in tests:
        got = Solution_2().reverseBits(inp)
        pass_ = got == exp
        ok_2 = ok_2 and pass_
        print(f"  A2 reverseBits({inp}) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Summary lines: time in µs, peak memory in KB.
    print(f"Approach 1 (shift-and-OR ×32)  : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.2f} KB")
    print(f"Approach 2 (5 block swaps)     : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.2f} KB")

    print("PASS : both approaches reverse every test value correctly."
          if ok_1 and ok_2
          else "FAIL : at least one test mismatched.")
