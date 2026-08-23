"""
=====================================================================
LeetCode 678 : Valid Parenthesis String                      (Medium)
https://leetcode.com/problems/valid-parenthesis-string/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    Given a string s of '(', ')' and '*' — where '*' may be '(', ')'
    or nothing — decide whether SOME assignment of the stars makes s
    a valid parentheses sequence.
---------------------------------------------------------------------
INTUITION
    The set of possible balance values after scanning a prefix is
    always ONE contiguous interval [lo, hi]. ')' shrinks it, '('
    grows it, '*' widens it (can be −1, 0, +1). Track only lo and hi:
    if hi < 0 → dead; if lo < 0 → clamp to 0; valid ⟺ lo == 0 at end.
---------------------------------------------------------------------
APPROACH 1 — Two-pass counter sweep (BEST, intuitive)
    Left→right with '*' as '(' : ')' must never be unmatched.
    Right→left with '*' as ')' : '(' must never be unmatched.
    Time  Complexity : O(n)   Space Complexity : O(1)
---------------------------------------------------------------------
APPROACH 2 — Min/max open-count interval (single pass)
    Time  Complexity : O(n)   Space Complexity : O(1)
    The two passes of Approach 1 are exactly the two extremes of this
    one interval walked separately.
---------------------------------------------------------------------
DEEP DIVE — why 2 numbers replace 3^m assignments
    Naive: enumerate 3^m star assignments. Greedy insight: balances
    form a contiguous interval because +1/−1/0 moves of a random walk
    fill every integer between min and max — no holes. Tracking
    [lo, hi] is an EXACT compression of the state set. Exchange
    argument: if any assignment works, the extreme assignments
    (stars-as-open / stars-as-close) survive every prefix, so the
    interval never dies.
---------------------------------------------------------------------
REAL LIFE
    • Regex / shell glob linting: validating patterns with wildcards
      before compiling them.
    • Compiler syntax analysis: bracket matching with optional tokens
      in grammar productions.
    • Text editors: live-validating unbalanced snippets while typing.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Two-pass counter sweep (best, intuitive)
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide if some assignment of '*' makes s valid.
    Inputs  : s — string of '(', ')' and '*'.
    Output  : bool — true if a valid assignment exists.
    """

    def checkValidString(self, s: str) -> bool:
        # LEFT pass: treat '*' as '(' — guarantees every ')' has an
        # earlier partner of some kind.
        balance = 0
        for c in s:
            balance += 1 if c in "(*" else -1  # star can open
            if balance < 0:
                return False                   # unmatched ')' → dead

        # RIGHT pass: treat '*' as ')' — guarantees every '(' has a
        # later partner of some kind.
        balance = 0
        for c in reversed(s):
            balance += 1 if c in ")*" else -1  # star can close
            if balance < 0:
                return False                   # unmatched '(' → dead
        return True                            # both directions pair up

# =====================================================================
# APPROACH 2 : Min/max open-count interval (single pass)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide if some assignment of '*' makes s valid.
    Inputs  : s — string of '(', ')' and '*'.
    Output  : bool — true if a valid assignment exists.
    """

    def checkValidString(self, s: str) -> bool:
        lo = 0  # minimum possible open-count (stars as ')'/empty)
        hi = 0  # maximum possible open-count (stars as '(')

        for c in s:
            if c == '(':
                lo, hi = lo + 1, hi + 1   # both bounds grow
            elif c == ')':
                lo, hi = lo - 1, hi - 1   # both bounds shrink
            else:
                lo, hi = lo - 1, hi + 1   # '*' widens the interval
            if hi < 0:
                return False              # even the maximum died
            lo = max(lo, 0)               # clamp: surplus closed
        return lo == 0                    # some assignment balances


# =====================================================================
# BENCHMARK — both approaches, time + peak memory per approach
# =====================================================================
if __name__ == "__main__":
    # Official examples + parity/edge cases (odd length = invalid).
    tests: List[str] = [
        "()",           # → True
        "(*)",          # → True
        "(*))",         # → True  (* = '(')
        "((((",         # → False (no closes)
        "((()))",       # → True
        "((*))",        # → True  (* = empty → (()) )
        "())(()",       # → False
        "*",            # → True  (star = empty)
        "***",          # → True  (all stars empty)
    ]
    expected = [True, True, True, False, True, True, False, True, True]

    def run_all(solve) -> tuple[bool, float, int]:
        """Time one solver over every test; return (allPass, µs, peakBytes)."""
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = all(solve(t) == e for t, e in zip(tests, expected))
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return ok, (t1 - t0) * 1e6, peak

    ok1, us1, peak1 = run_all(lambda t: SolutionOne().checkValidString(t))
    ok2, us2, peak2 = run_all(lambda t: SolutionTwo().checkValidString(t))

    print(f"Approach 1 (two-pass)      : {'PASS' if ok1 else 'FAIL'}  time = {us1:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (min/max range) : {'PASS' if ok2 else 'FAIL'}  time = {us2:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree on every test case."
          if ok1 and ok2
          else "FAIL : at least one approach is wrong.")
