"""
=====================================================================
LeetCode 91 : Decode Ways                                      (Medium)
https://leetcode.com/problems/decode-ways/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    A message of digits maps letters as 'A'→1 … 'Z'→26. Given a digit
    string `s`, count how many ways it can be decoded back to letters.
    Invalid if any digit cannot be consumed (e.g. a lone '0').
---------------------------------------------------------------------
INTUITION
    When scanning left→right, each position i can END a code of length
    1 (s[i] in 1..9) or length 2 (s[i-1..i] in 10..26). The number of
    decodings of prefix s[0..i] is the SUM of the decodings of the two
    prefixes that precede those endings → ways(i) = ways(i-1) + ways(i-2)
    with validity gates — Fibonacci again with filters.
---------------------------------------------------------------------
APPROACH 1 — Bottom-up with rolling variables (BEST)
    dp[i] = decodings of prefix s[0..i) (i = consumed characters).
    Recurrence :
        one = dp[i-1] if s[i-1] != '0' else 0      (code '1'..'9')
        two = dp[i-2] if s[i-2..i-1] in [10..26] else 0
        dp[i] = one + two
    State space : i ∈ [0, n] → n+1 states on array dp[n+1], filled
                  left→right; dp[i] reads only i-1, i-2 → roll the
                  table down to two variables → O(1) space.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Top-down memoized recursion
    f(i) = decodings of suffix s[i:]. Two branches: take 1 char (if
    valid) and take 2 chars (if 10..26). memo[i] caches each suffix.
    Trade-off : reads the string right-to-left — mirrors how a human
    would backtrack; recursion depth n for long strings.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Text messaging / T9: mapping digit sequences to words.
    • Barcode / ISBN check-digit decoding, biorhythm codes.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : bottom-up, two rolling variables
# =====================================================================
class SolutionOne:
    """
    Purpose : Count valid decodings of the digit string `s`.
    Inputs  : s — digits-only string (may start with '0').
    Output  : int — number of ways, 0 when undecodable.
    """

    def numDecodings(self, s: str) -> int:
        n = len(s)
        # Rolling window: prev2 = dp[i-2], prev1 = dp[i-1].
        prev2, prev1 = 1, 1  # dp[0] = 1 (empty prefix), dp[1] set below
        for i in range(1, n + 1):
            cur = 0
            # Length-1 code: this digit alone must be '1'..'9'.
            if s[i - 1] != '0':
                cur += prev1  # extend every dp[i-1] decoding by s[i-1]
            # Length-2 code: previous two digits must form 10..26.
            if i >= 2 and s[i - 2] == '1':
                cur += prev2  # 10..19
            elif i >= 2 and s[i - 2] == '2' and s[i - 1] <= '6':
                cur += prev2  # 20..26
            prev2, prev1 = prev1, cur  # slide the window right
        return prev1  # dp[n]


# =====================================================================
# APPROACH 2 : top-down memoized recursion over suffixes
# =====================================================================
class SolutionTwo:
    """
    Purpose : Count valid decodings of the digit string `s` (memoized).
    Inputs  : s — digits-only string.
    Output  : int — number of ways, 0 when undecodable.
    """

    def numDecodings(self, s: str) -> int:
        n = len(s)
        memo: List[int] = [-1] * (n + 1)  # -1 = suffix not solved yet

        def f(i: int) -> int:
            if i == n:
                return 1                      # consumed everything → 1 way
            if s[i] == '0':
                return 0                      # '0' cannot START a code
            if memo[i] != -1:
                return memo[i]                # overlapping subproblem → reuse
            # Branch 1: take one digit (guaranteed valid, it is 1..9).
            ways = f(i + 1)
            # Branch 2: take two digits if they form 10..26.
            if i + 1 < n and (s[i] == '1' or (s[i] == '2' and s[i + 1] <= '6')):
                ways += f(i + 2)
            memo[i] = ways                    # cache before returning
            return ways

        return f(0)


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (s, expected ways). Both solutions must match.
    tests: List[Tuple[str, int]] = [
        ("12", 2),    # "AB"(1,2), "L"(12)
        ("226", 3),   # "BZ"(2,26), "VF"(22,6), "BBF"(2,2,6)
        ("06", 0),    # '0' cannot lead a code → undecodable
    ]

    total_us_1 = total_us_2 = 0.0
    total_kb_1 = total_kb_2 = 0
    all_pass = True

    for s, expected in tests:
        # --- Approach 1: perf_counter for time, tracemalloc for RAM ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().numDecodings(s)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_1 += (t1 - t0) * 1e6
        total_kb_1 += peak1 // 1024

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().numDecodings(s)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_2 += (t1b - t0b) * 1e6
        total_kb_2 += peak2 // 1024

        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"s={s!r:6} A1={r1} A2={r2} expected={expected} "
              f"{'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches match every expected output."
          if all_pass
          else "FAIL : at least one answer is wrong.")