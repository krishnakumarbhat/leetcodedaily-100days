"""
=====================================================================
LeetCode 64 : Minimum Path Sum                                   (Medium)
https://leetcode.com/problems/minimum-path-sum/
Category   : 2-D dynamic programming
---------------------------------------------------------------------
PROBLEM
    Min-cost path from (0,0) to (m-1,n-1), moving right/down over a
    grid of non-negative costs.
---------------------------------------------------------------------
INTUITION
    mincost[i][j] = grid[i][j] + min(mincost[i-1][j], mincost[i][j-1])
    — the cheapest way to reach a cell comes from its cheaper feeder.
---------------------------------------------------------------------
APPROACH 1 · In-place DP (best)
    Seed row 0 and column 0 with prefix sums, then the recurrence.
APPROACH 2 · 1-D rolling row
    dp[j] = grid[i][j] + min(above, left) using a single array.
---------------------------------------------------------------------
DEEP DIVE · DP ≡ Dijkstra on a DAG
    With only right/down edges the grid is a DAG, so shortest paths
    follow topological order — no heap needed. Optimal substructure:
    the prefix of an optimal path through (i,j) is itself optimal,
    else swapping in a cheaper feeder improves the whole path.
---------------------------------------------------------------------
TIME COMPLEXITY : O(m·n)
MEMORY COMPLEXITY: O(1) in-place / O(n) rolling.
=====================================================================
"""


class Solution_1:
    def minPathSum(self, grid):
        m, n = len(grid), len(grid[0])
        for j in range(1, n):
            grid[0][j] += grid[0][j - 1]
        for i in range(1, m):
            grid[i][0] += grid[i - 1][0]
            for j in range(1, n):
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
        return grid[m - 1][n - 1]


class Solution_2:
    def minPathSum(self, grid):
        m, n = len(grid), len(grid[0])
        dp = [0] * n
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    dp[j] = grid[i][j]
                elif i == 0:
                    dp[j] = grid[i][j] + dp[j - 1]
                elif j == 0:
                    dp[j] = grid[i][j] + dp[j]
                else:
                    dp[j] = grid[i][j] + min(dp[j], dp[j - 1])
        return dp[n - 1]


if __name__ == "__main__":
    import time, tracemalloc
    cases = [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
             ([[1, 2, 3], [4, 5, 6]], 12),
             ([[5]], 5)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for g, want in cases:
        r1, r2 = Solution_1().minPathSum([row[:] for row in g]), Solution_2().minPathSum([row[:] for row in g])
        ok &= r1 == r2 == want
        print(f"-> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
