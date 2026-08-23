"""
=====================================================================
LeetCode 3 : Longest Substring Without Repeating Characters  (Medium)
https://leetcode.com/problems/longest-substring-without-repeating-characters/
Category   : Sliding Window
---------------------------------------------------------------------
PROBLEM
    Given a string `s`, return the length of the LONGEST substring
    (contiguous slice) that contains NO repeating characters.
---------------------------------------------------------------------
INTUITION
    A window [l, r] is valid ⇔ all its characters are distinct.
    When s[r] duplicates a character already inside the window, the
    window cannot grow — shrink from the left until the duplicate is
    evicted. r advances n times, l advances at most n times → O(n)
    amortized. This is THE canonical sliding-window pattern.
---------------------------------------------------------------------
APPROACH 1 — Sliding window + set (shrink step-by-step)
    Keep the set of characters inside [l, r]. On duplicate, evict
    s[l] and l++ until the duplicate is gone, then insert s[r].
    Time  Complexity : O(n)   Space Complexity : O(min(n, m))
    m = alphabet size (≤ 128 ASCII on LeetCode).
---------------------------------------------------------------------
APPROACH 2 — Sliding window + last-seen index map (JUMP past dupe)
    Store each char's most recent index; on duplicate l jumps to
    last_seen[s[r]] + 1 instead of evicting char-by-char.
    Time  Complexity : O(n)   Space Complexity : O(min(n, m))
---------------------------------------------------------------------
DEEP DIVE — set/map vs fixed count array, ASCII vs Unicode
    Python dict/set = open addressing with LINEAR PROBING:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    Collisions walk to the next free slot in ONE contiguous array →
    cache locality + tiny memory. C++ unordered_map/unordered_set =
    separate chaining (bucket of linked lists), O(1) average.
    If the alphabet is ASCII (≤ 128), a fixed array indexed by char
    code is faster than any hash structure: zero hashing, 128
    contiguous slots. For Unicode, maps keyed on code points are
    required — an array[128] would index only the first byte of a
    multi-byte UTF-8 char and silently produce wrong answers.
---------------------------------------------------------------------
REAL LIFE
    • Streaming deduplication: longest chunk of unique data in a
      byte stream (compression heuristics, cache line analysis).
    • Session/socket tracing: longest window of distinct events
      before a repeat forces a flush.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Optional


# =====================================================================
# APPROACH 1 : Sliding window + set (evict one char at a time)
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the length of the longest substring of `s` that
              contains no repeated characters.
    Inputs  : s — the string to scan.
    Output  : int — length of the longest valid substring.
    """

    def lengthOfLongestSubstring(self, s: str) -> int:
        # window : chars currently inside the [l, r] slice. Python
        # set = open-addressing table → O(1) average membership test.
        window: set[str] = set()
        l: int = 0        # left edge of the window (shrinks)
        max_len: int = 0  # best valid length seen so far

        for r, ch in enumerate(s):
            # s[r] breaks the "all distinct" invariant → shrink the
            # left edge until the duplicate char is evicted. Every
            # char is erased at most once → O(n) total work.
            while ch in window:
                window.remove(s[l])
                l += 1
            # Invariant restored → s[r] may join the window.
            window.add(ch)
            # [l, r] is valid by construction → candidate for best.
            max_len = max(max_len, r - l + 1)
        return max_len


# =====================================================================
# APPROACH 2 : Sliding window + last-seen index map (jump past dupe)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the length of the longest substring of `s` that
              contains no repeated characters.
    Inputs  : s — the string to scan.
    Output  : int — length of the longest valid substring.
    """

    def lengthOfLongestSubstring(self, s: str) -> int:
        # last_seen : char -> most recent index where it appeared.
        # Entries below `l` are stale — they predate the window.
        last_seen: dict[str, int] = {}
        l: int = 0        # left edge of the window
        max_len: int = 0  # best valid length seen so far

        for r, ch in enumerate(s):
            # If ch was seen INSIDE the current window, every index
            # ≤ that sighting is poisoned → l jumps over it in one
            # step instead of evicting char-by-char.
            if ch in last_seen and last_seen[ch] >= l:
                l = last_seen[ch] + 1
            # Record this sighting; future duplicates use it to jump.
            last_seen[ch] = r
            # [l, r] is valid by construction → candidate for best.
            max_len = max(max_len, r - l + 1)
        return max_len


# =====================================================================
# BENCHMARK — run both approaches on 3 tests + a longer string,
# compare time and peak memory (tracemalloc), print PASS/FAIL.
# =====================================================================
if __name__ == "__main__":
    tests: List[tuple[str, int]] = [
        ("abcabcbb", 3),  # "abc"     — classic triple repeat
        ("bbbbb", 1),     # "b"       — all identical
        ("pwwkew", 3),    # "wke"     — answer is a middle window
    ]

    all_pass = True
    for s, expected in tests:
        r1 = SolutionOne().lengthOfLongestSubstring(s)
        r2 = SolutionTwo().lengthOfLongestSubstring(s)
        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'} s={s!r} expected={expected}  set={r1}  jumpMap={r2}")

    # Longer mixed-case string so the benchmark is not trivially fast.
    bench = ("abcabcbbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "0123456789aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz")

    # --- Approach 1: time + peak memory ---
    tracemalloc.start()
    t0 = time.perf_counter()
    b1 = SolutionOne().lengthOfLongestSubstring(bench)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t2 = time.perf_counter()
    b2 = SolutionTwo().lengthOfLongestSubstring(bench)
    t3 = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (set eviction)  : result={b1}  time={(t1 - t0) * 1e6:.2f} µs  peak-mem={peak_1} bytes")
    print(f"Approach 2 (index jump)    : result={b2}  time={(t3 - t2) * 1e6:.2f} µs  peak-mem={peak_2} bytes")

    # Both approaches must agree with each other on the big string too.
    all_pass = all_pass and (b1 == b2)
    print("PASS : all test cases and benchmark agree." if all_pass
          else "FAIL : at least one answer is wrong.")
