"""
=====================================================================
LeetCode 125 : Valid Palindrome                                  (Easy)
https://leetcode.com/problems/valid-palindrome/
Category   : Two Pointers
---------------------------------------------------------------------
PROBLEM
    Given a string s, return true if s is a PALINDROME after
    normalizing it: keep only alphanumeric characters and convert
    letters to lowercase. An empty string after normalization is a
    palindrome.
---------------------------------------------------------------------
INTUITION
    A palindrome reads identically from both ends. That symmetry is
    exactly what two pointers exploit: compare the leftmost relevant
    character against the rightmost relevant character, and if every
    such pair matches, the string is a palindrome. The O(n) scan is
    unavoidable because every character must be inspected at least
    once (any one of them could break the palindrome).
---------------------------------------------------------------------
APPROACH 1 — Two pointers with in-place normalization (BEST, O(1) space)
    l walks from the left, r from the right. Skip any non-alphanumeric
    character (punctuation, spaces) on either side, then compare
    s[l].lower() vs s[r].lower(). Any mismatch → false; pointers
    meet at the center → true.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Filter + reverse compare
    Build a cleaned string (keep alnum, lowercase), then check it
    against its reverse. Conceptually simplest — a palindrome equals
    its own reverse — but allocates a second copy of the string.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
DEEP DIVE — what "alphanumeric" really costs
    Python's str.isalnum() is NOT a single instruction: for letters
    and digits it runs a Unicode category lookup per character
    (checks bitmaps for digit/alpha categories). Still O(1) per
    character, so the overall O(n) bound survives. Mirroring the
    check on both sides (instead of cleaning the whole string first)
    is what buys Approach 1 its O(1) space: normalization happens
    lazily, one character at a time.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

# =====================================================================
# APPROACH 1 : Two pointers, skip junk on the fly (BEST)
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether s is a palindrome ignoring case/junk.
    Inputs  : s — the raw string, possibly with spaces/punctuation.
    Output  : bool — true if normalized s reads the same both ways.
    """

    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1

        while l < r:
            # Advance l past any character that does not count:
            # punctuation and spaces are invisible to the palindrome.
            while l < r and not s[l].isalnum():
                l += 1
            # Same for r, coming from the right.
            while l < r and not s[r].isalnum():
                r -= 1
            # Both pointers now sit on real letters/digits; compare them
            # case-insensitively. lower() makes 'A' and 'a' equal.
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True


# =====================================================================
# APPROACH 2 : Filter + compare against the reverse
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether s is a palindrome ignoring case/junk.
    Inputs  : s — the raw string, possibly with spaces/punctuation.
    Output  : bool — true if normalized s reads the same both ways.
    """

    def isPalindrome(self, s: str) -> bool:
        # Build the normalized string: alnum only, lowercased.
        # Cost: O(n) work + O(n) memory for the copy.
        clean = "".join(c.lower() for c in s if c.isalnum())
        # A palindrome is a string equal to its own reverse — compare.
        return clean == clean[::-1]


# =====================================================================
# BENCHMARK — verify both solutions on real test cases + time/RAM
# =====================================================================
if __name__ == "__main__":
    # Case 1: official example — spaces/punct/case all ignored → true.
    # Case 2: near-palindrome; first comparison at the ends already fails.
    # Case 3: digits count as alphanumeric → true.
    tests: List[Tuple[str, bool]] = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("0P0", True),
    ]

    # Aggregate time + peak memory across all cases, per approach.
    time_us: List[float] = [0.0, 0.0]
    peak_kb: List[float] = [0.0, 0.0]
    all_pass = True

    for t, (s, expected) in enumerate(tests, 1):
        # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().isPalindrome(s)
        t1 = time.perf_counter()
        _, peak_1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[0] += (t1 - t0) * 1e6
        peak_kb[0] = max(peak_kb[0], peak_1 / 1024.0)

        # --- Approach 2: same instrumentation ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().isPalindrome(s)
        t1b = time.perf_counter()
        _, peak_2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[1] += (t1b - t0b) * 1e6
        peak_kb[1] = max(peak_kb[1], peak_2 / 1024.0)

        ok = (r1 == expected) and (r2 == expected)
        all_pass = all_pass and ok
        print(f"Test {t}: twoPtr={r1} filter={r2} expected={expected}  {'PASS' if ok else 'FAIL'}")

    print("---")
    print(f"Approach 1 (two pointers)     : {time_us[0]:.2f} µs total, peak {peak_kb[0]:.2f} KB")
    print(f"Approach 2 (filter + reverse) : {time_us[1]:.2f} µs total, peak {peak_kb[1]:.2f} KB")
    print("PASS : all cases" if all_pass else "FAIL : at least one case")