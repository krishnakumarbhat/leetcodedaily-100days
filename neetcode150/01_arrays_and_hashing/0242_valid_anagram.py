"""
=====================================================================
LeetCode 242 : Valid Anagram                                    (Easy)
https://leetcode.com/problems/valid-anagram/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Given two strings s and t, return true if t is an anagram of s
    (same letters, same counts, any order), false otherwise.
---------------------------------------------------------------------
INTUITION
    An anagram is a multiset equality: letter→count must match for
    both strings. Count letters of s, subtract counts of t, and
    check that everything returns to zero.
---------------------------------------------------------------------
APPROACH 1 — Fixed-size frequency array (BEST)
    Only 26 lowercase letters → a list of 26 ints. Index = ord(c)-97.
    Time  Complexity : O(n)   Space Complexity : O(1)  (26 slots!)
    WHY better than dict/Counter: the key space is tiny and fixed,
    so a plain list is faster AND smaller — no hashing, no probing,
    perfect cache locality. Counter is a dict subclass (open
    addressing, linear probing) — overkill for 26 possible keys.
---------------------------------------------------------------------
APPROACH 2 — Sort both strings
    Time  Complexity : O(n log n)   Space Complexity : O(1).
    Canonical form of an anagram is its sorted self.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc


# =====================================================================
# APPROACH 1 : Frequency array of 26 counters
# =====================================================================
class Solution_FreqArray:
    """
    Purpose : Decide whether t is an anagram of s.
    Inputs  : s, t — the two strings to compare.
    Output  : True when both hold identical letter multiset.
    """

    def isAnagram(self, s: str, t: str) -> bool:
        # Different lengths can never be anagrams — cheap early exit.
        if len(s) != len(t):
            return False

        # count[0..25] : occurrences of 'a'..'z'. 26 ints → O(1) space.
        count = [0] * 26

        # One pass: credit s's letters, debit t's letters.
        for i in range(len(s)):
            # ord(c) - ord('a') maps 'a'→0 … 'z'→25 — no hash needed.
            count[ord(s[i]) - ord('a')] += 1
            count[ord(t[i]) - ord('a')] -= 1

        # If every bucket is back to zero → the multiset matched.
        for c in count:
            if c != 0:
                return False
        return True


# =====================================================================
# APPROACH 2 : Sort both strings and compare
# =====================================================================
class Solution_SortCompare:
    """
    Purpose : Decide whether t is an anagram of s.
    Inputs  : s, t — the two strings to compare.
    Output  : True when both hold identical letter multiset.
    """

    def isAnagram(self, s: str, t: str) -> bool:
        # Sorting rearranges an anagram into the SAME canonical order.
        # Timsort (Python's sort) is O(n log n) worst case, O(n) on
        # nearly-sorted input.
        return sorted(s) == sorted(t)


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    s, t = "anagram", "nagaram"

    # --- Approach 1 ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_FreqArray().isAnagram(s, t)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2 ---
    tracemalloc.start()
    t2 = time.perf_counter()
    r2 = Solution_SortCompare().isAnagram(s, t)
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (freq array [26]) : {r1}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (sort + compare)  : {r2}  time = {(t3 - t2) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree." if r1 == r2 else "FAIL : approaches disagree.")