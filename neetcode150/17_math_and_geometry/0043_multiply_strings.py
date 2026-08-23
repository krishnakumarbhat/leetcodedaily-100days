"""
=====================================================================
LeetCode 43 : Multiply Strings                                 (Medium)
https://leetcode.com/problems/multiply-strings/
Category   : Math & Geometry
---------------------------------------------------------------------
PROBLEM
    Given two non-negative integers `num1` and `num2` as strings,
    return their product as a string. Inputs are up to 200 digits —
    far beyond any 64-bit integer, so we MUST multiply digit by
    digit, exactly like the grade-school algorithm.
---------------------------------------------------------------------
INTUITION
    num1 = Σ a_i·10^i  and  num2 = Σ b_j·10^j. Distributivity gives:
        num1 × num2 = Σ_i Σ_j (a_i·b_j) · 10^(i+j)
    So digit pair (i, j) always contributes to positional slot i+j —
    the "i+j digit-index trick". Accumulate all pair products in one
    array, then one carry pass normalizes it into the answer.
---------------------------------------------------------------------
APPROACH 1 — Digit-by-digit product array (BEST)
    res[i+j] accumulates a_i·b_j; carry flows to res[i+j+1] (the next
    power of ten). Exactly m+n slots (max digit count of the product).
    Time  Complexity : O(m·n)   Space Complexity : O(m+n)
    WHY it works: deferred carries are equivalent to the paper
    algorithm — slot (i+j) IS the 10^(i+j) place, and the carry from
    digit products is < 10 by construction, so it always lands in the
    very next slot.
---------------------------------------------------------------------
APPROACH 2 — Row-by-row long multiplication (textbook form)
    Multiply num1 by each digit of num2, producing one partial row
    per digit ("123×6=738", "123×5=6150"), then add every row into a
    running sum. Same O(m·n) math, two passes instead of one.
    Time  Complexity : O(m·n)   Space Complexity : O(m+n)
---------------------------------------------------------------------
REAL LIFE
    • Big-integer arithmetic (RSA/ECC cryptography multiplies
      2048-bit numbers that no machine int can hold) — exactly this
      digit loop, just in base 2³².
    • Decimal money/units libraries (pennies, mils) avoid float
      error by keeping every value as an integer digit string.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc


# =====================================================================
# APPROACH 1 : Digit-by-digit product array with i+j accumulation
# =====================================================================
class SolutionOne:
    """
    Purpose : Multiply two big numbers given as digit strings.
    Inputs  : num1 — first non-negative integer as a string.
              num2 — second non-negative integer as a string.
    Output  : str holding the exact product.
    """

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        m, n = len(num1), len(num2)

        # A product of an m-digit and an n-digit number has at most
        # m + n digits (e.g. 99×99 = 9801 has exactly 4 = 2+2 digits).
        # res is indexed from the MOST significant end: index k holds
        # the digit of weight 10^(m+n-1-k).
        res: list[int] = [0] * (m + n)

        # Walk every digit PAIR exactly once — the O(m·n) core.
        for i in range(m - 1, -1, -1):      # least significant first
            a = int(num1[i])                # i-th digit
            for j in range(n - 1, -1, -1):
                b = int(num2[j])            # j-th digit

                # THE i+j+1 TRICK: digits at positions i and j (counted
                # from the left) produce a value of weight
                # 10^(m-1-i) × 10^(n-1-j) = 10^(m+n-2-i-j), which lands
                # at index (m+n-1) − (m+n-2-i-j) = i+j+1.
                res[i + j + 1] += a * b     # accumulate the pair product

        # Deferred carry sweep: slots may hold up to 9×9×n < 10^3;
        # normalize right-to-left so each slot ends as a single digit.
        for k in range(m + n - 1, 0, -1):
            res[k - 1] += res[k] // 10
            res[k] %= 10

        # Slots hold digits most-significant-first → emit forward,
        # dropping leading zeros.
        start = 0
        while start < m + n - 1 and res[start] == 0:
            start += 1
        return "".join(str(res[i]) for i in range(start, m + n))


# =====================================================================
# APPROACH 2 : Row-by-row long multiplication (textbook form)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Multiply two big decimal strings the textbook way.
    Inputs  : num1, num2 — non-negative integers as digit strings.
    Output  : str holding the exact product.
    """

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        # Running sum of all partial rows, positional layout.
        # total[k] holds weight 10^k (LEAST significant end first).
        total: list[int] = [0] * (m + n)

        for j in range(n - 1, -1, -1):
            b = int(num2[j])
            carry = 0
            # Build ONE partial row: num1 × digit b, shifted by the
            # column offset (n-1-j) of digit j.
            for i in range(m - 1, -1, -1):
                a = int(num1[i])
                idx = (m - 1 - i) + (n - 1 - j)   # weight exponent
                acc = total[idx] + a * b + carry
                total[idx] = acc % 10
                carry = acc // 10
            total[(n - 1 - j) + m] += carry       # carry past the row's top

        start = m + n - 1
        while start > 0 and total[start] == 0:
            start -= 1
        return "".join(str(total[i]) for i in range(start, -1, -1))


# =====================================================================
# BENCHMARK — both approaches on 3 tests; time + peak memory (KB)
# =====================================================================
if __name__ == "__main__":
    # Fixed test suite; expected values verified with Python's own
    # arbitrary-precision int arithmetic (the reference implementation).
    tests = [
        ("123", "456", "56088"),
        ("2", "3", "6"),
        ("9133", "0", "0"),
    ]

    def run(label: str, solve) -> bool:
        """
        Purpose : Run one solution class over every test and print a row.
        Inputs  : label — display name of the approach.
                  solve — callable(num1, num2) -> str.
        Output  : bool — True when every test passed.
        """
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = True
        for a, b, expected in tests:
            got = solve(a, b)
            pass_ = got == expected
            ok = ok and pass_
            print(f"  {a} x {b} = {got}  {'PASS' if pass_ else 'FAIL (want ' + expected + ')'}")
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{label} : {'PASS' if ok else 'FAIL'}  time = {(t1 - t0) * 1e6:.1f} us  peak-mem = {peak // 1024} KB")
        return ok

    ok1 = run("Approach 1 (digit-by-digit i+j array)", lambda a, b: SolutionOne().multiply(a, b))
    ok2 = run("Approach 2 (row-by-row textbook)   ", lambda a, b: SolutionTwo().multiply(a, b))

    # Only PASS when BOTH approaches clear all 3 tests.
    print("PASS : both approaches return the exact product on all tests."
          if ok1 and ok2
          else "FAIL : at least one test failed.")
