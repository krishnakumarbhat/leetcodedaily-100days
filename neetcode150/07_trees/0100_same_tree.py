"""
=====================================================================
LeetCode 100 : Same Tree                                            (Easy)
https://leetcode.com/problems/same-tree/
Category   : Trees — structural equality
---------------------------------------------------------------------
PROBLEM
    Given the roots of two binary trees p and q, decide whether they
    are the SAME tree: identical structure AND identical values at
    every position.
---------------------------------------------------------------------
INTUITION
    "Same" decomposes recursively: the two roots must hold equal
    values AND their left subtrees must be the same AND their right
    subtrees must be the same. A null mismatch (one side empty, the
    other not) is the only structural failure — and it terminates the
    recursion without ever comparing values.
---------------------------------------------------------------------
APPROACH 1 — Recursive equality (BEST, clearest)
    Three base cases (both None → True; one None → False; values
    differ → False), then recurse into both child pairs.
    Time  Complexity : O(min(n, m)) — stops at the first mismatch.
    Space Complexity : O(h)         — call stack depth.
---------------------------------------------------------------------
APPROACH 2 — Iterative BFS (queue of node pairs)
    Same logic, but the work is held in an explicit FIFO queue of
    (p, q) pairs instead of the call stack — a flat loop, immune to
    deep-recursion stack overflow on skewed trees.
    Time  Complexity : O(min(n, m)) — each pair dequeued once.
    Space Complexity : O(w)         — queue width at the widest level.
---------------------------------------------------------------------
DEEP DIVE — why BOTH approaches are "the same algorithm"
    Recursive DFS and iterative BFS explore in different ORDERS but
    compare exactly the same pairs of nodes. The choice is about the
    container: the call stack (A1) vs an explicit queue (A2). For an
    O(n) tree walk either is fine; the queue version shines when the
    tree is so deep that recursion would blow the runtime stack.
REAL LIFE
    • Version-control diff tools compare directory trees this way —
      node = file, children = subdirectories.
    • Regression testers compare ASTs (abstract syntax trees) of
      refactored code with the identical walk.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
from collections import deque
from typing import List, Optional


class TreeNode:
    """One binary-tree node: a value plus pointers to two children."""

    def __init__(self, val: int = 0, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None) -> None:
        # Children default to None — a leaf is just a bare value.
        self.val = val
        self.left = left
        self.right = right


def buildTree(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a real tree from LeetCode's level-order list (None = missing child)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    pending = [root]
    i = 1
    while pending and i < len(vals):
        cur = pending.pop(0)          # oldest unfilled parent
        if i < len(vals) and vals[i] is not None:
            cur.left = TreeNode(vals[i])
            pending.append(cur.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            cur.right = TreeNode(vals[i])
            pending.append(cur.right)
        i += 1
    return root


def printTree(root: Optional[TreeNode]) -> str:
    """Level-order list of the tree, mirroring the buildTree input format."""
    if root is None:
        return "[]"
    out: List[str] = []
    pending = [root]
    while pending:
        cur = pending.pop(0)
        out.append("null" if cur is None else str(cur.val))
        if cur is not None:
            pending.append(cur.left)
            pending.append(cur.right)
    return "[" + ",".join(out) + "]"


# =====================================================================
# APPROACH 1 : Recursive equality
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether two trees are structurally identical.
    Inputs  : p, q — roots of the two trees (either may be None).
    Output  : True iff structure and every value match.
    """

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # Both empty → nothing to compare → same.
        if p is None and q is None:
            return True
        # Exactly one empty → structure differs → not the same.
        if p is None or q is None:
            return False
        # Roots differ → not the same. Short-circuits the whole walk.
        if p.val != q.val:
            return False
        # Both halves must match — the recursive definition of "same".
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


# =====================================================================
# APPROACH 2 : Iterative BFS — deque of (p, q) pairs
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether two trees are structurally identical.
    Inputs  : p, q — roots of the two trees (either may be None).
    Output  : True iff structure and every value match.
    """

    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # FIFO of node pairs still waiting to be compared level by level.
        pending: deque = deque([(p, q)])
        while pending:
            a, b = pending.popleft()
            # Both None → this pair matches, nothing more to enqueue.
            if a is None and b is None:
                continue
            # One None, or two different values → structural mismatch.
            if a is None or b is None or a.val != b.val:
                return False
            # Matching pair → compare their children in the same way.
            pending.append((a.left, b.left))
            pending.append((a.right, b.right))
        return True


# =====================================================================
# BENCHMARK — both solutions on 3 test pairs: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: identical trees → True.
    p1, q1 = buildTree([1, 2, 3]), buildTree([1, 2, 3])
    # Test 2: same root, different right child → False.
    p2, q2 = buildTree([1, 2, 3]), buildTree([1, 2, None])
    # Test 3: mirrored structure, different values → False.
    p3, q3 = buildTree([1, 2, 1]), buildTree([1, 1, 2])
    expected = [True, False, False]
    pairs = [(p1, q1), (p2, q2), (p3, q3)]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().isSameTree(p, q) for p, q in pairs]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().isSameTree(p, q) for p, q in pairs]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(3):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={r1[i]} S2={r2[i]} (expected {expected[i]}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (recursive)     : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (iterative BFS) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : all verdicts match expected." if ok_all else "FAIL : at least one verdict is wrong.")