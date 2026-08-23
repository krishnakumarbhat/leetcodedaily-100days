"""
=====================================================================
LeetCode 104 : Maximum Depth of Binary Tree                         (Easy)
https://leetcode.com/problems/maximum-depth-of-binary-tree/
Category   : Trees — recursion fundamentals
---------------------------------------------------------------------
PROBLEM
    Given the root of a binary tree, return its MAXIMUM DEPTH — the
    number of nodes along the longest root→leaf path. (Empty tree = 0.)
---------------------------------------------------------------------
INTUITION
    The depth of a node is 1 + the deeper of its children's depths —
    a self-referential statement, so recursion is the natural fit:
    the base case (empty subtree → depth 0) stops the descent, and
    every level adds exactly one.
---------------------------------------------------------------------
APPROACH 1 — Recursive post-order (BEST, canonical)
    Ask both children for their depths, take the max, add 1 for the
    current node. The answer assembles itself bottom-up.
    Time  Complexity : O(n)   Space Complexity : O(h), h = height.
---------------------------------------------------------------------
APPROACH 2 — Iterative BFS (count the levels)
    Process level by level with a queue; every finished level adds 1
    to a counter. No recursion at all — depth = number of rows.
    Time  Complexity : O(n)   Space Complexity : O(w) — queue holds
    the widest level (≤ n).
---------------------------------------------------------------------
DEEP DIVE — the recursion POST-ORDER shape
    Computing a value from children BEFORE acting on the node itself
    is a post-order pattern: the child answers arrive first, the
    parent's answer composes them. This exact shape powers max path
    sum, diameter and balanced-tree checks — every "climb back up
    with a summary value" problem. Approach 2 sidesteps recursion
    entirely because BFS measures depth horizontally, one level at a
    time — no call stack, but O(n) worst-case queue memory instead
    of O(h).
REAL LIFE
    • HTML/DOM depth = the maximum nesting of tags a parser must
      track before it can unwind.
    • Call-stack auditing tools measure recursion depth of running
      programs — same question on the call tree.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
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
# APPROACH 1 : Recursive post-order
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the maximum depth of a tree.
    Inputs  : root — the tree's root (may be None).
    Output  : number of nodes on the longest root→leaf path.
    """

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # Empty subtree contributes zero levels — the recursion's base.
        if root is None:
            return 0
        # Ask both children, keep the taller one, add this node itself.
        # POST-ORDER: children are fully answered before the parent.
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return max(left_depth, right_depth) + 1


# =====================================================================
# APPROACH 2 : Iterative BFS — count the levels
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the maximum depth of a tree.
    Inputs  : root — the tree's root (may be None).
    Output  : number of nodes on the longest root→leaf path.
    """

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        pending = [root]                      # FIFO — the next frontier
        depth = 0
        # Each complete pass over the current queue = exactly one level.
        while pending:
            # Drain this level entirely; children queue up behind it.
            for _ in range(len(pending)):
                cur = pending.pop(0)
                if cur.left is not None:
                    pending.append(cur.left)
                if cur.right is not None:
                    pending.append(cur.right)
            depth += 1                        # one more level consumed
        return depth


# =====================================================================
# BENCHMARK — both solutions on 4 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example → depth 3.
    t1 = buildTree([3, 9, 20, None, None, 15, 7])
    # Test 2: single root → depth 1.
    t2 = buildTree([1])
    # Test 3: empty tree → depth 0.
    t3 = None
    # Test 4: left chain 1→2→3→4 → depth 4 (worst-case height).
    t4 = buildTree([1, 2, None, 3, None, None, 4])
    expected = [3, 1, 0, 4]
    trees = [t1, t2, t3, t4]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().maxDepth(t) for t in trees]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().maxDepth(t) for t in trees]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(4):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={r1[i]} S2={r2[i]} (expected {expected[i]}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (recursive post-order) : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (iterative BFS)        : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : all depths match expected." if ok_all else "FAIL : at least one depth is wrong.")