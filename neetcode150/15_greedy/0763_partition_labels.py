"""
=====================================================================
LeetCode 763 : Partition Labels                              (Medium)
https://leetcode.com/problems/partition-labels/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    Split a lowercase string s into as MANY non-empty parts as
    possible such that every character appears in at most ONE part.
    Return the list of part lengths.
---------------------------------------------------------------------
INTUITION
    A part must be a SUFFIX of every character inside it: precompute
    last[c] = final occurrence. Sweeping, segEnd = max(last[·]) of
    the current part; i == segEnd is the EARLIEST safe cut. Earlier
    cuts leak characters (invalid); later cuts only merge parts
    (fewer parts). Earliest safe cut → maximal count → greedy exact.
---------------------------------------------------------------------
APPROACH 1 — Last-index map + sweep (BEST)
    Time  Complexity : O(n)   Space Complexity : O(1)
    (26 letters → constant-size last table.)
---------------------------------------------------------------------
APPROACH 2 — Merge per-character intervals
    Every character spans [first[c], last[c]]; sort the ≤26 intervals
    and merge overlapping ones (like "Merge Intervals"); emit merged
    lengths. Time O(n + k log k), k ≤ 26 → O(n) effective.
---------------------------------------------------------------------
DEEP DIVE — why the earliest safe cut is provably maximal
    Exchange argument: let O be any valid partition with first cut o.
    If o < e (= our first cut) then some char in [0, o] still occurs
    after o (else e ≤ o) → O's first part leaks → invalid. Every valid
    first cut is ≥ e, so cutting at e loses nothing; induction on the
    remainder makes greedy optimal for all cuts.
---------------------------------------------------------------------
REAL LIFE
    • Playlist splitting: group songs so an artist appears in one
      block (per-artist last index).
    • Log sharding: partition a log stream by key groups.
    • Database shard planning: split hot keys so each key lives in
      one shard.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Last-index table + sweep (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Return maximal partition lengths, one per part.
    Inputs  : s — lowercase string to partition.
    Output  : List[int] — length of each consecutive part.
    """

    def partitionLabels(self, s: str) -> List[int]:
        # last[c] = final occurrence index of character c.
        last = [-1] * 26
        for i, ch in enumerate(s):
            last[ord(ch) - 97] = i   # overwrite → ends at final spot

        parts: List[int] = []
        seg_start = 0  # left edge of the current part
        seg_end = 0    # furthest extent the current part must reach

        for i, ch in enumerate(s):
            seg_end = max(seg_end, last[ord(ch) - 97])  # must cover char's end

            if i == seg_end:
                # All chars in [seg_start, i] appeared → earliest safe
                # cut; later cuts only merge parts (fewer of them).
                parts.append(i - seg_start + 1)
                seg_start = i + 1   # next part starts right after
        return parts

# =====================================================================
# APPROACH 2 : Merge per-character intervals (≤26 intervals)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return maximal partition lengths, one per part.
    Inputs  : s — lowercase string to partition.
    Output  : List[int] — length of each consecutive part.
    """

    def partitionLabels(self, s: str) -> List[int]:
        first = [-1] * 26  # earliest occurrence per character
        last = [-1] * 26   # final occurrence per character
        for i, ch in enumerate(s):
            c = ord(ch) - 97
            if first[c] == -1:
                first[c] = i
            last[c] = i

        # Every character's span is an interval [first, last].
        intervals = sorted((first[c], last[c])
                           for c in range(26) if first[c] != -1)

        # Merge overlapping intervals — each merged block is one part.
        parts: List[int] = []
        cur_start, cur_end = intervals[0]
        for a, b in intervals[1:]:
            if a <= cur_end:
                cur_end = max(cur_end, b)   # overlapping → absorb
            else:
                parts.append(cur_end - cur_start + 1)  # close this part
                cur_start, cur_end = a, b
        parts.append(cur_end - cur_start + 1)          # close the last
        return parts


# =====================================================================
# BENCHMARK — both approaches, time + peak memory per approach
# =====================================================================
if __name__ == "__main__":
    # Official example + all-distinct + single char + repeated char.
    tests: List[str] = [
        "ababcbacadefegdehijhklij",  # → [9, 7, 8]
        "eccbbbbdec",                # → [10]
        "caedbdedda",                # → [1, 9]
        "a",                         # → [1]
        "abc",                       # → [1, 1, 1]
        "aaaa",                      # → [4]
    ]
    expected: List[List[int]] = [[9, 7, 8], [10], [1, 9], [1], [1, 1, 1], [4]]

    def run_all(solve) -> tuple[bool, float, int]:
        """Time one solver over every test; return (allPass, µs, peakBytes)."""
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = all(solve(t) == e for t, e in zip(tests, expected))
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return ok, (t1 - t0) * 1e6, peak

    ok1, us1, peak1 = run_all(lambda t: SolutionOne().partitionLabels(t))
    ok2, us2, peak2 = run_all(lambda t: SolutionTwo().partitionLabels(t))

    print(f"Approach 1 (last-index sweep): {'PASS' if ok1 else 'FAIL'}  time = {us1:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (interval merge)  : {'PASS' if ok2 else 'FAIL'}  time = {us2:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches produce the maximal partition."
          if ok1 and ok2
          else "FAIL : at least one approach is wrong.")
