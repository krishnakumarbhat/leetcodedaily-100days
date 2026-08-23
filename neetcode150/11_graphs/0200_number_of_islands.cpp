/*
 * =====================================================================
 * LeetCode 200 : Number of Islands                                   (Medium)
 * https://leetcode.com/problems/number-of-islands/
 * Category   : Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   An m×n grid of '1' (land) and '0' (water). Count the number of
 *   islands — maximal connected groups of '1's connected via the 4
 *   cardinal directions (diagonals do NOT connect).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every unvisited land cell starts a NEW island. To avoid counting
 *   the same island twice we must swallow it whole: flood-fill its
 *   entire connected component, marking cells visited. Repeat until
 *   every land cell is claimed — each successful flood fill = one
 *   island. Grid-as-graph again: cells are nodes, 4 dirs are edges.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive DFS flood fill (BEST for clarity)
 *   Scan the grid; on '1' → count++, sink the whole component by
 *   recursion (mark '0' on entry). Visited marking mutates the input
 *   grid, so no extra visited array is needed.
 *   Time  Complexity : O(m·n)  — each cell is touched a constant
 *                        number of times across all floods.
 *   Space Complexity : O(m·n)  — worst-case recursion depth.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative BFS flood fill (no recursion)
 *   Same scan-and-sink, but each component is flooded with a queue.
 *   Identical O(m·n) work; the frontier can hold O(m·n) cells in the
 *   worst case, but no call-stack overflow risk on tall islands.
 *   Time  Complexity : O(m·n)   Space Complexity : O(m·n).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — visited sets & in-place marking
 *   Two ways to track visited cells: an auxiliary bool grid (extra
 *   O(m·n) memory) or in-place mutation of the input (O(1) memory).
 *   Since the problem does not forbid modifying `grid`, sinking '1'→'0'
 *   is the classic trick. BFS vs DFS: same complexity; DFS recursion
 *   is terser, BFS is immune to deep-recursion crashes. The dirs
 *   array {( -1,0),(1,0),(0,-1),(0,1)} keeps the neighbour walk in
 *   one loop.
 * =====================================================================
 */

#include <iostream>         // std::cout — printing benchmark results
#include <vector>           // std::vector — the 2D grid
#include <string>           // std::string — grid rows
#include <queue>            // std::queue — BFS frontier
#include <unordered_map>    // std::unordered_map — hash table (chaining)
#include <unordered_set>    // std::unordered_set — visited set
#include <chrono>           // std::chrono — high-resolution timing
#include <sys/resource.h>   // getrusage — peak RAM measurement
#include <utility>          // std::pair — (r,c) coordinates

/* =====================================================================
 * APPROACH 1 : Recursive DFS — sink each island as it is discovered
 * ===================================================================== */
class Solution_1 {
private:
    int rows_, cols_;

    /*
     * Purpose : Flood-fill the island containing (r,c) to water.
     * Inputs  : grid — mutable grid; r, c — current land cell.
     * Output  : void — every reachable '1' becomes '0'.
     */
    void dfs(std::vector<std::vector<char>>& grid, int r, int c) {
        // Guards: outside the grid, or already water → stop.
        if (r < 0 || r >= rows_ || c < 0 || c >= cols_ || grid[r][c] != '1') return;
        // Sink the cell BEFORE recursing — marks it visited AND
        // prevents this flood from re-entering it through a cycle.
        grid[r][c] = '0';
        dfs(grid, r - 1, c);   // up
        dfs(grid, r + 1, c);   // down
        dfs(grid, r, c - 1);   // left
        dfs(grid, r, c + 1);   // right
    }

public:
    /*
     * Purpose : Count connected components of '1' cells.
     * Inputs  : grid — m×n grid of '1'/'0' (mutated in place).
     * Output  : int number of islands.
     */
    int numIslands(std::vector<std::vector<char>>& grid) {
        rows_ = static_cast<int>(grid.size());
        if (rows_ == 0) return 0;
        cols_ = static_cast<int>(grid[0].size());

        int count = 0;
        // Every unvisited land cell must start a brand-new island.
        for (int r = 0; r < rows_; ++r) {
            for (int c = 0; c < cols_; ++c) {
                if (grid[r][c] == '1') {
                    ++count;      // new island discovered
                    dfs(grid, r, c);  // sink it so it is never counted again
                }
            }
        }
        return count;
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative BFS — same scan-and-sink, queue-driven
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Count connected components of '1' cells.
     * Inputs  : grid — m×n grid of '1'/'0' (mutated in place).
     * Output  : int number of islands.
     */
    int numIslands(std::vector<std::vector<char>>& grid) {
        int m = static_cast<int>(grid.size());
        if (m == 0) return 0;
        int n = static_cast<int>(grid[0].size());

        const int dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        int count = 0;

        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                if (grid[r][c] != '1') continue;
                ++count;              // new island
                // BFS frontier seeded at the discovery cell.
                std::queue<std::pair<int, int>> q;
                q.push({r, c});
                grid[r][c] = '0';     // sink on enqueue (visited marker)
                while (!q.empty()) {
                    auto [cr, cc] = q.front();
                    q.pop();
                    for (int d = 0; d < 4; ++d) {
                        int nr = cr + dirs[d][0];
                        int nc = cc + dirs[d][1];
                        if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
                        if (grid[nr][nc] != '1') continue;
                        grid[nr][nc] = '0';  // claim before pushing
                        q.push({nr, nc});
                    }
                }
            }
        }
        return count;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 official-style tests
 * ===================================================================== */
int main() {
    // Test 1 (official): three islands (top-left block, centre lone,
    // bottom-right block).
    std::vector<std::vector<char>> t1 = {
        {'1', '1', '1', '1', '0'},
        {'1', '1', '0', '1', '0'},
        {'1', '1', '0', '0', '0'},
        {'0', '0', '0', '0', '0'}
    };
    // Test 2 (official): one island (ring shape, diagonals don't join).
    std::vector<std::vector<char>> t2 = {
        {'1', '1', '0', '0', '0'},
        {'1', '1', '0', '0', '0'},
        {'0', '0', '1', '0', '0'},
        {'0', '0', '0', '1', '1'}
    };
    // Test 3: single cell.
    std::vector<std::vector<char>> t3 = {{'1'}};

    struct { std::vector<std::vector<char>> grid; int expected; } tests[] = {
        {t1, 1}, {t2, 3}, {t3, 1}
    };

    bool allPass = true;
    for (int t = 0; t < 3; ++t) {
        // Fresh copies so both solutions see identical input.
        auto g1 = tests[t].grid;
        auto g2 = tests[t].grid;

        // --- Approach 1 timing + memory ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto s1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_1().numIslands(g1);
        auto e1_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);

        // --- Approach 2 timing + memory ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto s2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_2().numIslands(g2);
        auto e2_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);

        long mem1 = (after1.ru_maxrss - before1.ru_maxrss);
        long mem2 = (after2.ru_maxrss - before2.ru_maxrss);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1_ - s1).count() / 1000.0;
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2_ - s2).count() / 1000.0;

        bool ok = r1 == tests[t].expected && r2 == tests[t].expected && r1 == r2;
        allPass = allPass && ok;
        std::cout << "Test " << (t + 1) << (ok ? " PASS" : " FAIL")
                  << " | A1=" << r1 << " (expect " << tests[t].expected << ")"
                  << "  time=" << us1 << " µs  mem=" << mem1 << " KB"
                  << " | A2=" << r2 << "  time=" << us2 << " µs  mem=" << mem2 << " KB\n";
    }
    std::cout << (allPass ? "PASS : all tests green on both approaches.\n"
                          : "FAIL : at least one test/approach disagrees.\n");
    return 0;
}