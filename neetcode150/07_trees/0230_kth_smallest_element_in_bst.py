"""
=====================================================================
LeetCode 230 : Kth Smallest Element in a BST                      (Medium)
https://leetcode.com/problems/kth-smallest-element-in-a-bst/
Category   : Trees — inorder traversal
---------------------------------------------------------------------
PROBLEM
    Given the root of a binary SEARCH tree (unique values) and an
    integer k (1-based), return the k-th smallest value in the tree.
---------------------------------------------------------------------
INTUITION
    The defining property of a BST: an INORDER walk (left, node,
    right) visits values in ASCENDING order. So "the k-th smallest"
    is exactly "the k-th value emitted by an inorder walk" — and we
    can STOP the walk the instant the k-th value appears instead of
    traversing the rest of the tree.
---------------------------------------------------------------------
APPROACH 1 — Iterative inorder with early stop (BEST)
    Explicit stack descends the left spine, pops the smallest unseen
    value, counts it, then steps right. Stop at count == k.
    Time  Complexity : O(h + k) — spine descent + k pops.
    Space Complexity : O(h)     — explicit stack.
---------------------------------------------------------------------
APPROACH 2 — Recursive inorder with early stop
    Identical ordering, implicit call stack; the recursion returns a
    boolean "already found?" to unwind early.
    Time  Complexity : O(h + k) — same walk, same stop condition.
    Space Complexity : O(h)     — call stack.
---------------------------------------------------------------------
DEEP DIVE — why inorder ⇔ sorted for BSTs
    A BST stores every node's left subtree BELOW it and right subtree
    ABOVE it. Inorder emits left → node → right, so a value arrives
    only after everything smaller (left subtree) and before everything
    larger (right subtree) — induction over the whole tree gives a
    fully sorted sequence. Any "k-th" question about a BST is really
    an inorder question; the explicit-stack version is the classic
    interview answer because it makes the early stop visible.
REAL LIFE
    • Databases answer "the 50th percentile salary" with exactly
      this k-th inorder query on a B-tree index.
    • Streaming median algorithms keep BSTs and read the k-th element
      to split the stream in half.
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
# APPROACH 1 : Iterative inorder with an explicit stack
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the k-th smallest value in a BST.
    Inputs  : root — BST root; k — 1-based rank to find.
    Output  : the value that would appear k-th in sorted order.
    """

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        pending: List[TreeNode] = []   # explicit call-stack stand-in
        cur: Optional[TreeNode] = root
        visited = 0                    # values already emitted in order

        # Standard iterative inorder: left spine, visit, go right.
        while cur is not None or pending:
            # Descend the left spine — smallest unseen values live there.
            while cur is not None:
                pending.append(cur)
                cur = cur.left
            # Pop the next value in ascending order.
            cur = pending.pop()
            # Count it; the k-th one is the answer — stop RIGHT NOW,
            # the remaining (larger) values can stay unvisited.
            visited += 1
            if visited == k:
                return cur.val
            cur = cur.right            # continue with the right subtree
        return -1                      # k > tree size (never per spec)


# =====================================================================
# APPROACH 2 : Recursive inorder with early-stop unwinding
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the k-th smallest value in a BST.
    Inputs  : root — BST root; k — 1-based rank to find.
    Output  : the value that would appear k-th in sorted order.
    """

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.visited = 0               # reset per call (member state)
        return self._walk(root, k)

    def _walk(self, node: Optional[TreeNode], k: int) -> int:
        """Inorder recursion that stops as soon as k is reached."""
        if node is None:
            return -1                  # empty subtree holds nothing
        # LEFT first — smaller values always precede the node itself.
        from_left = self._walk(node.left, k)
        if from_left != -1:
            return from_left           # answer found below → unwind
        # Node itself is the next value in sorted order.
        self.visited += 1
        if self.visited == k:
            return node.val            # found → stop recursion cold
        # RIGHT last — larger values only.
        return self._walk(node.right, k)


# =====================================================================
# BENCHMARK — both solutions on 3 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example — [3,1,4,null,2], k=1 → 1.
    t1 = buildTree([3, 1, 4, None, 2])
    # Test 2: k=3 on the same tree → 3.
    # Test 3: BST [8,5,11,2,6,null,12] — sorted: 2,5,6,8,11,12;
    #         k=5 → 11.
    t3 = buildTree([8, 5, 11, 2, 6, None, 12])
    trees = [t1, t1, t3]
    ks = [1, 3, 5]
    expected = [1, 3, 11]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().kthSmallest(t, k) for t, k in zip(trees, ks)]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().kthSmallest(t, k) for t, k in zip(trees, ks)]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(3):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1} (k={ks[i]}): S1={r1[i]} S2={r2[i]} (expected {expected[i]}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (iterative inorder) : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (recursive inorder) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : both find the k-th smallest value." if ok_all else "FAIL : at least one answer is wrong.")