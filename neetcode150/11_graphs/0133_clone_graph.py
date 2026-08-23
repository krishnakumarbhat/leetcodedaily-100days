"""
=====================================================================
LeetCode 133 : Clone Graph                                       (Medium)
https://leetcode.com/problems/clone-graph/
Category   : Graphs
---------------------------------------------------------------------
PROBLEM
    Given a reference to a node in a CONNECTED undirected graph,
    return a deep copy: a brand-new graph with the same structure
    where every clone node holds a copy of the original's value and
    a neighbour list pointing to the CORRESPONDING clone nodes.
---------------------------------------------------------------------
INTUITION
    A graph is nodes + pointers. A deep copy must duplicate every
    node exactly once and rewire every pointer to the duplicate. The
    trap is SHARING: two neighbours pointing at the same node must
    map to ONE clone. A hash map `old -> clone` answers "already
    cloned?" in O(1) — it is the visited set AND the answer table.
---------------------------------------------------------------------
APPROACH 1 — Recursive DFS + hash map (BEST for clarity)
    clone(node): memoised. Store the fresh clone in the map BEFORE
    recursing so cycles self-resolve, then clone neighbours.
    Time  Complexity : O(V + E)   Space Complexity : O(V)
---------------------------------------------------------------------
APPROACH 2 — Iterative BFS + hash map
    Same memo table; a queue drives the traversal. No recursion depth
    risk; the frontier may hold O(V) nodes.
    Time  Complexity : O(V + E)   Space Complexity : O(V)
---------------------------------------------------------------------
DATA STRUCTURE DEEP DIVE — hash map as memoisation table
    Python dict = open addressing + LINEAR PROBING:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    colliding keys walk to the next free slot in ONE contiguous
    array → cache-friendly. C++ unordered_map = separate chaining
    (bucket of colliding keys). Both give O(1) average per op. The
    recursion is a DEEP COPY: allocations unwind on the call stack,
    every node is brand new — no aliasing with the original.
=====================================================================
REAL LIFE
    • Serialization / undo systems snapshot object graphs; snapshots
      are deep copies keyed by identity tables.
    • Git commit graphs, package dependency trees: "clone this
      subgraph" is a daily operation in build tooling.
    • GC / language runtimes clone heap graphs when forking sandbox
      processes (copy-on-write is an optimised deep copy).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import Dict, Optional, Set

# Graph node as given by LeetCode.
class Node:
    """Purpose : Graph node with value + neighbour list.
    Inputs  : val — integer node id.
    Output  : Node instance with empty neighbours list."""

    def __init__(self, val: int = 0, neighbors: Optional[list[Node]] = None) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

# =====================================================================
# APPROACH 1 : Recursive DFS + hash map (memoised deep copy)
# =====================================================================
class SolutionOne:
    """
    Purpose : Return a deep copy of a connected undirected graph.
    Inputs  : node — reference to any node of the original graph.
    Output  : Optional[Node] — root of the deep copy, None if empty.
    """

    def __init__(self) -> None:
        # memo : original node -> its clone. Acts as visited set AND
        # answer table in one dict.
        self.memo: Dict[Node, Node] = {}

    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:
        self.memo = {}                    # fresh memo table per call
        return self._clone(node)

    def _clone(self, node: Optional[Node]) -> Optional[Node]:
        # Memoisation guard: already cloned → return the SAME clone so
        # the copy keeps exactly one clone per original node.
        if node is None:
            return None
        if node in self.memo:
            return self.memo[node]

        # Allocate the clone, but STORE IT FIRST: a cycle pointing
        # back at `node` must find the clone already registered, or
        # the recursion never terminates.
        copy = Node(node.val)
        self.memo[node] = copy

        # Recursively clone every neighbour and attach the clones.
        for nb in node.neighbors:
            copy.neighbors.append(self._clone(nb))
        return copy

# =====================================================================
# APPROACH 2 : Iterative BFS + hash map
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return a deep copy of a connected undirected graph.
    Inputs  : node — reference to any node of the original graph.
    Output  : Optional[Node] — root of the deep copy, None if empty.
    """

    def cloneGraph(self, node: Optional[Node]) -> Optional[Node]:
        if node is None:
            return None

        # memo : original -> clone (visited set AND answer table).
        memo: Dict[Node, Node] = {}
        # Bootstrap: clone the root immediately.
        root_copy = Node(node.val)
        memo[node] = root_copy

        # BFS frontier over ORIGINAL nodes; clones are created on
        # first encounter, neighbour lists wired up on dequeue.
        queue = deque([node])
        while queue:
            cur = queue.popleft()
            for nb in cur.neighbors:
                # Clone each unvisited neighbour, then queue it so ITS
                # neighbours get wired later.
                if nb not in memo:
                    memo[nb] = Node(nb.val)
                    queue.append(nb)
                # Wire the clone of nb into the clone of cur. The memo
                # table guarantees shared nodes share one clone.
                memo[cur].neighbors.append(memo[nb])
        return root_copy

# =====================================================================
# BENCHMARK — build a small graph, clone with both, verify structure
# =====================================================================
if __name__ == "__main__":
    # Build the official test graph: 1-2, 1-4, 2-3, 3-4 (square).
    n1, n2, n3, n4 = Node(1), Node(2), Node(3), Node(4)
    n1.neighbors = [n2, n4]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]
    n4.neighbors = [n1, n3]
    originals: Set[Node] = {n1, n2, n3, n4}

    # --- Approach 1: time + peak memory ---
    tracemalloc.start()
    t0 = time.perf_counter()
    c1 = SolutionOne().cloneGraph(n1)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t2 = time.perf_counter()
    c2 = SolutionTwo().cloneGraph(n1)
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    def verify(root: Optional[Node]) -> bool:
        """Purpose : Confirm a clone is a 4-node deep copy.
        Inputs  : root — candidate clone root.
        Output  : bool — True if no aliasing and 4 distinct clones."""
        if root is None:
            return False
        seen: Set[Node] = set()
        queue = deque([root])
        seen.add(root)
        while queue:
            cur = queue.popleft()
            for nb in cur.neighbors:
                # Deep-copy contract: no neighbour may be an original
                # node (all clones must be fresh allocations).
                if nb in originals:
                    return False
                if nb not in seen:
                    seen.add(nb)
                    queue.append(nb)
        return len(seen) == 4

    ok1, ok2 = verify(c1), verify(c2)
    all_pass = ok1 and ok2
    print(f"Clone (A1 DFS)   : 4 nodes reachable, no aliasing → {'PASS' if ok1 else 'FAIL'}  time={(t1-t0)*1e6:.2f} µs  peak={peak1/1024:.1f} KB")
    print(f"Clone (A2 BFS)   : 4 nodes reachable, no aliasing → {'PASS' if ok2 else 'FAIL'}  time={(t3-t2)*1e6:.2f} µs  peak={peak2/1024:.1f} KB")
    print("PASS : deep copies structurally correct."
          if all_pass else "FAIL : at least one clone is wrong.")