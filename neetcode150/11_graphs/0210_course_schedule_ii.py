"""
=====================================================================
LeetCode 210 : Course Schedule II                             (Medium)
https://leetcode.com/problems/course-schedule-ii/
Category   : Graphs
---------------------------------------------------------------------
PROBLEM
    Same setup as 207, but now RETURN one valid order of taking all
    `numCourses` courses, or an empty array if a cycle makes it
    impossible.
---------------------------------------------------------------------
INTUITION
    The requested order is a TOPOLOGICAL ORDER: every prerequisite
    edge a → b puts b before a. Kahn's algorithm produces it
    naturally — the order courses leave the ready queue. DFS produces
    the REVERSE of finish time — prepending each node when it is
    marked "done" yields a valid topological order.
---------------------------------------------------------------------
APPROACH 1 — Kahn's algorithm (BEST)
    In-degree array + queue of "ready" courses; dequeue order IS the
    answer. Fewer than n courses output ⇒ cycle ⇒ return [].
    Time  Complexity : O(V + E)   Space Complexity : O(V + E)
---------------------------------------------------------------------
APPROACH 2 — DFS (post-order prepending)
    Colour DFS; when a node finishes (colour 2) prepend it to the
    answer. Detecting a back edge aborts with an empty array.
    Time  Complexity : O(V + E)   Space Complexity : O(V + E)
---------------------------------------------------------------------
DATA STRUCTURE DEEP DIVE — Kahn's vs DFS for topological sort
    Kahn's: BFS-like, iterative, the in-degree array is the "remaining
    dependencies" book. DFS: recursion — children always finish before
    their parent, so prepending on exit keeps prerequisites first.
    Both O(V+E); Kahn's has no recursion-depth risk and handles
    disconnected graphs in one pass.
=====================================================================
REAL LIFE
    • Compilers / build systems: topological order of compilation
      units so headers and libraries exist before dependents build.
    • Spreadsheet engines: order formula cells by their dependencies.
    • Database schema migrations: tables created in dependency order.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import List

# =====================================================================
# APPROACH 1 : Kahn's algorithm — dequeue order IS the answer
# =====================================================================
class SolutionOne:
    """
    Purpose : Return one valid order to take all courses.
    Inputs  : numCourses — number of courses.
              prerequisites — [a, b] pairs: a needs b first.
    Output  : List[int] — topological order, empty if cyclic.
    """

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj: List[List[int]] = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)   # edge b -> a : finish b before a
            indegree[a] += 1   # a gains one unsatisfied prerequisite

        # Ready queue: courses with no unsatisfied prerequisites.
        ready = deque(i for i in range(numCourses) if indegree[i] == 0)

        # The dequeue order is a valid topological order.
        order: List[int] = []
        while ready:
            course = ready.popleft()
            order.append(course)
            # Unblock dependents whose prerequisites are all done.
            for dep in adj[course]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    ready.append(dep)

        # Cycle → some course never became ready → order is short.
        return order if len(order) == numCourses else []

# =====================================================================
# APPROACH 2 : DFS — prepend on finish (reverse of finish time)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return one valid order to take all courses.
    Inputs  : numCourses — number of courses.
              prerequisites — [a, b] pairs: a needs b first.
    Output  : List[int] — topological order, empty if cyclic.
    """

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj: List[List[int]] = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            adj[b].append(a)
        # colour : 0 unvisited, 1 on stack, 2 done.
        colour = [0] * numCourses
        order: List[int] = []

        def dfs(v: int) -> bool:
            # Back edge → cycle → give up.
            if colour[v] == 1:
                return False
            if colour[v] == 2:
                return True
            colour[v] = 1
            for nb in adj[v]:
                if not dfs(nb):
                    return False
            colour[v] = 2
            # Children finished BEFORE v → prepending keeps each
            # prerequisite earlier in the final order.
            order.append(v)
            return True

        for v in range(numCourses):
            if colour[v] == 0 and not dfs(v):
                return []
        # `order` was built by appending on finish; reverse it so
        # prerequisites appear before their dependents.
        return order[::-1]

# =====================================================================
# BENCHMARK — run both approaches on 3 official-style tests
# =====================================================================
if __name__ == "__main__":
    # Test 1 (official): 2, [[1,0]] → [0,1].
    # Test 2 (official): 4, [[1,0],[2,0],[3,1],[3,2]] → valid order.
    # Test 3: 1, [] → [0].
    tests = [
        (2, [[1, 0]]),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
        (1, []),
    ]

    all_pass = True
    for idx, (n, pre) in enumerate(tests, start=1):
        # --- Approach 1: time + peak memory ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().findOrder(n, pre)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + peak memory ---
        tracemalloc.start()
        t2 = time.perf_counter()
        r2 = SolutionTwo().findOrder(n, pre)
        t3 = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Validity check: every prerequisite b must appear before a in
        # the output order.
        def valid(order: List[int]) -> bool:
            if len(order) != n:
                return False
            pos = {c: i for i, c in enumerate(order)}
            return all(pos[b] < pos[a] for a, b in pre)

        ok = valid(r1) and valid(r2)
        all_pass = all_pass and ok
        print(
            f"Test {idx} {'PASS' if ok else 'FAIL'} "
            f"| A1={r1} time={(t1-t0)*1e6:.2f} µs peak={peak1/1024:.1f} KB"
            f" | A2={r2} time={(t3-t2)*1e6:.2f} µs peak={peak2/1024:.1f} KB"
        )

    print("PASS : all tests green on both approaches."
          if all_pass else "FAIL : at least one test/approach disagrees.")