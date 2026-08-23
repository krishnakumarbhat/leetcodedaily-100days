"""
=====================================================================
LeetCode 155 : Min Stack                                       (Medium)
https://leetcode.com/problems/min-stack/
Category   : Stack (design)
---------------------------------------------------------------------
PROBLEM
    Design a stack supporting push, pop, top AND getMin — all in
    O(1) time. getMin returns the smallest value currently in the
    stack. The catch: O(1) getMin, not an O(n) scan on demand.
---------------------------------------------------------------------
INTUITION
    A plain stack cannot answer "what is the min?" in O(1) — the min
    can change arbitrarily when we pop. BUT the min at stack depth d
    only depends on values pushed at depth ≤ d. So keep a PARALLEL
    stack: at depth d it stores the min of everything pushed so far.
    When the main stack pops, the parallel stack pops with it — the
    min is always in sync because both stacks are the SAME depth.
---------------------------------------------------------------------
APPROACH 1 — Two parallel stacks (BEST)
    Main stack holds values; min stack holds the running minimum.
    push(v): push v; push min(min_top, v).
    pop():   pop BOTH stacks together (lockstep by design).
    getMin(): peek the min stack's top.
    Time  Complexity : O(1) for EVERY operation — nothing is scanned.
    Space Complexity : O(n) — two stacks, n entries each.
---------------------------------------------------------------------
APPROACH 2 — Single stack of (value, runningMin) pairs
    One stack; every element is a tuple (v, currentMin). Same logic,
    one physical stack, but each entry carries a second word.
    Time  Complexity : O(1)   Space Complexity : O(n)
---------------------------------------------------------------------
DEEP DIVE — the parallel-minimum invariant
    Invariant: after any sequence of ops, min_stack[-1] equals
    min(main_stack). Values in min_stack are NON-INCREASING from
    bottom to top (each push may only lower or keep the min). Because
    a pop removes the SAME depth from both stacks, the invariant
    survives every operation — this is why O(1) getMin is possible:
    the answer is precomputed per depth, not computed on demand.
---------------------------------------------------------------------
REAL LIFE
    • Undo-redo engines (editors, git): the "state at depth d" data
      structure — every pushed frame remembers its own snapshot.
    • Priority-aware pipelines: tracking the running min/max of a
      sliding data window (e.g. min latency seen so far in a log
      tailer) uses exactly this lockstep-stack trick.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from typing import List, Tuple

# =====================================================================
# APPROACH 1 : Two parallel stacks (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Stack with O(1) getMin via a parallel min stack.
    Inputs  : push(val) inserts val; pop() removes the top; top()
              reads the top value; getMin() reads the current min.
    Output  : methods mutate the stacks / return the asked value.
    """

    def __init__(self) -> None:
        self.stack: List[int] = []      # the real stack of values
        self.min_stack: List[int] = []  # running minimum at each depth

    def push(self, val: int) -> None:
        # Push v, and push the new running minimum alongside.
        self.stack.append(val)

        # Running min = min(previous min, this value). Empty min stack
        # → this value is trivially the min so far.
        new_min = val if not self.min_stack else min(self.min_stack[-1], val)
        self.min_stack.append(new_min)

    def pop(self) -> None:
        # Pop BOTH stacks — the depth must stay identical so the min
        # entry at the top always describes the main stack's depth.
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        # Peek the top value — main stack only.
        return self.stack[-1]

    def getMin(self) -> int:
        # The precomputed min at this depth — O(1), no scanning.
        return self.min_stack[-1]


# =====================================================================
# APPROACH 2 : Single stack of (value, runningMin) pairs
# =====================================================================
class SolutionTwo:
    """
    Purpose : Stack with O(1) getMin using one tuple stack.
    Inputs  : push(val) inserts val; pop() removes the top; top()
              reads the top value; getMin() reads the current min.
    Output  : methods mutate the stack / return the asked value.
    """

    def __init__(self) -> None:
        # Each entry: (value, minimumAtThisDepth).
        self.data: List[Tuple[int, int]] = []

    def push(self, val: int) -> None:
        # The tuple's second field mirrors approach 1's min stack.
        new_min = val if not self.data else min(self.data[-1][1], val)
        self.data.append((val, new_min))

    def pop(self) -> None:
        # Single stack → single pop; min sync is inside the pair.
        self.data.pop()

    def top(self) -> int:
        # First field of the top pair is the actual value.
        return self.data[-1][0]

    def getMin(self) -> int:
        # Second field of the top pair is the min at this depth.
        return self.data[-1][1]


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # --- Correctness: replay the official example 1 script ---
    # ops: push -2, push 0, push -3, getMin→-3, pop, top→0, getMin→-2
    s1 = SolutionOne()
    s2 = SolutionTwo()
    s1.push(-2); s2.push(-2)
    s1.push(0);  s2.push(0)
    s1.push(-3); s2.push(-3)

    ok1 = s1.getMin() == -3 and s2.getMin() == -3
    s1.pop(); s2.pop()
    ok2 = s1.top() == 0 and s2.top() == 0
    ok3 = s1.getMin() == -2 and s2.getMin() == -2

    # Extra stress: interleaved pops re-expose older minimums.
    s1.push(-5); s2.push(-5)
    ok4 = s1.getMin() == -5 and s2.getMin() == -5
    s1.pop(); s2.pop()
    ok5 = s1.getMin() == -2 and s2.getMin() == -2

    checks = [
        (ok1, "getMin after push(-3) == -3"),
        (ok2, "top() after pop == 0"),
        (ok3, "getMin after pop == -2"),
        (ok4, "getMin after push(-5) == -5"),
        (ok5, "getMin after popping -5 == -2")
    ]
    all_ok = all(ok for ok, _ in checks)
    for ok, label in checks:
        print(f"{'PASS' if ok else 'FAIL'} : {label}")

    # --- Benchmark: 200k mixed operations through both ---
    N = 200000

    def bench(sol) -> float:
        tracemalloc.start()
        t0 = time.perf_counter()
        for i in range(N):
            sol.push((i * 7919) % 1000000 - (1 if i % 3 == 0 else 0))
            if i % 4 == 0 and i > 0:   # never pop below empty at i=0
                sol.pop()
            if i % 16 == 0:
                sol.getMin()
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return (t1 - t0) * 1e6, peak

    us_1, peak_1 = bench(SolutionOne())
    us_2, peak_2 = bench(SolutionTwo())

    print(f"Approach 1 (two stacks)  : 200k ops  time = {us_1:.2f} µs"
          f"  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (tuple stack) : 200k ops  time = {us_2:.2f} µs"
          f"  peak-mem = {peak_2} bytes")

    print("PASS : all tests" if all_ok else "FAIL : a test was wrong")