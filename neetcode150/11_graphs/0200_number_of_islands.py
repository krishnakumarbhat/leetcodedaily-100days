"""
=====================================================================
LeetCode 200 : Number of Islands                                (Medium)
https://leetcode.com/problems/number-of-islands/
Category   : Graphs
---------------------------------------------------------------------
PROBLEM
    An m×n grid of '1' (land) and '0' (water). Count the number of
    islands — maximal connected groups of '1's connected via the 4
    cardinal directions (diagonals do NOT connect).
---------------------------------------------------------------------
INTUITION
    Every unvisited land cell starts a NEW island. To avoid counting
    the same island twice, swallow it whole: flood-fill its entire
    connected component, marking cells visited. Each successful flood
    fill = one island. Grid-as-graph: cells are nodes, 4 dirs edges.
---------------------------------------------------------------------
APPROACH 1 — Recursive DFS flood fill (BEST for clarity)
    Scan the grid; on '1' → count++, sink the whole component by
    recursion (mark '0' on entry). In-place marking = O(1) extra
    memory, no visited array.
    Time  Complexity : O(m·n)   Space Complexity : O(m·n) (stack)
---------------------------------------------------------------------
APPROACH 2 — Iterative BFS flood fill (no recursion)
    Same scan-and-sink, queue-driven flood. Identical O(m·n) work,
    no call-stack overflow risk on tall islands.
    Time  Complexity : O(m·n)   Space Complexity : O(m·n)
---------------------------------------------------------------------
DATA STRUCTURE DEEP DIVE — visited sets & in-place marking
    Two ways to track visited: an auxiliary bool grid (extra O(m·n)
    memory) or in-place mutation (O(1) extra). Sinking '1'→'0' is the
    classic trick when mutation is allowed. BFS vs DFS: same
    complexity; DFS recursion is terser, BFS never stack-overflows.
    The dirs array [(−1,0),(1,0),(0,−1),(0,1)] walks all 4 neighbours
    in one loop; bounds must be checked before indexing.
=====================================================================
REAL LIFE
    • Image segmentation: connected components of pixels (medical
      scans, satellite imagery) is this exact algorithm (OpenCV
      connectedComponents).
    • Social networks: islands = disconnected friend-groups that
      cannot reach each other.
    • Battle-tested flood fill: paint bucket tools in every editor.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import List

# =====================================================================
# APPROACH 1 : Recursive DFS — sink each island as it is discovered
# =====================================================================
class SolutionOne:
    """
    Purpose : Count connected components of '1' cells.
    Inputs  : grid — m×n grid of '1'/'0' (mutated in place).
    Output  : int number of islands.
    """

    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])

        # Nested closure keeps the recursion signature minimal.
        def dfs(r: int, c: int) -> None:
            # Guards: outside the grid, or already water → stop.
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != "1":
                return
            # Sink the cell BEFORE recursing — marks it visited AND
            # prevents re-entry through a cycle.
            grid[r][c] = "0"
            dfs(r - 1, c)   # up
            dfs(r + 1, c)   # down
            dfs(r, c - 1)   # left
            dfs(r, c + 1)   # right

        count = 0
        # Every unvisited land cell must start a brand-new island.
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1":
                    count += 1        # new island discovered
                    dfs(r, c)         # sink it so it is never counted again
        return count

# =====================================================================
# APPROACH 2 : Iterative BFS — same scan-and-sink, queue-driven
# =====================================================================
class SolutionTwo:
    """
    Purpose : Count connected components of '1' cells.
    Inputs  : grid — m×n grid of '1'/'0' (mutated in place).
    Output  : int number of islands.
    """

    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        count = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] != "1":
                    continue
                count += 1            # new island
                # BFS frontier seeded at the discovery cell.
                queue = deque([(r, c)])
                grid[r][c] = "0"      # sink on enqueue (visited marker)
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in dirs:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == "1":
                            grid[nr][nc] = "0"   # claim before pushing
                            queue.append((nr, nc))
        return count

# =====================================================================
# BENCHMARK — run both approaches on 3 official-style tests
# =====================================================================
if __name__ == "__main__":
    # Test 1 (official): one island. Test 2 (official): three islands.
    # Test 3: single cell.
    tests = [
        ([["1", "1", "1", "1", "0"],
          ["1", "1", "0", "1", "0"],
          ["1", "1", "0", "0", "0"],
          ["0", "0", "0", "0", "0"]], 1),
        ([["1", "1", "0", "0", "0"],
          ["1", "1", "0", "0", "0"],
          ["0", "0", "1", "0", "0"],
          ["0", "0", "0", "1", "1"]], 3),
        ([["1"]], 1),
    ]

    all_pass = True
    for idx, (grid, expected) in enumerate(tests, start=1):
        # --- Approach 1: time + peak memory (fresh copy each run) ---
        g1 = [row[:] for row in grid]
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().numIslands(g1)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + peak memory ---
        g2 = [row[:] for row in grid]
        tracemalloc.start()
        t2 = time.perf_counter()
        r2 = SolutionTwo().numIslands(g2)
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