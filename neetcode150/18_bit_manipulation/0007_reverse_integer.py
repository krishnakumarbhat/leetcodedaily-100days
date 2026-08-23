"""
=====================================================================
LeetCode 7  : Reverse Integer                                    (Medium)
https://leetcode.com/problems/reverse-integer/
Category   : Bit Manipulation
---------------------------------------------------------------------
PROBLEM
    Given a signed 32-bit integer `x`, return `x` with its decimal
    digits reversed. If reversing would fall OUTSIDE the signed
    32-bit range [-2^31, 2^31 - 1], return 0.
    Examples: 123 → 321     -123 → -321     1534236469 → 0 (overflow)
---------------------------------------------------------------------
INTUITION
    Pop the last digit (x % 10) and push it onto the result
    (result = result * 10 + digit) — writing the number backwards
    by hand. In C++/Java the multiply can overflow, so guards run
    BEFORE the multiplication. Python's ints are UNBOUNDED, so it
    never overflows naturally — the guard is an EMULATION of the
    int32 hardware contract, which is exactly what the problem tests.
---------------------------------------------------------------------
APPROACH 1 — Pop & push with pre-multiply guards (BEST)
    Check `result > INT_MAX // 10` before growing (any growth
    overflows) or `result == INT_MAX // 10 and digit > 7` (only the
    largest digit overflows at the exact boundary). Mirror on the
    negative side with -214748364 and guard digit -8 — two's
    complement gives the negative range one extra unit, so the two
    guard digits DIFFER (7 vs -8).
    Time  Complexity : O(log10 |x|)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Unbounded accumulation, single final range check
    Exploit Python's big ints: accumulate WITHOUT guards (nothing can
    overflow), then clamp once at the end: if the reversal escapes
    [-2^31, 2^31 - 1] → 0. Same loop, fewer branches, and it makes
    the "mask to 32 bits" idea explicit: the hardware does this
    clamping silently, so the algorithm must do it deliberately.
    Time  Complexity : O(log10 |x|)   Space Complexity : O(1)
---------------------------------------------------------------------
REAL LIFE
    • Integer parsing in compilers and DB wire protocols: every
      atoi/strtol implementation carries exactly this pre-multiply
      guard so a hostile 20-digit string cannot wrap the value.
    • Network byte order (big-endian) conversion when reversing
      digit/byte streams between CPU architectures.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

# 32-bit signed range boundaries (Python emulates these explicitly).
INT32_MAX = 2 ** 31 - 1
INT32_MIN = -2 ** 31


# =====================================================================
# APPROACH 1 : Pop & push with pre-multiply overflow guards (best)
# =====================================================================
class Solution_1:
    """
    Purpose : Reverse the decimal digits of a 32-bit signed int,
              returning 0 if the reversal leaves the int32 range.
    Inputs  : x — the integer whose digits must be reversed.
    Output  : int — reversed digits, or 0 on overflow.
    """

    def reverse(self, x: int) -> int:
        neg = x < 0
        n = -x if neg else x            # work on magnitude: // truncates
        result = 0

        # Peel digits off the right until nothing remains.
        while n != 0:
            digit = n % 10
            n //= 10

            # Positive guard: INT32_MAX // 10 = 214748364, guard digit 7.
            # If result already exceeds the quotient, ANY append grows
            # past the boundary; exactly at the quotient only digit > 7
            # overflows. The magnitude bound matches the 32-bit signed
            # range because |INT32_MIN| is only 1 wider than INT32_MAX,
            # and reversing -2147483648 overflows the magnitude anyway.
            if result > INT32_MAX // 10 or (result == INT32_MAX // 10 and digit > 7):
                return 0

            result = result * 10 + digit

        return -result if neg else result


# =====================================================================
# APPROACH 2 : Unbounded accumulation, single final range check
# =====================================================================
class Solution_2:
    """
    Purpose : Reverse the digits using Python's unbounded ints, then
              clamp to 0 with ONE range check at the end.
    Inputs  : x — the integer whose digits must be reversed.
    Output  : int — reversed digits, or 0 on overflow.
    """

    def reverse(self, x: int) -> int:
        # Python ints are arbitrary precision: the reversal of any
        # int32 (≤ 10 digits) can NEVER overflow, so no mid-loop
        # guards exist. The loop is just the raw digit shuffle.
        sign = -1 if x < 0 else 1
        value = abs(x)
        result = 0
        while value != 0:
            result = result * 10 + (value % 10)
            value //= 10
        result *= sign

        # ONE emulated int32 boundary check. In C++ the hardware
        # truncates silently here — returning 0 is the contract.
        if result < INT32_MIN or result > INT32_MAX:
            return 0
        return result


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test table: {input, expected} — includes an overflow case and
    # INT_MIN, the value whose negation still equals itself in int32.
    tests: List[Tuple[int, int]] = [
        (123, 321),
        (-123, -321),
        (1534236469, 0),
        (-2147483648, 0),
    ]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    ok_1 = True
    for inp, exp in tests:
        got = Solution_1().reverse(inp)
        pass_ = got == exp
        ok_1 = ok_1 and pass_
        print(f"  A1 reverse({inp}) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    ok_2 = True
    for inp, exp in tests:
        got = Solution_2().reverse(inp)
        pass_ = got == exp
        ok_2 = ok_2 and pass_
        print(f"  A2 reverse({inp}) = {got}  expected {exp}  {'PASS' if pass_ else 'FAIL'}")
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Summary lines: time in µs, peak memory in KB.
    print(f"Approach 1 (guarded pop/push)   : time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.2f} KB")
    print(f"Approach 2 (unbounded + clamp)  : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.2f} KB")

    print("PASS : both approaches agree with every expected value."
          if ok_1 and ok_2
          else "FAIL : at least one test mismatched.")
