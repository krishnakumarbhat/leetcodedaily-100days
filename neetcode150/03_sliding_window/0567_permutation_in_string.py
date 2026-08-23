"""
=====================================================================
LeetCode 567 : Permutation in String                          (Medium)
https://leetcode.com/problems/permutation-in-string/
Category   : Sliding Window
---------------------------------------------------------------------
PROBLEM
    Given strings `s1` and `s2`, return true if s2 contains ANY
    permutation of s1 as a contiguous substring.
---------------------------------------------------------------------
INTUITION
    A permutation is a re-ORDERING — so "s2 contains a permutation
    of s1" ⇔ "some length-|s1| window of s2 has the same character
    MULTISET as s1". Counting kills ordering. A window of exactly
    len(s1) slides over s2; each slide drops one char and adds one.
    The naive "compare 26 counters per slide" costs O(26n); a
    `matches` counter makes each slide O(1).
---------------------------------------------------------------------
APPROACH 1 — Fixed window + 26-array counters + matches (BEST)
    Count s1 into c1[26] and the first |s1| chars of s2 into c2[26].
    matches = #slots where c1[i] == c2[i]. Sliding: adding s2[i]
    and removing s2[i − |s1|] can each flip ONLY ONE slot's
    equality → matches updates in O(1) per slide. matches == 26 ⇔
    identical multisets ⇔ true.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Fixed window + Counter (dict) comparison
    Same window, but counters live in a collections.Counter and the
    full comparison happens every slide — O(σ) per slide.
    Time  Complexity : O(n·σ)   Space Complexity : O(σ)
    σ = distinct characters involved.
---------------------------------------------------------------------
DEEP DIVE — count[26] vs dict/Counter
    Fixed 26-letter lowercase alphabet (LeetCode constraint) → two
    lists of 26 ints win: index = ord(c) − ord('a'), O(1) worst
    case, zero hashing, one contiguous cache line. Counter is a
    dict subclass (open addressing, linear probing
    h(k,i) = (hash(k)+i) mod m) — correct but pays hash + resize
    costs for a universe of 26 keys. The REAL lesson is the
    `matches` counter: turning a per-slide full comparison into
    O(1) incremental bookkeeping is the difference between O(26n)
    and O(n).
---------------------------------------------------------------------
REAL LIFE
    • Substring anagram search in bioinformatics (k-mer counting)
      and plagiarism tools — same multiset-window pattern.
    • Plagiarism/scramble detection: does any fixed-length chunk of
      a document contain the same letter histogram as a query word?
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from collections import Counter
from typing import List, Tuple


# =====================================================================
# APPROACH 1 : Fixed window + 26 arrays + incremental matches count
# =====================================================================
class SolutionOne:
    """
    Purpose : Return true if some contiguous window of `s2` is a
              permutation of `s1`.
    Inputs  : s1 — the needle (its multiset must be matched).
              s2 — the haystack to slide the window over.
    Output  : bool — true iff a permutation of s1 appears in s2.
    """

    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False  # window longer than the haystack → impossible

        # c1 : s1's letter multiset (fixed target).
        c1: List[int] = [0] * 26
        # c2 : current window's letter multiset.
        c2: List[int] = [0] * 26

        # Seed: count s1 fully and the first |s1| chars of s2.
        for i in range(len(s1)):
            c1[ord(s1[i]) - ord("a")] += 1
            c2[ord(s2[i]) - ord("a")] += 1

        # matches : #slots (0..25) where c1[i] == c2[i].
        # 26 matches ⇔ identical multisets ⇔ window is a permutation.
        matches = sum(1 for i in range(26) if c1[i] == c2[i])

        # Slide: the window is [i − |s1| + 1 .. i].
        for i in range(len(s1), len(s2)):
            if matches == 26:
                return True  # short-circuit BEFORE the next slide
            # Add the incoming char s2[i] to the window.
            add = ord(s2[i]) - ord("a")
            c2[add] += 1
            # The incoming char can only flip ITS slot's equality:
            # it now matches exactly when previously one short.
            if c2[add] == c1[add]:
                matches += 1
            elif c2[add] == c1[add] + 1:
                matches -= 1  # overshot by one → lost its equality
            # Remove the outgoing char s2[i − |s1|] from the window.
            rem = ord(s2[i - len(s1)]) - ord("a")
            c2[rem] -= 1
            # Mirror logic for the outgoing char.
            if c2[rem] == c1[rem]:
                matches += 1
            elif c2[rem] == c1[rem] - 1:
                matches -= 1
        # Final window is [|s2| − |s1| .. |s2|−1] — check it too.
        return matches == 26


# =====================================================================
# APPROACH 2 : Fixed window + Counter (dict) comparison (simpler)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return true if some contiguous window of `s2` is a
              permutation of `s1`.
    Inputs  : s1 — the needle (its multiset must be matched).
              s2 — the haystack to slide the window over.
    Output  : bool — true iff a permutation of s1 appears in s2.
    """

    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        # target : s1's full letter multiset.
        target: Counter[str] = Counter(s1)
        # window_count : the current length-|s1| window's multiset.
        window_count: Counter[str] = Counter(s2[: len(s1)])
        if window_count == target:
            return True  # the very first window already matches

        # Slide: drop the left char, add the right char, compare.
        for i in range(len(s1), len(s2)):
            window_count[s2[i]] += 1                  # add new char
            left = s2[i - len(s1)]
            window_count[left] -= 1
            if window_count[left] == 0:
                del window_count[left]   # keep sparse: zero-count keys
            if window_count == target:   # would still compare equal
                return True
        return False


# =====================================================================
# BENCHMARK — run both approaches on 3 tests + a longer pair,
# compare time and peak memory (tracemalloc), print PASS/FAIL.
# =====================================================================
if __name__ == "__main__":
    tests: List[Tuple[str, str, bool]] = [
        ("ab", "eidbaooo", True),   # "ba" at index 3 — official
        ("ab", "eidboaoo", False),  # 'a' and 'b' never adjacent — official
        ("adc", "dcda", True),      # "cda" is a permutation of "adc"
    ]

    all_pass = True
    for s1, s2, expected in tests:
        r1 = SolutionOne().checkInclusion(s1, s2)
        r2 = SolutionTwo().checkInclusion(s1, s2)
        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'} s1={s1!r} s2={s2!r} expected={expected}  matches={r1}  compare={r2}")

    # Longer adversarial pair: the needle appears only at the very end.
    bench_s1 = "abcdefghijklmnopqrstuvwxyz"
    bench_s2 = "".join("mnopqrstuvwxyzabcdefghijkl" for _ in range(40)) + bench_s1

    # --- Approach 1: time + peak memory ---
    tracemalloc.start()
    t0 = time.perf_counter()
    b1 = SolutionOne().checkInclusion(bench_s1, bench_s2)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t2 = time.perf_counter()
    b2 = SolutionTwo().checkInclusion(bench_s1, bench_s2)
    t3 = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (matches counter) : result={b1}  time={(t1 - t0) * 1e6:.2f} µs  peak-mem={peak_1} bytes")
    print(f"Approach 2 (counter compare) : result={b2}  time={(t3 - t2) * 1e6:.2f} µs  peak-mem={peak_2} bytes")

    all_pass = all_pass and (b1 == b2)
    print("PASS : all test cases and benchmark agree." if all_pass
          else "FAIL : at least one answer is wrong.")
