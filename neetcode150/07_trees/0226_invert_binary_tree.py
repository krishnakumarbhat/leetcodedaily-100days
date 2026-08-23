"""
=====================================================================
LeetCode 226 : Invert Binary Tree                                   (Easy)
https://leetcode.com/problems/invert-binary-tree/
Category   : Trees — pointer surgery
---------------------------------------------------------------------
PROBLEM
    Given the root of a binary tree, INVERT it in place — mirror it
    horizontally: every node's left and right children swap. Return
    the root of the inverted tree.
---------------------------------------------------------------------
INTUITION
    Inversion is a per-node operation: swap the two child pointers,
    then invert both subtrees. Order does not matter — swap-then-
    recurse and recurse-then-swap produce the same mirror because the
    swap is independent at every node. That freedom lets us write it
    either recursively (implicit call stack) or with an explicit
    work list.
---------------------------------------------------------------------
APPROACH 1 — Recursive swap (BEST, 3 lines of essence)
    swap(node.left, node.right); invert(left); invert(right).
    Time  Complexity : O(n)   Space Complexity : O(h), h = height.
---------------------------------------------------------------------
APPROACH 2 — Iterative BFS/DFS with an explicit queue
    Same swaps, but a queue (or stack) holds the nodes still awaiting
    their swap — no recursion, safe on pathologically deep trees
    where the runtime stack would overflow.
    Time  Complexity : O(n)   Space Complexity : O(w), queue width.
---------------------------------------------------------------------
DEEP DIVE — pointer swaps ARE the mutation
    The tree is a set of heap nodes linked by pointers. "Inverting"
    changes NO node values and allocates NOTHING — it rewrites two
    pointers per node in place. That is why the operation is O(n)
    time and O(1) extra space per node; the recursion/queue memory is
    the only overhead. Watch the addresses stay fixed; only the
    arrows flip.
REAL LIFE
    • Rendering engines flip a UI tree horizontally (RTL layouts)
      with the same pointer-level swap on the widget hierarchy.
    • Image editors "flip horizontal" a picture's quad-tree of pixel
      blocks — identical recursion, identical swap.
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


def sameTree(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    """Structural equality helper used by the benchmark round-trip checks."""
    if a is None or b is None:
        return a is b
    return a.val == b.val and sameTree(a.left, b.left) and sameTree(a.right, b.right)


# =====================================================================
# APPROACH 1 : Recursive swap
# =====================================================================
class SolutionOne:
    """
    Purpose : Mirror the tree in place and return its root.
    Inputs  : root — the tree's root (may be None).
    Output  : root of the inverted (same) tree.
    """

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Empty subtree has nothing to mirror.
        if root is None:
            return None
        # Swap this node's children — the ONLY mutation the problem needs.
        root.left, root.right = root.right, root.left
        # Mirror both halves; order is irrelevant (independent swaps).
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root


# =====================================================================
# APPROACH 2 : Iterative — explicit FIFO of pending nodes
# =====================================================================
class SolutionTwo:
    """
    Purpose : Mirror the tree in place and return its root.
    Inputs  : root — the tree's root (may be None).
    Output  : root of the inverted (same) tree.
    """

    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        # The queue plays the role the call stack had in approach 1:
        # it remembers which subtrees still need their swap.
        pending = [root]
        while pending:
            cur = pending.pop(0)
            # Same pointer flip as before — explicit, visible, in place.
            cur.left, cur.right = cur.right, cur.left
            # Children now point at swapped subtrees; schedule both.
            if cur.left is not None:
                pending.append(cur.left)
            if cur.right is not None:
                pending.append(cur.right)
        return root


# =====================================================================
# BENCHMARK — both solutions on 3 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Each solution gets its OWN copy of every test tree — inversion
    # mutates in place, so sharing one tree would let the second
    # solution see the first one's output.
    # Test 1: official example → inverted [4,7,2,9,6,3,1].
    # Test 2: single node → unchanged [1].
    # Test 3: right chain 1→2→3 → becomes a LEFT chain [1,2,null,3].
    src = [[4, 2, 7, 1, 3, 6, 9], [1], [1, None, 2, None, 3]]
    expected = [buildTree([4, 7, 2, 9, 6, 3, 1]), buildTree([1]), buildTree([1, 2, None, 3])]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().invertTree(buildTree(s)) for s in src]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().invertTree(buildTree(s)) for s in src]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(3):
        ok = sameTree(r1[i], expected[i]) and sameTree(r2[i], expected[i])
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={printTree(r1[i])} S2={printTree(r2[i])} (expected {printTree(expected[i])}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (recursive)          : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (iterative queue)    : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : inverted trees match expected." if ok_all else "FAIL : inversion produced a wrong tree.")