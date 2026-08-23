"""
=====================================================================
LeetCode 66 : Plus One                                           (Easy)
https://leetcode.com/problems/plus-one/
Category   : Math & Geometry
---------------------------------------------------------------------
PROBLEM
    Given a big integer as a digit array (most significant first, no
    leading zeros), add ONE and return the new digit array. The
    number may be arbitrarily long — never convert to int.
---------------------------------------------------------------------
INTUITION
    Adding 1 only touches digits from the RIGHT until a digit < 9
    absorbs the carry. If every digit is 9 the number gains a new
    leading digit: [9,9] → [1,0,0]. Walk least-significant-first
    with a carry and stop the moment the carry is absorbed.
---------------------------------------------------------------------
APPROACH 1 — Backwards scan with carry (BEST)
    carry = 1 at the last digit; for each digit right → left: add
    carry; 10 → set 0 and continue; otherwise return immediately.
    All-9 input → prepend a leading 1.
    Time  Complexity : O(n)   Space Complexity : O(1) extra
---------------------------------------------------------------------
APPROACH 2 — Integer round-trip (contrast)
    int(digits) + 1 → back to digits. Correct only while the value
    fits a machine int; silently wrong beyond ~19 digits.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Big-number counters: odometers, invoice numbers, database
      auto-increment IDs that exceed 64 bits.
    • "Add one to a huge decimal" is the warm-up pattern for full
      big-integer addition (adding 999...9 exercises the carry chain).
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc

from typing import List


# =====================================================================
# APPROACH 1 : Backwards scan with carry (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Add one to a big integer stored as a digit array.
    Inputs  : digits — most-significant-first list of ints.
    Output  : List[int] holding the incremented digits.
    """

    def plusOne(self, digits: List[int]) -> List[int]:
        out = digits[:]                    # work on a copy

        # Walk from the LEAST significant digit, carrying 1 leftward.
        for i in range(len(out) - 1, -1, -1):
            if out[i] < 9:
                out[i] += 1                # carry absorbed right here
                return out                 # done — left digits unchanged
            out[i] = 0                     # 9+1 = 10 → 0, carry on

        # Every digit was 9 → the number gained one new leading digit.
        return [1] + out                   # [9,9,9] → [1,0,0,0]


# =====================================================================
# APPROACH 2 : Integer round-trip (contrast — overflow trap)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Add one by converting the digit array to an integer.
    Inputs  : digits — most-significant-first list of ints.
    Output  : List[int] holding the incremented digits.
    NOTE    : only correct while the value fits a machine int;
              longer inputs silently wrap — why Approach 1 exists.
    """

    def plusOne(self, digits: List[int]) -> List[int]:
        # Horner's rule: value = ((d0)*10 + d1)*10 + ... + dn.
        value = 0
        for d in digits:
            value = value * 10 + d
        value += 1

        # Emit the digits of value, most significant first.
        out: List[int] = []
        while value > 0:
            out.append(value % 10)
            value //= 10
        out.reverse()                      # collected LSB-first
        return out or [0]


# =====================================================================
# BENCHMARK — both approaches on 3 tests; time + peak memory (KB)
# =====================================================================
if __name__ == "__main__":
    tests = [[1, 2, 3], [9, 9, 9], [4, 3, 2, 1]]
    expected = [[1, 2, 4], [1, 0, 0, 0], [4, 3, 2, 2]]

    def run(label: str, solve) -> bool:
        """
        Purpose : Run one solution class over every test and print a row.
        Inputs  : label — display name of the approach.
                  solve — callable(digits) -> List[int].
        Output  : bool — True when every test passed.
        """
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = True
        for i, (d, want) in enumerate(zip(tests, expected)):
            got = solve(d)
            pass_ = got == want
            ok = ok and pass_
            print(f"  test {i + 1}: {got}  {'PASS' if pass_ else 'FAIL'}")
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{label} : {'PASS' if ok else 'FAIL'}  time = {(t1 - t0) * 1e6:.1f} us  peak-mem = {peak // 1024} KB")
        return ok

    ok1 = run("Approach 1 (backwards carry scan)  ", lambda d: SolutionOne().plusOne(d))
    ok2 = run("Approach 2 (int round-trip)        ", lambda d: SolutionTwo().plusOne(d))

    print("PASS : both approaches return the incremented digits on all tests."
          if ok1 and ok2
          else "FAIL : at least one test failed.")