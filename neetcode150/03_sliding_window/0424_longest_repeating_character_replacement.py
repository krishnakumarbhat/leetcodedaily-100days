"""
=====================================================================
LeetCode 424 : Longest Repeating Character Replacement      (Medium)
https://leetcode.com/problems/longest-repeating-character-replacement/
Category   : Sliding Window
---------------------------------------------------------------------
PROBLEM
    Given a string `s` of UPPERCASE letters and an integer `k`, you
    may change AT MOST k characters anywhere in the string. Return
    the length of the longest substring that can be made to contain
    ONLY ONE distinct character after those ≤ k changes.
---------------------------------------------------------------------
INTUITION
    A window [l, r] can be made uniform in ≤ k changes iff
        (window length) − (most frequent char count) ≤ k
    The left side counts "mismatched" characters — the ones that
    must be rewritten. The most frequent character is the one we
    KEEP; everything else gets converted into it.
---------------------------------------------------------------------
APPROACH 1 — Sliding window + running max frequency (BEST)
    count[26] tracks letter frequencies inside [l, r]. max_freq is
    the max over ALL history — it never decreases, which is sound:
    when len − max_freq > k, shrink l. max_len = max window seen.
    Time  Complexity : O(n)   Space Complexity : O(26) = O(1)
---------------------------------------------------------------------
APPROACH 2 — Brute force (every start, expand while valid)
    For each start i, expand j while the ≤ k condition holds using
    a fresh per-window count. Correct, but restarts all state for
    every i.
    Time  Complexity : O(n²)   Space Complexity : O(26) = O(1)
---------------------------------------------------------------------
DEEP DIVE — count[26] vs dict, and the max_freq trick
    The alphabet is exactly 26 uppercase letters → a list of 26
    ints indexed by (c − 'A') beats any hash map: no hashing, one
    contiguous array, perfect cache locality. A Python dict (open
    addressing + linear probing h(k,i) = (hash(k)+i) mod m) is
    correct but slower for a fixed 26-key universe.
    WHY max_freq never shrinks: max_len = r − l + 1 is monotone,
    and a stale-high max_freq makes (len − max_freq > k) only
    HARDER to pass → we shrink earlier, which is safe; it can never
    cause us to overstate max_len.
---------------------------------------------------------------------
REAL LIFE
    • Data-cleaning heuristics: longest run of similar records
      after tolerating k corrupt/missing values.
    • Compression: finding the largest chunk that can be normalized
      to one symbol with ≤ k edits (dictionary pre-scanning).
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : Sliding window + running max frequency (O(n))
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the longest substring of `s` that can become
              uniform after changing at most `k` characters.
    Inputs  : s — uppercase-letter string to scan.
              k — maximum allowed character replacements.
    Output  : int — length of the longest fixable substring.
    """

    def characterReplacement(self, s: str, k: int) -> int:
        # count : letter frequencies inside the current window.
        count: List[int] = [0] * 26
        l: int = 0        # left edge of the window
        max_freq: int = 0 # largest frequency EVER seen in any window
        max_len: int = 0  # best answer so far

        for r, ch in enumerate(s):
            # Expand: this char's frequency grows by one.
            idx = ord(ch) - ord("A")   # 'A'→0 … 'Z'→25
            count[idx] += 1
            # max_freq only ever grows — sound because it only makes
            # the validity check stricter, never looser (see dive).
            max_freq = max(max_freq, count[idx])

            # Invariant: window can be uniform in ≤ k changes.
            # If violated, shrink l until it holds again.
            while (r - l + 1) - max_freq > k:
                out = ord(s[l]) - ord("A")
                count[out] -= 1   # evicted char leaves the window
                l += 1
            # Window is valid again → candidate for the answer.
            max_len = max(max_len, r - l + 1)
        return max_len


# =====================================================================
# APPROACH 2 : Brute force — every start index, expand while valid
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the longest substring of `s` that can become
              uniform after changing at most `k` characters.
    Inputs  : s — uppercase-letter string to scan.
              k — maximum allowed character replacements.
    Output  : int — length of the longest fixable substring.
    """

    def characterReplacement(self, s: str, k: int) -> int:
        max_len: int = 0

        # Start index i fixes the window's left edge.
        for i in range(len(s)):
            count: List[int] = [0] * 26   # fresh counters per start
            max_freq: int = 0
            # Expand j while the ≤ k invariant still holds.
            for j in range(i, len(s)):
                idx = ord(s[j]) - ord("A")
                count[idx] += 1
                max_freq = max(max_freq, count[idx])
                # (j − i + 1) − max_freq = chars we would rewrite.
                if (j - i + 1) - max_freq <= k:
                    max_len = max(max_len, j - i + 1)
                else:
                    break   # shrinking j would only repeat shorter
        return max_len


# =====================================================================
# BENCHMARK — run both approaches on 3 tests + a longer string,
# compare time and peak memory (tracemalloc), print PASS/FAIL.
# =====================================================================
if __name__ == "__main__":
    tests: List[Tuple[str, int, int]] = [
        ("ABAB", 2, 4),     # official: whole string → "AAAA"
        ("AABABBA", 1, 4),  # official: best is length 4
        ("AAAB", 0, 3),     # k=0 → longest run of identical chars
    ]

    all_pass = True
    for s, k, expected in tests:
        r1 = SolutionOne().characterReplacement(s, k)
        r2 = SolutionTwo().characterReplacement(s, k)
        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'} s={s!r} k={k} expected={expected}  window={r1}  brute={r2}")

    # Longer string mixing long A-runs with filler, k=5.
    bench = "".join("AAAA" + "BCDEF" for _ in range(500))

    # --- Approach 1: time + peak memory ---
    tracemalloc.start()
    t0 = time.perf_counter()
    b1 = SolutionOne().characterReplacement(bench, 5)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t2 = time.perf_counter()
    b2 = SolutionTwo().characterReplacement(bench, 5)
    t3 = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (sliding window) : result={b1}  time={(t1 - t0) * 1e6:.2f} µs  peak-mem={peak_1} bytes")
    print(f"Approach 2 (brute force)    : result={b2}  time={(t3 - t2) * 1e6:.2f} µs  peak-mem={peak_2} bytes")

    # Brute force is the ground truth; the O(n) pass must match it.
    all_pass = all_pass and (b1 == b2)
    print("PASS : all test cases and benchmark agree." if all_pass
          else "FAIL : at least one answer is wrong.")
