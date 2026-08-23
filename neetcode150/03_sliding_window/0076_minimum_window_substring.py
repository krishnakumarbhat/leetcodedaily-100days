"""
=====================================================================
LeetCode 76 : Minimum Window Substring                        (Hard)
https://leetcode.com/problems/minimum-window-substring/
Category   : Sliding Window
---------------------------------------------------------------------
PROBLEM
    Given strings `s` and `t`, return the SHORTEST substring of `s`
    that contains EVERY character of `t` (including duplicates), or
    "" if no such window exists.
---------------------------------------------------------------------
INTUITION
    "Contains all of t" is a COUNTING condition, not an order
    condition. required = # of DISTINCT chars in t; formed = how
    many of them the window currently satisfies. When
    formed == required the window is valid — then shrink from the
    left while validity holds: a shorter window can only ever come
    from shrinking a valid one.
---------------------------------------------------------------------
APPROACH 1 — Sliding window + two dicts (formed/required)
    Grow r. When the window count of s[r] reaches t's requirement,
    formed += 1. While formed == required: record the candidate,
    then shrink l (decrement its count; below the requirement → 1).
    Time  Complexity : O(n + m)   Space Complexity : O(m)
    n = |s|, m = |t|; dicts hold ≤ |t| distinct chars.
---------------------------------------------------------------------
APPROACH 2 — Sliding window + 128-slot count arrays (no hashing)
    Identical logic, but need[128] / window_count[128] indexed by
    ASCII code: O(1) worst case, zero hashing, fixed memory.
    matched mirrors formed; required counts nonzero need slots.
    Time  Complexity : O(n + m)   Space Complexity : O(1)
---------------------------------------------------------------------
DEEP DIVE — count array vs hash map
    Python dict = open addressing + linear probing:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    C++ unordered_map = separate chaining. Both O(1) average.
    A fixed int[128] beats both for ASCII input: no hashing, one
    contiguous array, perfect cache locality, O(1) worst case. The
    formed/required trick is what makes each character movement
    O(1) instead of a full "window ⊇ t?" scan.
---------------------------------------------------------------------
REAL LIFE
    • Subtitle/transcript search: shortest span containing every
      keyword from a query (document snippet generation).
    • Network traffic filtering: shortest byte-range containing all
      required protocol markers — identical pattern.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from collections import Counter
from typing import Dict, Tuple, List


# =====================================================================
# APPROACH 1 : Sliding window + two dicts (formed/required)
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the shortest substring of `s` containing every
              character of `t` (with multiplicities), or "" if none.
    Inputs  : s — the haystack to search inside.
              t — the needle whose character counts must be matched.
    Output  : str — the minimum window, or empty string.
    """

    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""  # nothing to match or nowhere to look

        # need : t's character requirements (target counts).
        need: Dict[str, int] = Counter(t)
        # required = number of DISTINCT characters that must be met.
        required: int = len(need)
        # window_count : counts currently inside [l, r].
        window_count: Dict[str, int] = {}

        formed: int = 0              # chars that have met their quota
        ans_len: int = float("inf")  # best (smallest) window length
        ans_l: int = 0               # left edge of the best window
        l: int = 0                   # left edge of the CURRENT window

        for r, ch in enumerate(s):
            # Expand: s[r] enters the window.
            window_count[ch] = window_count.get(ch, 0) + 1

            # Did this expansion push exactly one char to its quota?
            if ch in need and window_count[ch] == need[ch]:
                formed += 1

            # Window is valid → try to shrink for a smaller window.
            while formed == required:
                # Candidate: [l, r] is valid and minimal post-shrink.
                length = r - l + 1
                if length < ans_len:
                    ans_len = length
                    ans_l = l
                # Shrink: s[l] leaves the window.
                out = s[l]
                window_count[out] -= 1
                # If the outgoing char breaks its quota → validity ends.
                if out in need and window_count[out] < need[out]:
                    formed -= 1
                l += 1

        # ans_len stays inf ⇔ no valid window ever existed.
        return "" if ans_len == float("inf") else s[ans_l:ans_l + ans_len]


# =====================================================================
# APPROACH 2 : Sliding window + 128-slot count arrays (no hashing)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the shortest substring of `s` containing every
              character of `t` (with multiplicities), or "" if none.
    Inputs  : s — the haystack to search inside.
              t — the needle whose character counts must be matched.
    Output  : str — the minimum window, or empty string.
    """

    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""

        # need : required count per ASCII char; slot = ord(char).
        need: List[int] = [0] * 128
        for ch in t:
            need[ord(ch)] += 1
        # required = distinct chars in t (slots whose need > 0).
        required = sum(1 for c in need if c > 0)

        window_count: List[int] = [0] * 128  # counts inside [l, r]
        matched: int = 0                     # chars meeting their quota
        ans_len: int = float("inf")
        ans_l: int = 0
        l: int = 0

        for r, ch in enumerate(s):
            # Expand: increment this char's window count, then check
            # whether it just crossed its quota (need[c] > 0 guard).
            c = ord(ch)
            window_count[c] += 1
            if need[c] > 0 and window_count[c] == need[c]:
                matched += 1

            while matched == required:
                length = r - l + 1
                if length < ans_len:
                    ans_len = length
                    ans_l = l
                out = ord(s[l])
                window_count[out] -= 1
                # Outgoing char dropped below quota → window invalid.
                if need[out] > 0 and window_count[out] < need[out]:
                    matched -= 1
                l += 1

        return "" if ans_len == float("inf") else s[ans_l:ans_l + ans_len]


# =====================================================================
# BENCHMARK — run both approaches on 3 tests + a longer pair,
# compare time and peak memory (tracemalloc), print PASS/FAIL.
# =====================================================================
if __name__ == "__main__":
    tests: List[Tuple[str, str, str]] = [
        ("ADOBECODEBANC", "ABC", "BANC"),  # classic official example
        ("a", "a", "a"),                  # single char matches
        ("a", "aa", ""),                  # t has more copies than s
    ]

    all_pass = True
    for s, t, expected in tests:
        r1 = SolutionOne().minWindow(s, t)
        r2 = SolutionTwo().minWindow(s, t)
        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'} s={s!r} t={t!r} expected={expected!r}  maps={r1!r}  arrays={r2!r}")

    # Longer adversarial-ish string: the minimum window is the suffix
    # "XYZ..." at the end, forcing the full shrink/slide cycle.
    bench_s = "AAAAAAABBBBBBCCCCCDDDDDABCDEFGHIJKLMNOPQRSTUVWXYZ"
    bench_t = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # --- Approach 1: time + peak memory ---
    tracemalloc.start()
    t0 = time.perf_counter()
    b1 = SolutionOne().minWindow(bench_s, bench_t)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t2 = time.perf_counter()
    b2 = SolutionTwo().minWindow(bench_s, bench_t)
    t3 = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (hash maps)     : result={b1!r}  time={(t1 - t0) * 1e6:.2f} µs  peak-mem={peak_1} bytes")
    print(f"Approach 2 (count arrays)  : result={b2!r}  time={(t3 - t2) * 1e6:.2f} µs  peak-mem={peak_2} bytes")

    all_pass = all_pass and (b1 == b2)
    print("PASS : all test cases and benchmark agree." if all_pass
          else "FAIL : at least one answer is wrong.")
