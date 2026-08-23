"""
=====================================================================
LeetCode 124 : Binary Tree Maximum Path Sum                       (Hard)
https://leetcode.com/problems/binary-tree-maximum-path-sum/
Category   : Trees — post-order info passing
---------------------------------------------------------------------
PROBLEM
    A PATH is any sequence of nodes connected by tree edges (can start
    and end ANYWHERE, may not visit a node twice). Return the LARGEST
    sum a path can collect. Node values may be negative.
---------------------------------------------------------------------
INTUITION
    Every path has a HIGHEST node (the one closest to the root).
    Decompose: at each node, the best path passing THROUGH it is
    bestDown(left) + node.val + bestDown(right), where bestDown is
    the best sum of a path that starts at a node and goes DOWN into
    one subtree. Only two facts must travel upward: the best down-sum
    through each child (to extend the parent's path) and the global
    best-so-far. Post-order = the child answers arrive before the
    parent composes them.
---------------------------------------------------------------------
APPROACH 1 — Post-order with best-so-far (BEST)
    dfs(node) returns the best single-branch down-sum through node;
    the caller updates a shared `best` with the full path through it.
    Negative branches are dropped (max(0, child)) — a path may simply
    not extend into a subtree that would shrink it.
    Time  Complexity : O(n)   Space Complexity : O(h), h = height.
---------------------------------------------------------------------
APPROACH 2 — Brute force, path-through-every-node (contrast)
    For every node compute the max down-sum through each child with a
    separate helper, then combine. Same idea, but each child's down-
    sum is recomputed for every ancestor.
    Time  Complexity : O(n²)  worst   Space Complexity : O(h).
    WHY SHOW IT: identical math, wildly different cost — the whole
    point of carrying info up instead of re-deriving it.
---------------------------------------------------------------------
DEEP DIVE — "return a summary, keep a global" (the tree-DP shape)
    dfs returning ONE value while a shared accumulator tracks the
    answer is the canonical Hard-tree pattern: the return value is
    the "legal to extend" summary (one branch only), the global is
    the "any shape" answer (both branches, no parent). Confusing the
    two is THE classic bug on this problem — a path can bend through
    the node (left + right) but can only EXTEND upward along one
    branch. Clamping child contributions at 0 is safe because an
    empty path is always allowed.
REAL LIFE
    • Network latency routing: the most valuable end-to-end route
      through a tree of routers is the same "best path through a
      node" DP with sums replaced by costs.
    • Circuit layout: longest viable trace between any two pads on a
      routing tree — same traversal, same combine rule.
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
# APPROACH 1 : Post-order, one down-sum per node, global best
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the maximum sum of any path in the tree.
    Inputs  : root — the tree's root (may be None).
    Output  : largest path sum; 0 for an empty tree.
    """

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.best = float("-inf")     # -∞: every node re-arms the max
        self._down_sum(root)
        return int(self.best)

    def _down_sum(self, node: Optional[TreeNode]) -> int:
        """Best single-branch path sum starting at `node`; folds the full
        left+node+right path into the global best."""
        # No node → contributes nothing to any path through its parent.
        if node is None:
            return 0
        # Children FIRST (post-order): their down-sums are ready here.
        # max(..., 0): a negative branch is better NOT extended into.
        left = max(0, self._down_sum(node.left))
        right = max(0, self._down_sum(node.right))
        # A path can BEND through this node: left leg + node + right leg.
        # That shape can never extend upward, so it only feeds `best`.
        self.best = max(self.best, left + node.val + right)
        # What we hand the PARENT: the better single leg through us.
        # One branch only — the parent's path must stay a simple chain.
        return node.val + max(left, right)


# =====================================================================
# APPROACH 2 : Brute force — re-derive each child's down-sum
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the maximum sum of any path in the tree.
    Inputs  : root — the tree's root (may be None).
    Output  : largest path sum; 0 for an empty tree.
    Cost    : O(n²) worst — down-sums are recomputed per ancestor.
    """

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        self.best = float("-inf")
        self._consider(root)          # every node as the path's peak
        return int(self.best)

    def _consider(self, node: Optional[TreeNode]) -> None:
        """Evaluate the best path whose highest node is `node`."""
        if node is None:
            return
        # Recomputes BOTH legs from scratch — the O(n) waste per node.
        left = max(0, self._down_sum(node.left))
        right = max(0, self._down_sum(node.right))
        self.best = max(self.best, left + node.val + right)
        self._consider(node.left)     # every node gets its turn
        self._consider(node.right)

    def _down_sum(self, node: Optional[TreeNode]) -> int:
        """Best downward-branch sum starting at `node`."""
        if node is None:
            return 0
        return node.val + max(self._down_sum(node.left), self._down_sum(node.right))


# =====================================================================
# BENCHMARK — both solutions on 3 tests: time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example → best path 4→2→1→3 = 6.
    t1 = buildTree([1, 2, 3])
    # Test 2: negative root, best path 15→20→7 = 42.
    t2 = buildTree([-10, 9, 20, None, None, 15, 7])
    # Test 3: all-negative chain → the largest single node (-1).
    t3 = buildTree([-3, -1, None, -2])
    expected = [6, 42, -1]
    trees = [t1, t2, t3]

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = [SolutionOne().maxPathSum(t) for t in trees]
    t1e = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = [SolutionTwo().maxPathSum(t) for t in trees]
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    ok_all = True
    for i in range(3):
        ok = r1[i] == expected[i] and r2[i] == expected[i]
        ok_all = ok_all and ok
        print(f"Test {i+1}: S1={r1[i]} S2={r2[i]} (expected {expected[i]}) {'PASS' if ok else 'FAIL'}")

    print(f"SolutionOne (post-order, O(n))    : time = {(t1e - t0) * 1e6:.2f} µs  peak-mem = {peak_1 / 1024:.1f} KB")
    print(f"SolutionTwo (brute force, O(n²))  : time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2 / 1024:.1f} KB")
    print("PASS : all path sums match expected." if ok_all else "FAIL : at least one path sum is wrong.")