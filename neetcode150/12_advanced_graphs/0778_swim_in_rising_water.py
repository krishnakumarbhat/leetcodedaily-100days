"""
=====================================================================
LeetCode 778 : Swim in Rising Water                              (Hard)
https://leetcode.com/problems/swim-in-rising-water/
Category   : Advanced Graphs
---------------------------------------------------------------------
PROBLEM
    n x n grid; grid[r][c] is the elevation of that cell. Rain raises
    the water level uniformly: at time t every cell with elevation
    <= t is underwater and you may swim between adjacent underwater
    cells. Start at (0,0), reach (n-1, n-1). Return the EARLIEST time
    t at which a path exists.
---------------------------------------------------------------------
INTUITION
    "Earliest t with a path" is a YES/NO question repeated over t:
    if a path exists at time t it still exists at any larger t (more
    cells are underwater) — the predicate is MONOTONE, which is
    exactly what binary search handles. Probe a water level, run a
    reachability check, shrink the window. Equivalent view: minimise
    the maximum cell elevation along a path (a minimax path).
---------------------------------------------------------------------
APPROACH 1 — Binary search over t + BFS reachability (BEST)
    lo = grid[0][0] (start cell must be flooded), hi = max elevation.
    While lo < hi: probe mid; BFS from (0,0) visiting only cells with
    elevation <= mid; if the target is reached, hi = mid (feasible,
    try lower), else lo = mid + 1 (need higher water).
    Time  Complexity : O(n² log H) — log H probes, each BFS is O(n²)
                         (H = max elevation).
    Space Complexity : O(n²)       — visited matrix per probe.
---------------------------------------------------------------------
APPROACH 2 — Binary search over t + DSU connectivity
    Same binary search, but reachability uses union-find: for the
    probed level, union every underwater cell with its underwater
    neighbours; (0,0) and (n-1,n-1) are connected iff a path exists.
    Time  Complexity : O(n² log H)   Space Complexity : O(n²)
---------------------------------------------------------------------
DEEP DIVE — why binary search, and the DSU alternative
    P(t) = "path exists at water level t" is monotone because water
    never goes DOWN: reachable at t ⇒ reachable at t+1. Any monotone
    predicate on a sorted universe answers with binary search in
    O(log H) probes — each probe a graph reachability run. The DSU
    variant unions flooded cells instead of visiting them one by one;
    connectivity then costs two find() calls. BFS proves an actual
    path, DSU proves connectivity — both answer the same question.
---------------------------------------------------------------------
REAL LIFE
    • Flood / evacuation planning — "when does a road network still
      connect the shelters?"
    • Terrain traversal in games & robotics — minimax path = least
      dangerous route through a height map.
    • Chip design — the slowest (max-delay) path sets the clock.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import List


# =====================================================================
# APPROACH 1 : Binary search + BFS reachability
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the earliest time the target cell becomes
              reachable from (0,0) as the water rises.
    Inputs  : grid — n x n matrix of cell elevations.
    Output  : int — earliest feasible water level.
    """

    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        # Feasibility window: lo = start elevation (any valid t must
        # already flood the start cell), hi = global max (at that
        # level every cell is passable, so a path always exists).
        lo, hi = grid[0][0], max(max(row) for row in grid)

        # Standard binary search on a monotone predicate.
        while lo < hi:
            mid = (lo + hi) // 2
            if self._reachable(grid, mid):
                hi = mid          # feasible → try a LOWER water level
            else:
                lo = mid + 1      # infeasible → water must rise further
        return lo

    def _reachable(self, grid: List[List[int]], level: int) -> bool:
        """BFS over cells with elevation <= level; True iff the target
        cell is reachable from (0,0)."""
        n = len(grid)
        if grid[0][0] > level:
            return False          # start already flooded out

        seen = [[False] * n for _ in range(n)]
        q = deque([(0, 0)])
        seen[0][0] = True

        while q:
            r, c = q.popleft()
            if r == n - 1 and c == n - 1:
                return True       # target reached
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                # Skip out-of-bounds, visited, or still-dry cells.
                if not (0 <= nr < n and 0 <= nc < n):
                    continue
                if seen[nr][nc] or grid[nr][nc] > level:
                    continue
                seen[nr][nc] = True
                q.append((nr, nc))
        return False


# =====================================================================
# APPROACH 2 : Binary search + DSU connectivity
# =====================================================================
class SolutionTwo:
    """
    Purpose : Earliest feasible water level, decided by union-find
              connectivity instead of BFS.
    Inputs  : grid — n x n matrix of cell elevations.
    Output  : int — earliest feasible water level.
    """

    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        lo, hi = grid[0][0], max(max(row) for row in grid)

        while lo < hi:
            mid = (lo + hi) // 2
            if self._connected(grid, mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

    def _connected(self, grid: List[List[int]], level: int) -> bool:
        """Union all underwater cells (<= level) with their underwater
        neighbours; True iff the two corners share a root."""
        n = len(grid)
        parent = list(range(n * n))   # cell id = r * n + c
        rank = [0] * (n * n)

        def find(x: int) -> int:
            # Find with path compression: walk up then flatten.
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def unite(a: int, b: int) -> None:
            # Union by rank: shallower tree under the deeper one.
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            else:
                parent[rb] = ra
                if rank[ra] == rank[rb]:
                    rank[ra] += 1

        for r in range(n):
            for c in range(n):
                if grid[r][c] > level:
                    continue        # dry cell — skip
                ident = r * n + c
                # Merge with DOWN and RIGHT neighbours only:
                # each edge is considered exactly once this way.
                if r + 1 < n and grid[r + 1][c] <= level:
                    unite(ident, ident + n)
                if c + 1 < n and grid[r][c + 1] <= level:
                    unite(ident, ident + 1)

        # Connected iff the two corners share a union-find root.
        return find(0) == find(n * n - 1)


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example 1 — path (0,0)->(1,0)->(1,1), max 3.
    g1 = [[0, 2], [1, 3]]
    # Test 2: official example 2 — spiral grid, answer 16.
    g2 = [
        [0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16],
        [11, 17, 18, 19, 20], [10, 9, 8, 7, 6],
    ]
    # Test 3: mirror image — must cross the 3 before dropping to 1.
    g3 = [[3, 2], [0, 1]]
    cases = [(g1, 3), (g2, 16), (g3, 3)]

    all_ok = True
    for idx, (grid, want) in enumerate(cases):
        # --- Approach 1: binary search + BFS ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().swimInWater(grid)
        t1_ = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: binary search + DSU ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().swimInWater(grid)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok1 = r1 == want
        ok2 = r2 == want
        all_ok = all_ok and ok1 and ok2

        print(f"Test {idx+1} A1 (BFS + binary search): {r1}  {('PASS' if ok1 else 'FAIL')}  "
              f"time = {(t1_-t0)*1e6:.2f} us  peak = {peak1/1024:.1f} KB")
        print(f"Test {idx+1} A2 (DSU + binary search): {r2}  {('PASS' if ok2 else 'FAIL')}  "
              f"time = {(t1b-t0b)*1e6:.2f} us  peak = {peak2/1024:.1f} KB")

    print("PASS : both approaches match the expected swim times."
          if all_ok else "FAIL : at least one answer is wrong.")