/*
 * =====================================================================
 * LeetCode 63  : Unique Paths II                                    (Medium)
 * https://leetcode.com/problems/unique-paths-ii/
 * Category   : 2-D dynamic programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Robot at (0,0) must reach (m-1,n-1) moving only right/down; cells
 *   with obstacleGrid[i][j] == 1 are blocked. Count the paths.
 * ---------------------------------------------------------------------
 * INTUITION
 *   paths[i][j] = paths[i-1][j] + paths[i][j-1] — every path reaches
 *   a cell from above or from the left. Obstacles zero out a cell and
 *   (by the recurrence) everything downstream of it.
 * ---------------------------------------------------------------------
 * APPROACH 1 · In-place DP (best)
 *   Reuse the input grid as the DP table: seed (0,0), then propagate
 *   the recurrence skipping obstacle cells.
 * APPROACH 2 · 1-D rolling row
 *   dp[j] += dp[j-1] row by row; obstacles set dp[j] = 0.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why in-place mutation is safe here
 *   obstacleGrid cells are only ever read as booleans (0/1) and we
 *   overwrite them with path counts ≥ 0 — a value that can never be
 *   mistaken for an obstacle. The rolling-row variant is the same
 *   recurrence with 1/4 of the memory; both are exact because the
 *   path count of a cell depends only on cells already computed
 *   (top-down-left → left-to-right order).
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(m·n).
 * MEMORY COMPLEXITY: O(1) in-place / O(n) rolling.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int uniquePathsWithObstacles(std::vector<std::vector<int>>& g) {
        int m = static_cast<int>(g.size());
        int n = static_cast<int>(g[0].size());
        if (g[0][0] == 1) return 0;
        g[0][0] = 1;                                   // seed
        for (int j = 1; j < n; ++j)                    // first row
            g[0][j] = g[0][j] == 1 ? 0 : g[0][j - 1];
        for (int i = 1; i < m; ++i) {                  // rest of the grid
            g[i][0] = g[i][0] == 1 ? 0 : g[i - 1][0];
            for (int j = 1; j < n; ++j)
                g[i][j] = g[i][j] == 1 ? 0 : g[i - 1][j] + g[i][j - 1];
        }
        return g[m - 1][n - 1];
    }
};

class Solution_2 {
public:
    int uniquePathsWithObstacles(std::vector<std::vector<int>>& g) {
        int n = static_cast<int>(g[0].size());
        std::vector<long> dp(n, 0);
        dp[0] = g[0][0] == 1 ? 0 : 1;
        for (auto& row : g) {
            if (row[0] == 1) dp[0] = 0;
            for (int j = 1; j < n; ++j) {
                if (row[j] == 1) dp[j] = 0;
                else dp[j] += dp[j - 1];
            }
        }
        return static_cast<int>(dp[n - 1]);
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
        {{{0, 0, 0}, {0, 1, 0}, {0, 0, 0}}, 2},
        {{{0, 1}, {0, 0}}, 1},
        {{{1, 0}}, 0},
        {{{0, 0}, {0, 0}}, 2}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        auto g1 = c.g, g2 = c.g;
        int r1 = Solution_1().uniquePathsWithObstacles(g1);
        int r2 = Solution_2().uniquePathsWithObstacles(g2);
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
