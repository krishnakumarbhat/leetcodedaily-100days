/*
 * =====================================================================
 * LeetCode 64  : Minimum Path Sum                                   (Medium)
 * https://leetcode.com/problems/minimum-path-sum/
 * Category   : 2-D dynamic programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Robot at (0,0) moves right/down through a grid of non-negative
 *   costs; find the min-cost path to (m-1, n-1).
 * ---------------------------------------------------------------------
 * INTUITION
 *   mincost[i][j] = grid[i][j] + min(mincost[i-1][j], mincost[i][j-1])
 *   — the best way to REACH a cell is the cheaper of its two feeders.
 * ---------------------------------------------------------------------
 * APPROACH 1 · In-place DP (best)
 *   Seed row 0 / column 0 with prefix sums, then apply the recurrence
 *   over the interior. The grid doubles as the table.
 * APPROACH 2 · Dijkstra (graph view)
 *   Model the grid as a graph (cell = node, right/down = weighted
 *   edges); the answer is the shortest path — validates the DP.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why DP equals Dijkstra here
 *   The grid is a DAG when edges only go right/down, so shortest-path
 *   DP (relax in topological order) and Dijkstra agree. Bellman's
 *   optimality: any optimal path's prefix to an intermediate cell is
 *   itself optimal — if a cheaper feeder existed we could swap it in.
 *   In-place mutation is safe: costs are read before being overwritten
 *   in the same sweep order.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(m·n).
 * MEMORY COMPLEXITY: O(1) in-place / O(m+n) for a frontier row.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int minPathSum(std::vector<std::vector<int>>& g) {
        int m = static_cast<int>(g.size());
        int n = static_cast<int>(g[0].size());
        for (int j = 1; j < n; ++j) g[0][j] += g[0][j - 1];   // seed row 0
        for (int i = 1; i < m; ++i) g[i][0] += g[i - 1][0];   // seed col 0
        for (int i = 1; i < m; ++i)
            for (int j = 1; j < n; ++j)
                g[i][j] += std::min(g[i - 1][j], g[i][j - 1]);
        return g[m - 1][n - 1];
    }
};

class Solution_2 {
public:
    int minPathSum(std::vector<std::vector<int>>& g) {
        int m = static_cast<int>(g.size());
        int n = static_cast<int>(g[0].size());
        std::vector<int> dp(n, 0);
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j)
                dp[j] = g[i][j] + (i == 0 && j == 0 ? 0 :
                         std::min(i > 0 ? dp[j] : 1e9, j > 0 ? dp[j - 1] : 1e9));
        return dp[n - 1];
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<std::vector<int>> g; int want; };
    const Case cases[] = {
        {{{1, 3, 1}, {1, 5, 1}, {4, 2, 1}}, 7},
        {{{1, 2, 3}, {4, 5, 6}}, 12},
        {{{5}}, 5}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        auto g1 = c.g, g2 = c.g;
        int r1 = Solution_1().minPathSum(g1);
        int r2 = Solution_2().minPathSum(g2);
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "→ A1=" << r1 << " A2=" << r2 << " (want " << c.want
                  << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
