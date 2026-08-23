"""
=====================================================================
LeetCode 5 : Longest Palindromic Substring                     (Medium)
https://leetcode.com/problems/longest-palindromic-substring/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    Given a string `s`, return the LONGEST substring that reads the
    same forwards and backwards (a palindrome). Ties: any one answer.
---------------------------------------------------------------------
INTUITION
    A palindrome is symmetric around a CENTER. Every palindrome has a
    unique center — one char for odd length, the gap between two chars
    for even length. So instead of testing all O(n²) substrings, grow
    outwards from all 2n-1 centers and stop at the first mismatch.
    DP view: s[i..j] is a palindrome ⇔ s[i] == s[j] AND s[i+1..j-1] is
    a palindrome → optimal substructure + overlapping subproblems.
---------------------------------------------------------------------
APPROACH 1 — Expand around centers (BEST)
    For every center c ∈ [0, 2n): expand while the two mirrored chars
    match; track the widest window seen.
    Time  Complexity : O(n²) — 2n-1 centers × O(n) expansion each.
    Space Complexity : O(1) — a few index variables.
---------------------------------------------------------------------
APPROACH 2 — DP boolean table
    dp[i][j] = s[i..j] is a palindrome.
    Recurrence : dp[i][j] = (s[i] == s[j]) and (j - i <= 2 or dp[i+1][j-1])
    State space : (i, j) with i <= j → n(n+1)/2 ≈ O(n²) states mapped
                  onto an n×n table. Fill by increasing length so the
                  inner cell dp[i+1][j-1] is already computed.
    Space optimization : row i reads only row i+1 → ONE rolling row of
                  booleans collapses the table to O(n) space.
    Time  Complexity : O(n²)   Space Complexity : O(n²) → O(n) rolling
---------------------------------------------------------------------
REAL LIFE
    • Bio-informatics: DNA/RNA palindromic motifs are regulatory
      regions — finding them is literally this problem.
    • Text editors / string toolboxes: mirror detection primitives.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : expand around every center (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the longest palindromic substring of `s`.
    Inputs  : s — the string to search inside.
    Output  : str — widest palindrome window (any tie).
    """

    def longestPalindrome(self, s: str) -> str:
        # best_l/best_r = inclusive window of the widest palindrome.
        best_l, best_r = 0, 0
        n = len(s)

        # 2n-1 centers: even c → single char, odd c → gap between chars.
        for c in range(2 * n - 1):
            # c=0 → (0,0); c=1 → (0,1); c=2 → (1,1); c=3 → (1,2); ...
            l, r = c // 2, (c + 1) // 2
            # Expand while the mirrored characters still match.
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l > best_r - best_l:   # strictly wider → new best
                    best_l, best_r = l, r
                l -= 1                        # reach one char further left
                r += 1                        # ...and one further right

        return s[best_l:best_r + 1]


# =====================================================================
# APPROACH 2 : DP boolean table, filled by increasing length
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the longest palindromic substring of `s`.
    Inputs  : s — the string to search inside.
    Output  : str — widest palindrome window (any tie).
    """

    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n == 0:
            return ""  # empty-string edge case

        # dp[i][j] = True ⇔ s[i..j] is a palindrome.
        dp: List[List[bool]] = [[False] * n for _ in range(n)]
        best_l, best_r = 0, 0

        # Fill by LENGTH so dp[i+1][j-1] (length len-2) already exists.
        for length in range(1, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                # Recurrence: matching ends AND a valid inner window
                # (length 1 or 2 needs no inner window at all).
                if s[i] == s[j] and (length <= 2 or dp[i + 1][j - 1]):
                    dp[i][j] = True
                    if length > best_r - best_l + 1:  # new global best
                        best_l, best_r = i, j

        return s[best_l:best_r + 1]


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (input, expected). Both solutions must match.
    tests: List[Tuple[str, str]] = [
        ("babad", "bab"),   # "aba" is also valid — check length only
        ("cbbd", "bb"),
        ("a", "a"),
    ]

    total_us_1 = total_us_2 = 0.0
    total_kb_1 = total_kb_2 = 0
    all_pass = True

    def is_pal(x: str) -> bool:
        """Return True when x reads identically forwards and backwards."""
        return x == x[::-1]

    for s, expected in tests:
        # --- Approach 1: time via perf_counter, RAM via tracemalloc ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().longestPalindrome(s)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_1 += (t1 - t0) * 1e6
        total_kb_1 += peak1 // 1024

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().longestPalindrome(s)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_2 += (t1b - t0b) * 1e6
        total_kb_2 += peak2 // 1024

        # Acceptance: a palindrome of the SAME length as expected (ties ok).
        ok = is_pal(r1) and is_pal(r2) and len(r1) == len(expected) and len(r2) == len(expected)
        all_pass = all_pass and ok
        print(f"s={s!r:8} A1={r1!r:5} A2={r2!r:5} expected-len={len(expected)} "
              f"{'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches return valid maximal palindromes."
          if all_pass
          else "FAIL : at least one answer is wrong.")