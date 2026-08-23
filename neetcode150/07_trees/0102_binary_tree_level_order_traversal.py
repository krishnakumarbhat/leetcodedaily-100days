"""
=====================================================================
LeetCode 102 : Binary Tree Level Order Traversal                  (Medium)
https://leetcode.com/problems/binary-tree-level-order-traversal/
Category   : Trees — BFS
---------------------------------------------------------------------
PROBLEM
    Given the root of a binary tree, return a list of lists: one
    list per LEVEL, listing that level's values left → right.
---------------------------------------------------------------------
INTUITION
    A level IS a frontier: the set of nodes at depth d. BFS processes
    the tree exactly one frontier at a time — if we snapshot the whole
    queue before expanding it, each snapshot is one output row. The
    queue is thus both the work list AND the level delimiter.
---------------------------------------------------------------------
APPROACH 1 — BFS with a per-level snapshot (BEST)
    At each iteration record size = len(queue), pop exactly `size`
    nodes into one row, enqueue their children for the next row.
    Time  Complexity : O(n)   Space Complexity : O(n) — queue holds
    at most a full level (worst: all leaves of a balanced tree).
---------------------------------------------------------------------
APPROACH 2 — DFS with depth-indexed rows (no queue at all)
    Recursively visit nodes carrying their depth; append each value
    into rows[depth] (growing the list on first visit to a depth).
    Same output, different traversal order (preorder instead of BFS).
    Time  Complexity : O(n)   Space Complexity : O(h) call stack +
    O(n) for the answer.
---------------------------------------------------------------------
DEEP DIVE — queue = the classic level-order machine
    FIFO is THE container for breadth-first walks: a node's children
    are appended AFTER everything already queued, so nodes at depth d
    are always processed before any node at depth d+1. Stacks would
    produce DFS instead. The "snapshot the size first" trick converts
    a FIFO stream into explicit level boundaries — the same pattern
    powers right-side view and zigzag traversal.
REAL LIFE
    • Renderers rasterize UI trees one depth (layer) at a time —
      exactly level order.
    • Social-graph analytics compute "friends of friends" by BFS
      levels; each level is a person's social circle at distance d.
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
# APPROACH 1 : BFS with per-level snapshots
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the tree's values level by level, left → right.
    Inputs  : root — the tree's root (may be None).
    Output  : list of rows; row i holds depth-i nodes' values.
    """

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        rows: List[List[int]] = []            # one list per level
        if root is None:
            return rows                       # empty tree → empty output

        pending = [root]                      # FIFO of the next frontier
        while pending:
            row: List[int] = []
            # Snapshot size BEFORE expanding: exactly this many nodes
            # form the current level — children join for the NEXT one.
            for _ in range(len(pending)):
                cur = pending.pop(0)
                row.append(cur.val)           # collect this level's value
                # Children are the next frontier — appended behind any
                # nodes of the CURRENT level still in the queue.
                if cur.left is not None:
                    pending.append(cur.left)
                if cur.right is not None:
                    pending.append(cur.right)
            rows.append(row)                  # commit the finished level
        return rows


# =====================================================================
# APPROACH 2 : DFS with depth-indexed rows
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the tree's values level by level, left → right.
    Inputs  : root — the tree's root (may be None).
    Output  : list of rows; row i holds depth-i nodes' values.
    """

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        rows: List[List[int]] = []
        self._walk(root, 0, rows)             # root sits at depth 0
        return rows

    def _walk(self, node: Optional[TreeNode], depth: int, rows: List[List[int]]) -> None:
        """Preorder visit carrying the node's depth; grows rows on first visit."""
        if node is None:
            return                            # no node → nothing to record
        # First visit to this depth → allocate its row.
        if depth == len(rows):
            rows.append([])
        rows[depth].append(node.val)          # preorder: root first
        self._walk(node.left, depth + 1, rows)
        self._walk(node.right, depth + 1, rows)


# =====================================================================
# BENCHMARK — both solutions on 3 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example → [[3],[9,20],[15,7]].
    t1 = buildTree([3, 9, 20, None, None, 15, 7])
    # Test 2: single node → [[1]].
    t2 = buildTree([1])
    # Test 3: skewed chain → one row per node.
    t3 = buildTree([1, 2, None, 3])
    expected = [[[3], [9, 20], [15, 7]], [[1]], [[1], [2], [3]]]
    trees = [t1, t2, t3]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().levelOrder(t) for t in trees]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().levelOrder(t) for t in trees]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(3):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1 rows={len(r1[i])} S2 rows={len(r2[i])} (expected {len(expected[i])}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (BFS snapshots)    : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (DFS + depth rows) : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : both produce the expected levels." if ok_all else "FAIL : at least one output differs.")