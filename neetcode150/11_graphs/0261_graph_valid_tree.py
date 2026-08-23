"""
=====================================================================
LeetCode 261 : Graph Valid Tree                              (Medium)
https://leetcode.com/problems/graph-valid-tree/
Category   : Graphs
---------------------------------------------------------------------
PROBLEM
    Given n nodes labelled 0..n-1 and an edge list, decide whether
    the edges form a VALID TREE: connected AND acyclic.
---------------------------------------------------------------------
INTUITION
    Two structural facts decide everything:
      • A connected acyclic graph on n nodes has EXACTLY n−1 edges.
      • Connected + n−1 edges ⇔ acyclic (and vice versa).
    So "valid tree" ⇔ no cycle AND n−1 edges. Cycle detection in an
    UNDIRECTED graph: union-find (an edge joining two already-merged
    nodes closes a cycle) or DFS with a visited set + parent skip.
---------------------------------------------------------------------
APPROACH 1 — Union-Find with path compression (BEST)
    Merge endpoints of every edge. Edge with both endpoints ALREADY
    in one set → cycle → invalid. Require n−1 edges, no cycle, and
    one final component.
    Time  Complexity : O(n + E·α(n))  — α = inverse Ackermann,
                        effectively constant.
    Space Complexity : O(n)           — parent + rank arrays.
---------------------------------------------------------------------
APPROACH 2 — DFS from node 0
    Iterative DFS with (node, parent); revisit of a non-parent →
    cycle. Then verify every node was visited (connected).
    Time  Complexity : O(n + E)   Space Complexity : O(n + E)
---------------------------------------------------------------------
DATA STRUCTURE DEEP DIVE — union-find: path compression + rank
    parent[x] chains x to its component root; find() flattens the
    path; union() attaches the smaller-rank root under the larger.
    With both optimisations the amortised cost is the INVERSE
    ACKERMANN function α(n) — ≤ 4 for any practical n. Node labels
    are 0..n−1 so plain arrays index directly — no hash table needed
    (Python dict probing h(k,i)=(hash(k)+i) mod m is only for
    sparse/arbitrary labels).
=====================================================================
REAL LIFE
    • Network cabling: minimum viable mesh (tree) without loops —
      STP (Spanning Tree Protocol) keeps switches loop-free.
    • Git history is a DAG; "is this a tree?" = branch sanity checks.
    • Circuit design: detecting redundant/looping wires.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List

# =====================================================================
# APPROACH 1 : Union-Find — any edge closing a cycle kills the tree
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether the edges form a valid tree.
    Inputs  : n — node count; edges — undirected edge list.
    Output  : bool — true iff connected and acyclic.
    """

    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Tree on n nodes needs exactly n−1 edges — cheap early reject.
        if len(edges) != n - 1:
            return False

        # parent[i] = i : every node starts as its own component root.
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            # PATH COMPRESSION: walk to the root, flattening the chain
            # so the next lookup is near-O(1).
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # grandparent jump
                x = parent[x]
            return x

        def union(a: int, b: int) -> bool:
            # UNION BY RANK: attach shorter tree under taller root so
            # trees stay shallow.
            ra, rb = find(a), find(b)
            if ra == rb:
                return False               # already merged → cycle!
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[ra] > rank[rb]:
                parent[rb] = ra
            else:
                parent[rb] = ra            # equal ranks: attach + bump
                rank[ra] += 1
            return True

        components = n
        for a, b in edges:
            if not union(a, b):
                return False               # edge closes a cycle
            components -= 1
        # With n−1 successful merges all nodes share one component.
        return components == 1

# =====================================================================
# APPROACH 2 : DFS from node 0 — cycle + connectivity in one walk
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether the edges form a valid tree.
    Inputs  : n — node count; edges — undirected edge list.
    Output  : bool — true iff connected and acyclic.
    """

    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False

        # Adjacency list of the undirected graph.
        adj: List[List[int]] = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        # Iterative DFS with (node, parent). In an undirected graph
        # the ONLY way to revisit a node is (a) its parent via the
        # edge we came on — legal — or (b) a genuine cycle.
        visited = [False] * n
        stack = [(0, -1)]
        visited[0] = True
        seen = 1

        while stack:
            node, parent = stack.pop()
            for nb in adj[node]:
                if nb == parent:
                    continue               # the edge we came on
                if visited[nb]:
                    return False           # back edge → cycle
                visited[nb] = True
                seen += 1
                stack.append((nb, node))

        # Cycle-free AND every node reached → connected → valid tree.
        return seen == n

# =====================================================================
# BENCHMARK — run both approaches on 3 official-style tests
# =====================================================================
if __name__ == "__main__":
    # Test 1: star → true. Test 2: cycle 1-2-3-1 → false.
    # Test 3: two separate edges → false (disconnected).
    tests = [
        (5, [[0, 1], [0, 2], [0, 3], [1, 4]], True),
        (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], False),
        (4, [[0, 1], [2, 3]], False),
    ]

    all_pass = True
    for idx, (n, edges, expected) in enumerate(tests, start=1):
        # --- Approach 1: time + peak memory ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().validTree(n, edges)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + peak memory ---
        tracemalloc.start()
        t2 = time.perf_counter()
        r2 = SolutionTwo().validTree(n, edges)
        t3 = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == expected and r2 == expected and r1 == r2
        all_pass = all_pass and ok
        print(
            f"Test {idx} {'PASS' if ok else 'FAIL'} "
            f"| A1={r1} (expect {expected}) time={(t1-t0)*1e6:.2f} µs peak={peak1/1024:.1f} KB"
            f" | A2={r2} time={(t3-t2)*1e6:.2f} µs peak={peak2/1024:.1f} KB"
        )

    print("PASS : all tests green on both approaches."
          if all_pass else "FAIL : at least one test/approach disagrees.")