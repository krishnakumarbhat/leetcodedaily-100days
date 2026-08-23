"""
=====================================================================
LeetCode 63 : Unique Paths II                                    (Medium)
https://leetcode.com/problems/unique-paths-ii/
Category   : 2-D dynamic programming
---------------------------------------------------------------------
PROBLEM
    Paths from (0,0) to (m-1,n-1) moving right/down, avoiding
    obstacle cells (value 1).
---------------------------------------------------------------------
INTUITION
    paths[i][j] = paths[i-1][j] + paths[i][j-1]; obstacles zero out
    a cell and everything downstream of it.
---------------------------------------------------------------------
APPROACH 1 · In-place DP (best)
    Reuse the grid as the table; seed (0,0), sweep row-major.
APPROACH 2 · 1-D rolling row
    dp[j] += dp[j-1] per row; obstacle cells set dp[j] = 0.
---------------------------------------------------------------------
DEEP DIVE · Mutation safety
    Cells read (0/1 obstacle flags) and written (path counts) can
    never be confused because counts ≥ 0, and each cell is computed
    only after its feeders — top-down + left-to-right order. Rolling
    row: dp[j] alone is the whole column's history.
---------------------------------------------------------------------
TIME COMPLEXITY : O(m·n)
MEMORY COMPLEXITY: O(1) in-place / O(n) rolling.
=====================================================================
"""


class Solution_1:
    def uniquePathsWithObstacles(self, grid):
        m, n = len(grid), len(grid[0])
        if grid[0][0] == 1:
            return 0
        grid[0][0] = 1
        for j in range(1, n):
            grid[0][j] = 0 if grid[0][j] == 1 else grid[0][j - 1]
        for i in range(1, m):
            grid[i][0] = 0 if grid[i][0] == 1 else grid[i - 1][0]
            for j in range(1, n):
                grid[i][j] = 0 if grid[i][j] == 1 else grid[i - 1][j] + grid[i][j - 1]
        return grid[m - 1][n - 1]


class Solution_2:
    def uniquePathsWithObstacles(self, grid):
        n = len(grid[0])
        dp = [0] * n
        dp[0] = 0 if grid[0][0] == 1 else 1
        for row in grid:
            if row[0] == 1:
                dp[0] = 0
            for j in range(1, n):
                if row[j] == 1:
                    dp[j] = 0
                else:
                    dp[j] += dp[j - 1]
        return dp[n - 1]


if __name__ == "__main__":
    import time, tracemalloc
    cases = [([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2),
             ([[0, 1], [0, 0]], 1),
             ([[1, 0]], 0),
             ([[0, 0], [0, 0]], 2)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for g, want in cases:
        r1, r2 = Solution_1().uniquePathsWithObstacles([row[:] for row in g]), Solution_2().uniquePathsWithObstacles([row[:] for row in g])
        ok &= r1 == r2 == want
        print(f"-> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
