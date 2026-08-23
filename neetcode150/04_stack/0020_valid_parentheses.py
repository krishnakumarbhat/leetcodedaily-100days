"""
=====================================================================
LeetCode 20 : Valid Parentheses                                (Easy)
https://leetcode.com/problems/valid-parentheses/
Category   : Stack
---------------------------------------------------------------------
PROBLEM
    Given a string `s` made only of '(' ')' '{' '}' '[' ']', return
    true if the brackets are correctly nested: every opener must be
    closed by the SAME bracket type, and the most recently opened
    bracket must close first (LIFO — a stack).
---------------------------------------------------------------------
INTUITION
    "Most recent opener closes first" is exactly the stack contract.
    Push every opener; on a closer, the stack top must be its
    matching opener. Python dict answers "which opener matches this
    closer?" in O(1).
---------------------------------------------------------------------
APPROACH 1 — Stack + dict (BEST)
    Single pass. Closers are looked up in a dict and compared to the
    stack top; any mismatch (or a closer over an empty stack) is an
    immediate False. A valid string leaves the stack EMPTY.
    Time  Complexity : O(n)   Space Complexity : O(n)
---------------------------------------------------------------------
APPROACH 2 — Repeated pair erasure (no stack, no dict)
    Delete the substrings "()", "{}", "[]" from a working copy until
    it stops shrinking; valid ⇔ the result is empty.
    Time  Complexity : O(n²)   Space Complexity : O(n)
---------------------------------------------------------------------
DEEP DIVE — the matching dict
    Python dict = open addressing + linear probing:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    Collisions walk to the next free slot inside ONE contiguous array
    → cache locality + low memory. C++ std::unordered_map uses
    separate chaining instead. With only 3 keys either is overkill,
    but the dict keeps the matching rule declarative.
---------------------------------------------------------------------
REAL LIFE
    • Compilers / interpreters validate bracket nesting of code with
      this exact stack (LIFO = most recent scope closes first).
    • JSON/HTML parsers: mismatched delimiters are caught the same
      way — one stack, one pass.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import Dict, List

# =====================================================================
# APPROACH 1 : Stack + dict (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether the bracket string is correctly nested.
    Inputs  : s — string of '(' ')' '{' '}' '[' ']' characters only.
    Output  : True if every opener is closed in LIFO order by the
              same bracket type, False otherwise.
    """

    def isValid(self, s: str) -> bool:
        # match : closer -> the opener it must close (O(1) lookup).
        match: Dict[str, str] = {")": "(", "}": "{", "]": "["}

        # st : every not-yet-closed opener, most recent on top.
        st: List[str] = []

        # One linear pass — this is the entire O(n) walk.
        for c in s:

            # If this character IS a closer, look up its partner...
            if c in match:

                # ...and demand the stack top IS that partner.
                # Empty stack means the closer has nothing to close.
                if not st or st[-1] != match[c]:
                    return False   # wrong type or unmatched — fail fast
                st.pop()           # pair matched → remove the opener
            else:
                # Not a closer → it must be an opener → push it.
                st.append(c)

        # Every opener must have been matched → stack must be empty.
        return not st


# =====================================================================
# APPROACH 2 : Repeated pair erasure (no stack, no dict)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether the bracket string is correctly nested.
    Inputs  : s — string of '(' ')' '{' '}' '[' ']' characters only.
    Output  : True if erasing "()" "{}" "[]" pairs iteratively
              reduces the string to empty, False otherwise.
    """

    def isValid(self, s: str) -> bool:
        # Work on a mutable copy — the input must stay untouched.
        work = s

        # Loop until a full pass removes nothing (string is stable).
        # Each replacement pass is O(n); worst case n/2 passes → O(n²).
        while True:
            before = work
            for pair in ("()", "{}", "[]"):
                work = work.replace(pair, "")
            if work == before:
                break   # stable: fully balanced (empty) or invalid

        # Valid ⇔ all pairs were erased ⇔ nothing remains.
        return work == ""


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Correctness tests ---
    tests: List[tuple] = [
        ("()[]{}", True),   # every pair type, properly nested
        ("([)]", False),    # interleaved wrong nesting (classic trap)
        ("{[]}", True),     # nested pairs, LIFO order respected
        ("(]", False),      # mismatched types
        ("(((", False)      # unclosed openers
    ]

    all_ok = True
    for inp, expect in tests:
        r1 = SolutionOne().isValid(inp)
        r2 = SolutionTwo().isValid(inp)
        ok = r1 == expect and r2 == expect
        if not ok:
            all_ok = False
        print(f"{'PASS' if ok else 'FAIL'} : {inp!r}  stack={r1}"
              f"  erasure={r2}  expect={expect}")

    # --- Benchmark: worst-case-ish nesting "((((...))))" ---
    # (10k pairs: erasure is O(n²) in pure Python, so keep it modest)
    big = "(" * 10000 + ")" * 10000

    tracemalloc.start()
    t0 = time.perf_counter()
    rb1 = SolutionOne().isValid(big)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t0b = time.perf_counter()
    rb2 = SolutionTwo().isValid(big)
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (stack + dict) : {rb1}  time = {(t1 - t0) * 1e6:.2f} µs"
          f"  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (pair erasure) : {rb2}  time = {(t1b - t0b) * 1e6:.2f} µs"
          f"  peak-mem = {peak_2} bytes")

    print("PASS : all tests" if all_ok else "FAIL : a test was wrong")
