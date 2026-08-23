"""
=====================================================================
LeetCode 110 : Balanced Binary Tree                                (Easy)
https://leetcode.com/problems/balanced-binary-tree/
Category   : Trees — post-order info passing
---------------------------------------------------------------------
PROBLEM
    Given the root of a binary tree, decide whether it is HEIGHT-
    BALANCED: for every node, the heights of its two subtrees differ
    by at most 1 — and both subtrees are themselves balanced.
---------------------------------------------------------------------
INTUITION
    "Balanced" needs two facts about each subtree: its HEIGHT (to
    compare siblings) and its BALANCEDNESS (to propagate up). Those
    are exactly the two values a single post-order pass can carry
    back: each node computes height = max(children) + 1 and flags
    itself unbalanced if |left_h - right_h| > 1 or either child was.
    One walk, both answers — no separate height recomputation.
---------------------------------------------------------------------
APPROACH 1 — Single post-order pass (BEST)
    dfs(node) returns the subtree height, or -1 as a sentinel meaning
    "unbalanced somewhere below". Every node is touched once.
    Time  Complexity : O(n)   Space Complexity : O(h), h = height.
---------------------------------------------------------------------
APPROACH 2 — Top-down double recursion (contrast)
    isBalanced(root) = |height(left) − height(right)| ≤ 1 AND
    balanced(left) AND balanced(right), recomputing height() per node.
    Time  Complexity : O(n²)  worst — height() re-walks subtrees for
    every ancestor (skewed chain: 1+2+…+n).  Space Complexity : O(h).
    WHY SHOW IT: the naive recursion looks identical but hides the
    O(n²) price — the classic "accidental quadratic".
---------------------------------------------------------------------
DEEP DIVE — post-order info passing (the tree-DP pattern)
    "Return a compact summary from each subtree, compose at the node"
    is the fundamental pattern of tree DP: max path sum, diameter,
    and balanced checks are ALL this. The summary is a PAIR here —
    (height, balanced) — encoded cleverly as a single int: height ≥ 0,
    or -1 meaning "imbalanced". One value, two meanings, zero extra
    structs. Approach 2 shows the cost of NOT passing info up: every
    level re-asks the same subtree questions it already knew the
    answer to.
REAL LIFE
    • Database indexes stay fast only while balanced — AVL/red-black
      trees rebalance on insert using exactly this check.
    • Compiler AST analyzers reject pathologically deep expressions
      (stack-overflow guardrails) with the same per-node test.
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
# APPROACH 1 : Single post-order pass, -1 sentinel for "unbalanced"
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether a tree is height-balanced.
    Inputs  : root — the tree's root (may be None).
    Output  : True iff every node's children differ by ≤ 1 in height
              and both subtrees are themselves balanced.
    """

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        # -1 from the walk = some subtree below was unbalanced.
        return self._height(root) != -1

    def _height(self, node: Optional[TreeNode]) -> int:
        """Post-order height probe with an imbalance sentinel (-1)."""
        # Empty subtree: height 0, trivially balanced.
        if node is None:
            return 0
        # Children first — the answers flow BOTTOM-UP.
        left_h = self._height(node.left)
        right_h = self._height(node.right)
        # A child reporting -1 propagates the verdict unchanged.
        if left_h == -1 or right_h == -1:
            return -1
        # The balance rule at THIS node: heights differ by at most 1.
        if abs(left_h - right_h) > 1:
            return -1
        # Balanced here: height = taller child + 1, passed upward.
        return max(left_h, right_h) + 1


# =====================================================================
# APPROACH 2 : Top-down — recompute height() at every node (O(n²))
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether a tree is height-balanced.
    Inputs  : root — the tree's root (may be None).
    Output  : True iff every node passes the |Δheight| ≤ 1 rule.
    Cost    : O(n²) worst — height() is recomputed for every ancestor.
    """

    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        # Empty tree is trivially balanced.
        if root is None:
            return True
        # Check the local rule at this node...
        if abs(self._height(root.left) - self._height(root.right)) > 1:
            return False
        # ...AND recurse into both children. The waste: height() is
        # recomputed for EVERY ancestor — O(n) per node → O(n²).
        return self.isBalanced(root.left) and self.isBalanced(root.right)

    def _height(self, node: Optional[TreeNode]) -> int:
        """Compute a subtree's height the plain recursive way."""
        if node is None:
            return 0
        return max(self._height(node.left), self._height(node.right)) + 1


# =====================================================================
# BENCHMARK — both solutions on 4 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: balanced example → True.
    t1 = buildTree([3, 9, 20, None, None, 15, 7])
    # Test 2: unbalanced (20's right leg 7→4 hangs 2 deeper) → False.
    t2 = buildTree([1, 2, 2, 3, 3, None, None, 4, 4])
    # Test 3: empty tree → True.
    t3 = None
    # Test 4: left chain 1→2→3 — height difference 2 at the root → False.
    t4 = buildTree([1, 2, None, 3])
    expected = [True, False, True, False]
    trees = [t1, t2, t3, t4]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().isBalanced(t) for t in trees]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().isBalanced(t) for t in trees]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(4):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={r1[i]} S2={r2[i]} (expected {expected[i]}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (post-order, O(n))    : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (top-down, O(n²))     : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : all verdicts match expected." if ok_all else "FAIL : at least one verdict is wrong.")