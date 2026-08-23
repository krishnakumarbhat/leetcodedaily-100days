"""
=====================================================================
LeetCode 199 : Binary Tree Right Side View                        (Medium)
https://leetcode.com/problems/binary-tree-right-side-view/
Category   : Trees — BFS / level capture
---------------------------------------------------------------------
PROBLEM
    Imagine standing to the RIGHT of a binary tree: report, top to
    bottom, the value of the node you see at every level — i.e. the
    LAST node of each level (rightmost existing node).
---------------------------------------------------------------------
INTUITION
    A level's rightmost node is simply its LAST value when the level
    is collected left → right. Level-order BFS therefore answers the
    question almost for free: finish a level, take its tail.
    A DFS alternative: if we always walk RIGHT before LEFT, the FIRST
    node ever visited at a given depth is exactly its rightmost node.
---------------------------------------------------------------------
APPROACH 1 — BFS level snapshots (BEST, intuitive)
    Same per-level snapshot loop as level-order traversal; instead of
    storing the whole row, keep only its last element.
    Time  Complexity : O(n)   Space Complexity : O(n) — queue width.
---------------------------------------------------------------------
APPROACH 2 — DFS, right-first, first-visit-per-depth
    dfs(node, depth): if depth equals the count of levels recorded so
    far, this is the FIRST node seen at that depth → append it. Then
    recurse RIGHT first, LEFT second — rightmost wins the race.
    Time  Complexity : O(n)   Space Complexity : O(h), h = height.
---------------------------------------------------------------------
DEEP DIVE — same answer, two traversal philosophies
    BFS sees levels HORIZONTALLY (who is last in the row) — O(w)
    queue memory. DFS sees levels VERTICALLY (who is first to arrive
    at a depth) — O(h) stack memory. On a wide-but-shallow tree BFS
    costs more memory; on a narrow-but-deep tree DFS does. Both are
    O(n) time; the choice is which axis you want to pay for.
REAL LIFE
    • File explorers render the rightmost column of a directory tree
      (visible files) with exactly this logic.
    • Layout engines compute the "last visible element per depth" of
      a UI hierarchy — right side view in disguise.
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
# APPROACH 1 : BFS — keep the last node of every level
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the rightmost value of every level, top-down.
    Inputs  : root — the tree's root (may be None).
    Output  : list of the right side view, root first.
    """

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        view: List[int] = []
        if root is None:
            return view
        pending = [root]                      # FIFO — next frontier
        while pending:
            last_val = 0                      # will hold the row's tail
            for _ in range(len(pending)):
                cur = pending.pop(0)
                last_val = cur.val            # overwritten → ends as LAST
                if cur.left is not None:
                    pending.append(cur.left)
                if cur.right is not None:
                    pending.append(cur.right)
            view.append(last_val)             # rightmost node of the level
        return view


# =====================================================================
# APPROACH 2 : DFS right-first — first visit to a depth wins
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the rightmost value of every level, top-down.
    Inputs  : root — the tree's root (may be None).
    Output  : list of the right side view, root first.
    """

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        view: List[int] = []
        self._walk(root, 0, view)
        return view

    def _walk(self, node: Optional[TreeNode], depth: int, view: List[int]) -> None:
        """Right-first preorder; record the first node seen per depth."""
        if node is None:
            return
        # depth == len(view) ⇔ no node at this depth was visited yet
        # → THIS is the rightmost (we always descend right first).
        if depth == len(view):
            view.append(node.val)
        self._walk(node.right, depth + 1, view)   # right side has priority
        self._walk(node.left, depth + 1, view)    # left fills the gaps


# =====================================================================
# BENCHMARK — both solutions on 3 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example → [1,3,4].
    t1 = buildTree([1, 2, 3, None, 5, None, 4])
    # Test 2: single node → [1].
    t2 = buildTree([1])
    # Test 3: left chain 1→2→3 — only left nodes exist → [1,2,3].
    t3 = buildTree([1, 2, None, 3])
    expected = [[1, 3, 4], [1], [1, 2, 3]]
    trees = [t1, t2, t3]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().rightSideView(t) for t in trees]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().rightSideView(t) for t in trees]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(3):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={r1[i]} S2={r2[i]} (expected {expected[i]}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (BFS snapshots)     : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (DFS right-first)   : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : both views match expected." if ok_all else "FAIL : at least one view differs.")