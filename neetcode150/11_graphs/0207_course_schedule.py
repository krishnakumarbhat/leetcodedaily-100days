"""
=====================================================================
LeetCode 207 : Course Schedule                                 (Medium)
https://leetcode.com/problems/course-schedule/
Category   : Graphs
---------------------------------------------------------------------
PROBLEM
    You must take `numCourses` courses labelled 0..numCourses-1.
    Prerequisites are pairs [a, b] meaning "to take course a you
    must first finish b". Decide whether ALL courses can be finished
    — i.e. whether a valid ordering exists.
---------------------------------------------------------------------
INTUITION
    Courses are nodes; edge a → b means "a depends on b". A valid
    schedule exists ⇔ the directed graph has NO CYCLE (a cycle is a
    set of mutually dependent courses that can never be ordered).
    So: cycle detection on a directed graph — Kahn's algorithm (BFS
    on in-degrees) or DFS with 3-colour marking.
---------------------------------------------------------------------
APPROACH 1 — Kahn's algorithm (BEST, iterative)
    Count in-degrees (prerequisites per course). Repeatedly remove a
    course with in-degree 0 — "ready now". All n removed ⇔ acyclic.
    Time  Complexity : O(V + E)   Space Complexity : O(V + E)
---------------------------------------------------------------------
APPROACH 2 — DFS with colours (0=unvisited, 1=in-stack, 2=done)
    Hitting a node still ON the current stack (colour 1) = back edge
    = cycle. Colour 2 (finished) nodes are safe to skip.
    Time  Complexity : O(V + E)   Space Complexity : O(V + E)
---------------------------------------------------------------------
DATA STRUCTURE DEEP DIVE — cycle detection via colours
    A plain boolean visited array is NOT enough for directed graphs:
    a visited node may be finished (fine) or still on the current
    path (cycle!). The third state — "in progress" — distinguishes a
    BACK EDGE from a cross edge. Kahn's is iterative (no recursion
    risk) and produces the topological order as a by-product (210).
=====================================================================
REAL LIFE
    • Build systems (make, Bazel, Gradle): dependency graphs must be
      acyclic or the build deadlocks.
    • Package managers (npm, pip, apt): resolving install order and
      rejecting circular dependencies.
    • Curriculum planning, Git merge ordering, CPU instruction
      scheduling in compilers.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import List

# =====================================================================
# APPROACH 1 : Kahn's algorithm — peel in-degree-0 nodes
# =====================================================================
class SolutionOne:
    """
    Purpose : Decide whether all courses can be finished.
    Inputs  : numCourses — number of courses.
              prerequisites — [a, b] pairs: a needs b first.
    Output  : bool — true iff no cycle exists.
    """

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # adjacency : course -> its prerequisites (edges a → b).
        adj: List[List[int]] = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for a, b in prerequisites:
            adj[a].append(b)   # a depends on b
            indegree[b] += 1   # b has one more dependent

        # Ready queue: every course with NO remaining prerequisites.
        ready = deque(i for i in range(numCourses) if indegree[i] == 0)

        processed = 0  # how many courses were fully scheduled
        while ready:
            course = ready.popleft()
            processed += 1
            # Finishing `course` unblocks every course that listed it
            # as a prerequisite.
            for dep in adj[course]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    ready.append(dep)

        # A cycle leaves some course forever with in-degree > 0 →
        # fewer than numCourses get processed.
        return processed == numCourses

# =====================================================================
# APPROACH 2 : DFS with 3 colours — detect a back edge
# =====================================================================
class SolutionTwo:
    """
    Purpose : Decide whether all courses can be finished.
    Inputs  : numCourses — number of courses.
              prerequisites — [a, b] pairs: a needs b first.
    Output  : bool — true iff no cycle exists.
    """

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj: List[List[int]] = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            adj[a].append(b)
        # colour : 0 = unvisited, 1 = on stack, 2 = fully explored.
        colour = [0] * numCourses

        def dfs(v: int) -> bool:
            # Back edge: v is still ON the current DFS stack → cycle.
            if colour[v] == 1:
                return False
            # Fully explored before → provably no cycle in its subtree.
            if colour[v] == 2:
                return True
            colour[v] = 1             # enter: mark "in progress"
            for nb in adj[v]:
                if not dfs(nb):
                    return False
            colour[v] = 2             # exit: mark "done"
            return True

        # Every node seeds a DFS — the graph may be disconnected.
        return all(dfs(v) for v in range(numCourses))

# =====================================================================
# BENCHMARK — run both approaches on 3 official-style tests
# =====================================================================
if __name__ == "__main__":
    # Test 1 (official): 2, [[1,0]] → true. Test 2: mutual cycle → false.
    # Test 3: chain 0→1→2→3 → true.
    tests = [
        (2, [[1, 0]], True),
        (2, [[1, 0], [0, 1]], False),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),
    ]

    all_pass = True
    for idx, (n, pre, expected) in enumerate(tests, start=1):
        # --- Approach 1: time + peak memory ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().canFinish(n, pre)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + peak memory ---
        tracemalloc.start()
        t2 = time.perf_counter()
        r2 = SolutionTwo().canFinish(n, pre)
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