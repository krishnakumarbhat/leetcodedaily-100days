"""
=====================================================================
LeetCode 130 : Surrounded Regions                               (Medium)
https://leetcode.com/problems/surrounded-regions/
Category   : Graphs
---------------------------------------------------------------------
PROBLEM
    An m×n board of 'X' and 'O'. Flip every 'O' that is NOT connected
    to the border through other 'O's into 'X'. Border 'O's (and any
    'O' reachable from them) survive.
---------------------------------------------------------------------
INTUITION
    "Surrounded" is really REACHABILITY: an 'O' must flip iff it
    cannot walk to the board's edge. So invert the question — multi-
    source flood fill from every border 'O', mark those cells as
    escaping, then flip every unmarked 'O'. One pass, no per-cell
    searches.
---------------------------------------------------------------------
APPROACH 1 — BFS from every border 'O' (BEST)
    Queue all border 'O's, mark 'E'. BFS the 4 neighbours; every 'O'
    reached escapes too. Final sweep: 'E'→'O', leftover 'O'→'X'.
    Time  Complexity : O(m·n)   Space Complexity : O(m·n)
---------------------------------------------------------------------
APPROACH 2 — Recursive DFS from every border 'O'
    Identical idea, recursive traversal. Call stack can reach O(m·n)
    on a winding island — stack-overflow risk on big boards.
    Time  Complexity : O(m·n)   Space Complexity : O(m·n) (stack)
---------------------------------------------------------------------
DATA STRUCTURE DEEP DIVE — grid graphs & the dirs array
    A grid IS a graph: cell (r,c) is a node, edges to its 4
    neighbours. The dirs array `[(−1,0),(1,0),(0,−1),(0,1)]` turns 4
    copy-pasted branches into one loop. Bounds must be checked BEFORE
    indexing the grid. BFS vs DFS: identical O(m·n); BFS avoids deep
    recursion; DFS is terser to write. Both need a visited marker to
    stop cycles (here: repainting 'O'→'E').
=====================================================================
REAL LIFE
    • Flood-fill tools (paint bucket in every editor) are BFS/DFS on
      a grid graph.
    • "Is this pixel/region reachable from the edge?" = leak
      detection in circuit-board etching and PCB design.
    • Go/Baduk territory evaluation: stones enclosed by the opponent.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import List

# =====================================================================
# APPROACH 1 : Multi-source BFS from every border 'O'
# =====================================================================
class SolutionOne:
    """
    Purpose : Flip surrounded 'O' regions into 'X' in place.
    Inputs  : board — m×n grid of 'X'/'O' (mutated in place).
    Output  : None — board modified so only border-connected 'O'
              survive.
    """

    def solve(self, board: List[List[str]]) -> None:
        m, n = len(board), len(board[0])
        # Frontier of every border 'O' — multi-source BFS start set.
        queue = deque()
        for r in range(m):
            for c in range(n):
                # Only cells ON the rim can seed the escape wave.
                if (r in (0, m - 1) or c in (0, n - 1)) and board[r][c] == "O":
                    board[r][c] = "E"      # 'E' = escapes (temporary mark)
                    queue.append((r, c))

        # dirs : the 4 cardinal offsets — one loop over 4 neighbours.
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # BFS: any 'O' reachable from a border 'O' escapes too.
        while queue:
            r, c = queue.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                # Bounds guard FIRST — never index outside the grid.
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                    board[nr][nc] = "E"    # claim: this cell escapes
                    queue.append((nr, nc))

        # Final sweep: 'E' reverts to 'O'; any remaining 'O' is truly
        # enclosed → flip to 'X'.
        for r in range(m):
            for c in range(n):
                if board[r][c] == "E":
                    board[r][c] = "O"
                elif board[r][c] == "O":
                    board[r][c] = "X"

# =====================================================================
# APPROACH 2 : Recursive DFS from every border 'O'
# =====================================================================
class SolutionTwo:
    """
    Purpose : Flip surrounded 'O' regions into 'X' in place.
    Inputs  : board — m×n grid of 'X'/'O' (mutated in place).
    Output  : None — board modified so only border-connected 'O'
              survive.
    """

    def solve(self, board: List[List[str]]) -> None:
        m, n = len(board), len(board[0])

        # Nested closure keeps the recursion signature tiny — only the
        # coordinates travel down the call stack.
        def dfs(r: int, c: int) -> None:
            # Recursion guard: stop at walls, visited cells, or rim.
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != "O":
                return
            board[r][c] = "E"              # mark BEFORE recursing — the
                                           # classic anti-cycle guard.
            dfs(r - 1, c)                  # up
            dfs(r + 1, c)                  # down
            dfs(r, c - 1)                  # left
            dfs(r, c + 1)                  # right

        # Seed DFS from every border 'O' — same multi-source idea.
        for r in range(m):
            for c in range(n):
                if (r in (0, m - 1) or c in (0, n - 1)) and board[r][c] == "O":
                    dfs(r, c)

        # Same final sweep: 'E' → 'O', leftover 'O' → 'X'.
        for r in range(m):
            for c in range(n):
                if board[r][c] == "E":
                    board[r][c] = "O"
                elif board[r][c] == "O":
                    board[r][c] = "X"

# =====================================================================
# BENCHMARK — run both approaches on 3 tests, compare full boards
# =====================================================================
if __name__ == "__main__":
    # Test 1 (official): center 2×2 enclosed; border ring survives.
    t1 = [["X", "X", "X", "X"],
          ["X", "O", "O", "X"],
          ["X", "X", "O", "X"],
          ["X", "O", "X", "X"]]
    # Test 2 (official): single border 'O' → nothing flipped.
    t2 = [["X"]]
    # Test 3: 'O' column touching the rim saves the whole corridor.
    t3 = [["O", "X", "X"],
          ["O", "X", "O"],
          ["O", "O", "O"]]
    tests = [t1, t2, t3]
    # Official expected board for test 1.
    expected_t1 = [["X", "X", "X", "X"],
                   ["X", "X", "X", "X"],
                   ["X", "X", "X", "X"],
                   ["X", "O", "X", "X"]]

    all_pass = True
    for idx, test in enumerate(tests, start=1):
        # --- Approach 1: time + peak memory (fresh copy each run) ---
        board_a = [row[:] for row in test]
        tracemalloc.start()
        t0 = time.perf_counter()
        SolutionOne().solve(board_a)
        t1_ = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + peak memory ---
        board_b = [row[:] for row in test]
        tracemalloc.start()
        t2_ = time.perf_counter()
        SolutionTwo().solve(board_b)
        t3_ = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Both approaches must produce IDENTICAL final boards, and test
        # 1 must match the official expected result.
        same = board_a == board_b
        known = board_a == expected_t1 if idx == 1 else True
        ok = same and known
        all_pass = all_pass and ok
        print(
            f"Test {idx} {'PASS' if ok else 'FAIL'} "
            f"| A1 time={(t1_-t0)*1e6:.2f} µs peak={peak1/1024:.1f} KB"
            f" | A2 time={(t3_-t2_)*1e6:.2f} µs peak={peak2/1024:.1f} KB"
            f" | boards identical: {same}"
        )

    print("PASS : all tests green on both approaches."
          if all_pass else "FAIL : at least one test/approach disagrees.")