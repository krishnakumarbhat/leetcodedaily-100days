"""
=====================================================================
LeetCode 10 : Regular Expression Matching                        (Hard)
https://leetcode.com/problems/regular-expression-matching/
Category   : 2D DP
---------------------------------------------------------------------
PROBLEM
    Given an input string `s` and a pattern `p`, implement regular
    expression matching with two wildcards:
        '.'  — matches ANY single character.
        '*'  — matches ZERO or MORE of the PRECEDING element.
    The match must cover the ENTIRE string.
---------------------------------------------------------------------
INTUITION
    Every prefix pair (s[0..i), p[0..j)) is a self-contained sub-problem
    whose answer depends only on SMALLER prefix pairs → a 2D DP table
    dp[i][j] = "does s[0..i-1] match p[0..j-1]?". The '*' rule gives a
    CHOICE (zero copies vs one more copy) — an OR over two states.
---------------------------------------------------------------------
APPROACH 1 — Bottom-up 2D DP (BEST)
    dp[i][j] = does s[0..i-1] match p[0..j-1]?
        Base: dp[0][0] = True.
        p[j-1] != '*':
            dp[i][j] = dp[i-1][j-1] AND (s[i-1] == p[j-1] OR p[j-1]=='.')
        p[j-1] == '*':
            dp[i][j] = dp[i][j-2]        (zero copies)
                    OR (dp[i-1][j] AND (s[i-1] == p[j-2] OR p[j-2]=='.'))
    Time  Complexity : O(|s|·|p|)   Space Complexity : O(|s|·|p|)
---------------------------------------------------------------------
APPROACH 2 — Top-down memoized DFS (same recurrence, recursion-first)
    solve(i, j) computes the same value lazily, recursing only on the
    states it needs and memoizing them.
    Time  Complexity : O(|s|·|p|)   Space Complexity : O(|s|·|p|)
---------------------------------------------------------------------
REAL LIFE
    • Every regex engine (grep, V8, RE2) implements '.' and '*' —
      RE2/PCRE literally use a DP like this (Thompson NFA simulation).
    • Input validation, template systems, URL routers ("/users/:id*").
---------------------------------------------------------------------
DEEP DIVE — the '*' recurrence
    p = "c*" against s = "cccc": the '*' must decide:
      zero copies → drop "c*" (dp[i][j-2]); one more copy → consume
      one matching char and KEEP "c*" (dp[i-1][j]). The OR lets ONE
      '*' absorb any run length, including zero. Table is (|s|+1)×(|p|+1)
      so the empty-string prefixes are representable.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc


# =====================================================================
# APPROACH 1 : Bottom-up 2D DP (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether `s` fully matches pattern `p`.
    Inputs  : s — subject string; p — pattern with '.' and '*'.
    Output  : True iff the full s matches the full p.
    """

    def isMatch(self, s: str, p: str) -> bool:
        n, m = len(s), len(p)
        # dp[i][j] : do the FIRST i chars of s match the FIRST j of p?
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True  # empty string matches empty pattern

        # Row 0: "a*b*c*" matches the empty string iff every literal is
        # neutralized by a following '*'.
        for j in range(2, m + 1):
            if p[j - 1] == "*":
                dp[0][j] = dp[0][j - 2]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if p[j - 1] != "*":
                    # Literal or '.': both sides consume exactly one char.
                    dp[i][j] = dp[i - 1][j - 1] and (s[i - 1] == p[j - 1] or p[j - 1] == ".")
                else:
                    # '*' = zero copies (dp[i][j-2]) OR one more copy:
                    # consume s[i-1] when it equals the '*'s character.
                    dp[i][j] = dp[i][j - 2]
                    if s[i - 1] == p[j - 2] or p[j - 2] == ".":
                        dp[i][j] = dp[i][j] or dp[i - 1][j]
        return dp[n][m]


# =====================================================================
# APPROACH 2 : Top-down memoized DFS (same recurrence)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether `s` fully matches pattern `p` (memo DFS).
    Inputs  : s — subject string; p — pattern with '.' and '*'.
    Output  : True iff the full s matches the full p.
    """

    def isMatch(self, s: str, p: str) -> bool:
        # memo[(i,j)] : known answer for "s[i:] vs p[j:]" (-1 unknown).
        memo: dict[tuple[int, int], bool] = {}

        def solve(i: int, j: int) -> bool:
            if (i, j) in memo:
                return memo[(i, j)]  # memo hit → O(1)
            if j == len(p):
                # Pattern spent: the string must be spent too.
                ans = i == len(s)
            else:
                # Does this position match? (literal, or '.' wildcard)
                first_match = i < len(s) and (s[i] == p[j] or p[j] == ".")
                if j + 1 < len(p) and p[j + 1] == "*":
                    # 'x*' ahead → skip it entirely, OR consume one char
                    # and keep 'x*' so it can repeat.
                    ans = solve(i, j + 2) or (first_match and solve(i + 1, j))
                else:
                    # No '*' after p[j]: both consume exactly one char.
                    ans = first_match and solve(i + 1, j + 1)
            memo[(i, j)] = ans
            return ans

        return solve(0, 0)


# =====================================================================
# BENCHMARK — run both approaches on the official examples
# =====================================================================
if __name__ == "__main__":
    tests: list[tuple[str, str, bool]] = [
        ("aa", "a", False),
        ("aa", "a*", True),
        ("aab", "c*a*b", True),
        ("mississippi", "mis*is*p*.", False),
        ("ab", ".*", True),
    ]

    ok1 = ok2 = True
    us1 = us2 = 0.0
    peak1 = peak2 = 0

    for s, p, expected in tests:
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().isMatch(s, p)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().isMatch(s, p)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        us1 += (t1 - t0) * 1e6
        us2 += (t1b - t0b) * 1e6
        ok1 = ok1 and (r1 == expected)
        ok2 = ok2 and (r2 == expected)
        print(f"isMatch({s!r}, {p!r})  A1={r1}  A2={r2}  expected={expected}")

    print(f"Approach 1 (2D DP)      : {'PASS' if ok1 else 'FAIL'}  time = {us1:.2f} µs  peak-mem = {peak1 // 1024} KB")
    print(f"Approach 2 (memo DFS)   : {'PASS' if ok2 else 'FAIL'}  time = {us2:.2f} µs  peak-mem = {peak2 // 1024} KB")
