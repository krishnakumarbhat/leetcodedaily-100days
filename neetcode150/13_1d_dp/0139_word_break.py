"""
=====================================================================
LeetCode 139 : Word Break                                     (Medium)
https://leetcode.com/problems/word-break/
Category   : 1D Dynamic Programming
---------------------------------------------------------------------
PROBLEM
    Given a string `s` and a word dictionary `wordDict`, return True if
    `s` can be segmented into a space-separated sequence of dictionary
    words (words may be reused).
---------------------------------------------------------------------
INTUITION
    s is breakable iff some PREFIX s[0:j] is breakable AND the
    remaining suffix s[j:i] is a dictionary word → the same suffix is
    checked by many prefixes → overlapping subproblems. The word
    dictionary must answer "is this slice a word?" in O(1) → put it in
    a hash set (dict) — or a trie to test characters incrementally.
---------------------------------------------------------------------
APPROACH 1 — Bottom-up DP + hash set (BEST)
    dp[i] = s[0:i] is breakable. dp[0] = True (empty prefix).
    Recurrence : dp[i] = OR over j < i of ( dp[j] and s[j:i] in wordSet )
    State space : i ∈ [0, n] → n+1 booleans on array dp[n+1], filled
                  left→right; cell i reads every earlier cell j → the
                  table is essential (no rolling-variable shortcut).
    Time  Complexity : O(n²·m) — n² (i, j) pairs × O(m) slice hash,
                       m = max word length.
    Space Complexity : O(n) for dp + O(total word chars) for the set.
---------------------------------------------------------------------
APPROACH 2 — Top-down memoized DFS (suffix-first)
    f(i) = can s[i:] be broken? Try each dictionary word w: if s[i:]
    starts with w AND f(i+len(w)) → True. memo[i] caches suffixes.
    Trade-off : explores only word-aligned boundaries (usually fewer
    checks than all n² boundaries); recursion depth up to n.
    Time  Complexity : O(n·W·m)   Space Complexity : O(n) memo + set.
---------------------------------------------------------------------
REAL LIFE
    • Input sanitizers / "sentence from words" (predictive text).
    • Regex tokenizers, dictionary-driven text segmentation.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Set, Tuple


# =====================================================================
# APPROACH 1 : bottom-up DP with a word-set hash map
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether `s` segments into words of `wordDict`.
    Inputs  : s — the string to segment.
              wordDict — list of allowed dictionary words.
    Output  : bool — True when a valid segmentation exists.
    """

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Hash set (open addressing, linear probing) → O(1) membership.
        word_set: Set[str] = set(wordDict)
        n = len(s)
        dp: List[bool] = [False] * (n + 1)
        dp[0] = True  # empty prefix is trivially breakable

        # Fill left→right: is prefix s[0:i] breakable?
        for i in range(1, n + 1):
            # Try every split point j: breakable prefix + dict-word suffix.
            for j in range(i):
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True   # one valid split is enough
                    break          # no need to test further j
        return dp[n]


# =====================================================================
# APPROACH 2 : top-down memoized DFS over suffixes
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether `s` segments into words of `wordDict`.
    Inputs  : s — the string to segment.
              wordDict — list of allowed dictionary words.
    Output  : bool — True when a valid segmentation exists.
    """

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set: Set[str] = set(wordDict)
        memo: List[int] = [-1] * len(s)  # -1 unknown, 0 false, 1 true

        def f(i: int) -> bool:
            if i == len(s):
                return True             # suffix consumed → breakable
            if memo[i] != -1:
                return bool(memo[i])    # overlapping subproblem → reuse
            # Try every word as the head of the remaining suffix.
            for w in wordDict:
                if s.startswith(w, i) and f(i + len(w)):
                    memo[i] = 1         # cache the answer
                    return True
            memo[i] = 0
            return False

        return f(0)


# =====================================================================
# BENCHMARK — run both approaches on every test, compare time + RAM
# =====================================================================
if __name__ == "__main__":
    # Test battery: (s, wordDict, expected). Both solutions must match.
    tests: List[Tuple[str, List[str], bool]] = [
        ("leetcode", ["leet", "code"], True),
        ("applepenapple", ["apple", "pen"], True),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
    ]

    total_us_1 = total_us_2 = 0.0
    total_kb_1 = total_kb_2 = 0
    all_pass = True

    for s, words, expected in tests:
        # --- Approach 1: perf_counter for time, tracemalloc for RAM ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().wordBreak(s, words)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_1 += (t1 - t0) * 1e6
        total_kb_1 += peak1 // 1024

        # --- Approach 2 ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().wordBreak(s, words)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        total_us_2 += (t1b - t0b) * 1e6
        total_kb_2 += peak2 // 1024

        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"s={s!r:14} A1={r1!s:5} A2={r2!s:5} expected={expected!s:5} "
              f"{'PASS' if ok else 'FAIL'}  "
              f"A1 {(t1 - t0) * 1e6:.1f}µs/{peak1 // 1024}KB  "
              f"A2 {(t1b - t0b) * 1e6:.1f}µs/{peak2 // 1024}KB")

    print(f"Totals: A1 {total_us_1:.1f}µs/{total_kb_1}KB | "
          f"A2 {total_us_2:.1f}µs/{total_kb_2}KB")
    print("PASS : both approaches match every expected output."
          if all_pass
          else "FAIL : at least one answer is wrong.")