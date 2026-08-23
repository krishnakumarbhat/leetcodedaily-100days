"""
=====================================================================
LeetCode 22 : Generate Parentheses                            (Medium)
https://leetcode.com/problems/generate-parentheses/
Category   : Stack / Backtracking
---------------------------------------------------------------------
PROBLEM
    Given an integer n, generate ALL well-formed combinations of n
    pairs of parentheses — every '(' must be closed by a later ')',
    and the count of ')' may never exceed the count of '(' while the
    string is being built left to right.
---------------------------------------------------------------------
INTUITION
    A partial string stays valid iff it never contains more ')' than
    '(' — i.e. open_count >= close_count ALWAYS. At every position
    there are at most two legal moves:
      • append '(' if open_count < n
      • append ')' if close_count < open_count
    Enumerating all legal move sequences is a DFS; the recursion
    depth is exactly 2n, and the call stack is a stack of partials.
---------------------------------------------------------------------
APPROACH 1 — Backtracking DFS (BEST)
    Recursively grow a string, only taking the two legal moves above,
    and record the string when it reaches length 2n. Every generated
    string is valid by construction — no filtering needed.
    Time  Complexity : O(4ⁿ/√n)   Space Complexity : O(n) recursion
---------------------------------------------------------------------
APPROACH 2 — Iterative BFS (explicit queue, no recursion)
    Same expansion, level by level: a deque of (string, opens,
    closes) grows every frontier simultaneously until length 2n.
    Time  Complexity : O(4ⁿ/√n)   Space Complexity : O(4ⁿ/√n)
---------------------------------------------------------------------
DEEP DIVE — the hidden stack
    Approach 1's stack is the CALL STACK (LIFO of partial strings);
    approach 2 swaps it for an explicit FIFO deque. DFS is standard:
    it keeps only O(n) partial strings in memory while BFS holds a
    whole level of the Catalan tree. The guard close < open is the
    invariant that makes every branch valid without backtracking.
---------------------------------------------------------------------
REAL LIFE
    • Parser generators (yacc/bison) enumerate valid derivations of
      a grammar exactly like this — one production per recursion.
    • Balanced-bracket code generation / test-case generators for
      compilers: every valid input shape must be enumerated.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from collections import deque
from typing import Deque, List, Tuple

# =====================================================================
# APPROACH 1 : Backtracking DFS (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Generate every well-formed combination of n pairs.
    Inputs  : n — number of '(' ')' pairs to generate (n >= 1).
    Output  : List of all valid strings, each of length 2n.
    """

    def generateParenthesis(self, n: int) -> List[str]:
        result: List[str] = []

        # Helper recurse: 'cur' is the string so far (always valid).
        # open / close count the parentheses already placed.
        def dfs(cur: str, open_count: int, close_count: int) -> None:
            # Length 2n → every pair used → this branch is complete.
            if len(cur) == 2 * n:
                result.append(cur)
                return  # no more moves possible from a full string

            # Legal move 1: open a new pair while budget remains.
            if open_count < n:
                dfs(cur + "(", open_count + 1, close_count)

            # Legal move 2: close an open pair — only if one is open.
            # This guard is the entire correctness argument.
            if close_count < open_count:
                dfs(cur + ")", open_count, close_count + 1)

        dfs("", 0, 0)
        return result


# =====================================================================
# APPROACH 2 : Iterative BFS (explicit queue)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Generate every well-formed combination of n pairs.
    Inputs  : n — number of '(' ')' pairs to generate (n >= 1).
    Output  : List of all valid strings, each of length 2n.
    """

    def generateParenthesis(self, n: int) -> List[str]:
        result: List[str] = []

        # Frontier entry: (partial string, opens used, closes used).
        frontier: Deque[Tuple[str, int, int]] = deque([("", 0, 0)])

        # Level-by-level expansion — identical rules to the DFS.
        while frontier:
            cur, open_count, close_count = frontier.popleft()

            # Full string → this leaf is a final answer.
            if len(cur) == 2 * n:
                result.append(cur)
                continue  # leaf: nothing else to expand

            # Same two legal moves as approach 1.
            if open_count < n:
                frontier.append((cur + "(", open_count + 1, close_count))
            if close_count < open_count:
                frontier.append((cur + ")", open_count, close_count + 1))

        return result


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Correctness tests: n = 1, 2, 3 (counts = Catalan numbers) ---
    ns = [1, 2, 3]
    expect = [1, 2, 5]  # Catalan numbers C_1..C_3
    all_ok = True
    for n, exp in zip(ns, expect):
        r1 = SolutionOne().generateParenthesis(n)
        r2 = SolutionTwo().generateParenthesis(n)
        ok = len(r1) == exp and len(r2) == exp
        if not ok:
            all_ok = False
        print(f"{'PASS' if ok else 'FAIL'} : n={n}  dfs-count={len(r1)}"
              f"  bfs-count={len(r2)}  expect={exp}")

    # --- Benchmark on n = 12 (≈ 20 million strings, noticeable) ---
    N = 12

    tracemalloc.start()
    t0 = time.perf_counter()
    rb1 = SolutionOne().generateParenthesis(N)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t0b = time.perf_counter()
    rb2 = SolutionTwo().generateParenthesis(N)
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (backtracking DFS) : {len(rb1)} strings"
          f"  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (iterative BFS)    : {len(rb2)} strings"
          f"  time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2} bytes")

    print("PASS : all tests" if all_ok else "FAIL : a test was wrong")
