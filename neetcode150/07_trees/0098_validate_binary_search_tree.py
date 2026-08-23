"""
=====================================================================
LeetCode 98 : Validate Binary Search Tree                        (Medium)
https://leetcode.com/problems/validate-binary-search-tree/
Category   : Trees — BST property
---------------------------------------------------------------------
PROBLEM
    Given the root of a binary tree, decide whether it is a VALID
    binary search tree (BST). For EVERY node:
      • its left subtree holds only values STRICTLY LESS than it,
      • its right subtree holds only values STRICTLY GREATER than it,
      • both subtrees are themselves valid BSTs. No duplicates.
---------------------------------------------------------------------
INTUITION
    Checking only direct children is WRONG: [5,4,6,null,null,3,7]
    passes that test, yet 3 sits in 5's RIGHT subtree with 3 < 5.
    The correct rule: every node carries an allowed interval (lo, hi)
    inherited from its ancestors — going LEFT replaces hi by the
    parent's value, going RIGHT replaces lo. A node is valid iff its
    value lies strictly inside its inherited interval.
---------------------------------------------------------------------
APPROACH 1 — Recursive interval propagation (BEST)
    DFS down the tree carrying (lo, hi); each node must satisfy
    lo < val < hi. ±inf floats give the root no constraints.
    Time  Complexity : O(n)   Space Complexity : O(h), h = height.
---------------------------------------------------------------------
APPROACH 2 — Iterative inorder (must be strictly ascending)
    A BST's inorder walk emits values in STRICTLY increasing order —
    and only a BST does. Walk iteratively with an explicit stack;
    if the current value is <= the previous one → not a BST.
    Time  Complexity : O(n)   Space Complexity : O(h).
---------------------------------------------------------------------
DEEP DIVE — recursion = the implicit call stack
    Every function call pushes a FRAME (locals + return address) onto
    the call stack; the frame pops when the callee returns. Recursive
    tree code therefore costs O(h) extra memory — one frame per
    ancestor still on the current path. Approach 1 lets the runtime
    maintain that stack invisibly; Approach 2 builds the SAME stack
    by hand with a list. Identical memory behaviour — recursion just
    hides the bookkeeping, which is why tree code prefers it.
REAL LIFE
    • Databases validate index keys against B-tree ordering rules —
      the same interval-propagation check.
    • Binary-search-tree autocomplete: a broken ordering silently
      corrupts every search; validation guards the structure.
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
    # Empty input (or null root) → empty tree → allocate nothing.
    if not vals or vals[0] is None:
        return None
    # Slot 0 is the root; BFS replays the level-order list afterwards.
    root = TreeNode(vals[0])
    pending = [root]
    i = 1
    while pending and i < len(vals):
        cur = pending.pop(0)          # oldest unfilled parent
        # Next slot = left child; None means the child simply is absent.
        if i < len(vals) and vals[i] is not None:
            cur.left = TreeNode(vals[i])
            pending.append(cur.left)
        i += 1
        # Following slot = right child of the same parent.
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
        # Missing children are queued as None — same convention as input.
        if cur is not None:
            pending.append(cur.left)
            pending.append(cur.right)
    return "[" + ",".join(out) + "]"


# =====================================================================
# APPROACH 1 : Recursive interval propagation
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether a tree is a valid BST.
    Inputs  : root — the tree's root (may be None).
    Output  : True iff every node lies strictly inside the interval
              inherited from its ancestors.
    """

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # Root has no constraints: ±infinity both ways.
        return self._validate(root, float("-inf"), float("inf"))

    def _validate(self, node: Optional[TreeNode], lo: float, hi: float) -> bool:
        """Check the subtree at `node` against the inherited interval (lo, hi)."""
        # Empty subtree cannot violate anything — the recursion's base.
        if node is None:
            return True
        # The node's own value must be strictly inside its interval.
        if not (lo < node.val < hi):
            return False
        # LEFT is bounded above by this value, RIGHT below by it.
        return self._validate(node.left, lo, node.val) and self._validate(node.right, node.val, hi)


# =====================================================================
# APPROACH 2 : Iterative inorder — values must be strictly ascending
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether a tree is a valid BST via inorder walk.
    Inputs  : root — the tree's root (may be None).
    Output  : True iff the inorder traversal is strictly increasing.
    """

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # Explicit stack replaces the call stack: nodes whose RIGHT
        # subtree is still pending live here.
        pending: List[TreeNode] = []
        cur: Optional[TreeNode] = root
        prev: Optional[TreeNode] = None   # last value emitted by the walk

        # Classic iterative inorder: descend left, visit, go right.
        while cur is not None or pending:
            # Push the whole left spine; these are visited later.
            while cur is not None:
                pending.append(cur)
                cur = cur.left
            # Pop the deepest unvisited node — the next inorder value.
            cur = pending.pop()
            # Inorder must be strictly ascending; equality = duplicate
            # = violation of the BST property.
            if prev is not None and prev.val >= cur.val:
                return False
            prev = cur
            # After visiting a node, walk its right subtree (or climb
            # back up — the stack holds the ancestors).
            cur = cur.right
        return True


# =====================================================================
# BENCHMARK — both solutions on 3 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test trees (level-order = LeetCode's "[a,b,c,null,...]" format).
    # t1: 2's right subtree contains 3 (which is < 5) → INVALID.
    t1 = buildTree([5, 1, 4, None, None, 3, 6])
    # t2: classic valid BST.
    t2 = buildTree([2, 1, 3])
    # t3: the famous trap — 3 < 5 but sits in the RIGHT subtree → INVALID.
    t3 = buildTree([5, 4, 6, None, None, 3, 7])
    expected = [False, True, False]
    trees = [t1, t2, t3]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().isValidBST(t) for t in trees]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().isValidBST(t) for t in trees]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Per-test verdicts, printed compactly.
    ok_all = True
    for i in range(3):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={r1[i]} S2={r2[i]} (expected {expected[i]}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (recursive intervals): time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (iterative inorder)  : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : all verdicts match expected." if ok_all else "FAIL : at least one verdict is wrong.")