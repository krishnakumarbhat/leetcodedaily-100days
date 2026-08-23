"""
=====================================================================
LeetCode 105 : Construct Binary Tree from Preorder and Inorder    (Medium)
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder/
Category   : Trees — divide & conquer
---------------------------------------------------------------------
PROBLEM
    Given two integer lists — a tree's PREORDER and INORDER
    traversals (all values distinct) — reconstruct the original
    binary tree.
---------------------------------------------------------------------
INTUITION
    Preorder starts with the ROOT. That root splits inorder into
    [left subtree values][root][right subtree values] — and the two
    halves tell us EXACTLY how big the left/right subtrees are. Then
    each subtree is the same problem on smaller slices: divide and
    conquer all the way down. Every slice is identified by its
    (preorder range, inorder range) pair.
---------------------------------------------------------------------
APPROACH 1 — Hash map of inorder indices (BEST)
    Pre-scan inorder into a dict value→index so "how big is the left
    subtree?" is an O(1) arithmetic question: left_size =
    in_index[root] - in_left. Build slices recursively.
    Time  Complexity : O(n)   Space Complexity : O(n) map + O(h) stack.
    WHY THE MAP: every recursion step needs "where is this value in
    inorder?" A linear scan costs O(n) per step → O(n²) total. The
    map turns it into O(1). Python's dict does this with OPEN
    ADDRESSING / LINEAR PROBING:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    Collisions walk to the next free slot inside ONE contiguous array
    → excellent cache locality + tiny memory footprint.
---------------------------------------------------------------------
APPROACH 2 — No map: linear scan (conceptually simpler, slower)
    Identical recursion, but the inorder root is located by scanning
    the slice linearly each time.
    Time  Complexity : O(n²)   Space Complexity : O(h) — no map.
    WHY BOTHER: proves the map is what buys the O(n) bound; on small
    inputs both are equally fast, on skewed input A2 degrades.
---------------------------------------------------------------------
DEEP DIVE — slicing invariant
    Preorder range [pl, pr] and inorder range [il, ir] always describe
    the SAME subtree. root = pre[pl]. left subtree = pre[pl+1,
    pl+1+ls) × inorder [il, mid); right = pre[pl+1+ls, pr] × inorder
    (mid, ir]. Empty ranges → None. That is the whole algorithm —
    recursion is just the for-loop of divide & conquer.
REAL LIFE
    • Compilers rebuild ASTs from flat token streams — exactly this
      reconstruction, with grammar rules as the two "traversals".
    • File-system undelete tools re-assemble directory trees from
      two journal logs recorded in different orders.
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
# APPROACH 1 : Recursion + hash map of inorder indices
# =====================================================================
class SolutionOne:
    """
    Purpose : Rebuild a binary tree from its preorder + inorder.
    Inputs  : preorder, inorder — the two traversals (unique values).
    Output  : root of the reconstructed tree.
    """

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # value → index inside inorder: O(1) subtree-size arithmetic.
        in_index = {v: i for i, v in enumerate(inorder)}
        # Kick off the recursion over the FULL ranges of both lists.
        return self._build(preorder, 0, len(preorder) - 1,
                           inorder, 0, len(inorder) - 1, in_index)

    def _build(self, pre: List[int], pl: int, pr: int,
               ino: List[int], il: int, ir: int,
               in_index: dict) -> Optional[TreeNode]:
        """Build one subtree from aligned range slices (pl/pr × il/ir)."""
        # Empty slice → empty subtree (leaf sentinel of the recursion).
        if pl > pr or il > ir:
            return None
        # PREORDER's first element of the slice is always the root.
        root_val = pre[pl]
        root = TreeNode(root_val)
        # The root's inorder position splits the slice in two halves.
        mid = in_index[root_val]
        left_size = mid - il            # how many nodes sit left
        # Left subtree: pre[pl+1 .. pl+left_size] × in[il .. mid-1].
        root.left = self._build(pre, pl + 1, pl + left_size, ino, il, mid - 1, in_index)
        # Right subtree: pre[pl+1+left_size .. pr] × in[mid+1 .. ir].
        root.right = self._build(pre, pl + 1 + left_size, pr, ino, mid + 1, ir, in_index)
        return root


# =====================================================================
# APPROACH 2 : Same recursion, linear inorder scan (no map)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Rebuild a binary tree from its preorder + inorder.
    Inputs  : preorder, inorder — the two traversals (unique values).
    Output  : root of the reconstructed tree.
    Cost    : O(n²) worst — an O(slice) scan at every recursion level.
    """

    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        return self._build(preorder, 0, len(preorder) - 1,
                           inorder, 0, len(inorder) - 1)

    def _build(self, pre: List[int], pl: int, pr: int,
               ino: List[int], il: int, ir: int) -> Optional[TreeNode]:
        """Build one subtree; finds the inorder root by scanning linearly."""
        if pl > pr or il > ir:
            return None
        root_val = pre[pl]
        root = TreeNode(root_val)
        # Linear scan inside the inorder slice — the only difference
        # from approach 1, and the reason this is O(n²), not O(n).
        mid = il
        while ino[mid] != root_val:
            mid += 1
        left_size = mid - il
        root.left = self._build(pre, pl + 1, pl + left_size, ino, il, mid - 1)
        root.right = self._build(pre, pl + 1 + left_size, pr, ino, mid + 1, ir)
        return root


# =====================================================================
# BENCHMARK — both solutions on 3 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example → tree [3,9,20,null,null,15,7].
    pre1, ino1 = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
    # Test 2: single node.
    pre2, ino2 = [-1], [-1]
    # Test 3: right chain 1→2→3.
    pre3, ino3 = [1, 2, 3], [1, 2, 3]
    cases = [(pre1, ino1), (pre2, ino2), (pre3, ino3)]
    # Expected trees, built directly from level order for comparison.
    # Test 3: right chain 1→2→3 ⇔ level order [1,null,2,null,3].
    expected = [buildTree([3, 9, 20, None, None, 15, 7]), buildTree([-1]), buildTree([1, None, 2, None, 3])]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().buildTree(p, i) for p, i in cases]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().buildTree(p, i) for p, i in cases]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Round-trip verification: every reconstruction must equal the
    # expected tree built directly from level order.
    ok_all = True
    for i in range(3):
        ok = sameTree(r1[i], expected[i]) and sameTree(r2[i], expected[i])
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={printTree(r1[i])} S2={printTree(r2[i])} {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (hash map, O(n))    : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (linear scan, O(n²)): time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : reconstruction matches expected trees." if ok_all else "FAIL : reconstruction differs from expected.")