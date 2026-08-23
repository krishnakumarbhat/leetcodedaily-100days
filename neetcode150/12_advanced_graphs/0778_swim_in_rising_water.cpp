/*
 * =====================================================================
 * LeetCode 778 : Swim in Rising Water                              (Hard)
 * https://leetcode.com/problems/swim-in-rising-water/
 * Category   : Advanced Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   n x n grid; grid[r][c] is the elevation of that cell. Rain raises
 *   the water level uniformly: at time t every cell with elevation
 *   <= t is underwater, and you may swim between adjacent underwater
 *   cells. You start at (0,0) and must reach (n-1, n-1). Return the
 *   EARLIEST time t at which a path exists.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Earliest t with a path" is a YES/NO question repeated over t:
 *   if a path exists at time t, it still exists at any larger t
 *   (more cells are underwater) — the predicate is MONOTONE. Monotone
 *   predicates are exactly what binary search is for: probe a water
 *   level, run a reachability check (BFS or union-find), and shrink
 *   the search window. Equivalent view: we need the path that
 *   MINIMIZES the maximum cell elevation along it (a minimax path).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Binary search over t + BFS reachability (BEST)
 *   lo = grid[0][0] (must be under water at any feasible t), hi = max
 *   elevation in the grid (the whole grid is passable at hi). While
 *   lo < hi: probe mid; BFS from (0,0) visiting only cells with
 *   elevation <= mid; if (n-1,n-1) is reached, hi = mid (feasible,
 *   try lower), else lo = mid + 1 (infeasible, need higher water).
 *   Time  Complexity : O(n² log H) — log H binary-search probes,
 *                        each BFS costs O(n²) cells (H = max value).
 *   Space Complexity : O(n²)       — visited grid per probe.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Binary search over t + DSU connectivity check
 *   Same binary search, but reachability is decided by union-find:
 *   for the probed level, union every underwater cell with its
 *   underwater neighbours; (0,0) and (n-1,n-1) are connected iff a
 *   path exists. DSU keeps the parent array as a flat index -> root
 *   map, making connectivity a pair of find() calls.
 *   Time  Complexity : O(n² log H)   Space Complexity : O(n²)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why binary search, and the DSU alternative
 *   The predicate P(t) = "path exists at water level t" is monotone
 *   because water never goes DOWN: if the set of cells reachable at
 *   level t contains the target, it also contains it at level t+1.
 *   Any monotone predicate on a sorted universe answers with binary
 *   search in O(log H) probes — here each probe is a graph
 *   reachability run. DSU variant: instead of visiting cells one by
 *   one, we UNION underwater cells with their underwater neighbours;
 *   connectivity then costs two finds. BFS probes the actual path,
 *   DSU probes only connectivity — both answer the same question.
 * =====================================================================
 */

#include <vector>          // std::vector — grid + visited matrices
#include <queue>           // std::queue — BFS frontier
#include <utility>         // std::pair — (row, col) coordinates
#include <algorithm>       // std::max — scanning the grid for hi
#include <chrono>          // std::chrono::steady_clock — benchmark timing
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

namespace {
// 4-directional neighbour offsets: down, up, right, left.
const int DR[4] = {1, -1, 0, 0};
const int DC[4] = {0, 0, 1, -1};
}

/* =====================================================================
 * APPROACH 1 : Binary search + BFS reachability
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the earliest time the target cell becomes
     *           reachable from (0,0) as the water rises.
     * Inputs  : grid — n x n matrix of cell elevations.
     * Output  : int — earliest feasible water level.
     */
    int swimInWater(const std::vector<std::vector<int>>& grid) {
        const int n = static_cast<int>(grid.size());

        // Feasibility window: lo = start elevation (any valid t must
        // already flood the start cell), hi = global maximum (at that
        // level every cell is passable, so a path always exists).
        int lo = grid[0][0];
        int hi = grid[0][0];
        for (const auto& row : grid) {
            for (int v : row) hi = std::max(hi, v);
        }

        // Standard binary search on a monotone predicate.
        while (lo < hi) {
            const int mid = lo + (hi - lo) / 2;
            if (reachable(grid, mid)) {
                hi = mid;      // feasible → try a LOWER water level
            } else {
                lo = mid + 1;  // infeasible → water must rise further
            }
        }
        return lo;
    }

private:
    /*
     * Purpose : Decide whether a path exists using only cells with
     *           elevation <= level, starting from (0,0).
     * Inputs  : grid  — elevation matrix.
     *           level — the probed water level.
     * Output  : bool — true iff (n-1, n-1) is reachable.
     */
    bool reachable(const std::vector<std::vector<int>>& grid, int level) {
        const int n = static_cast<int>(grid.size());
        if (grid[0][0] > level) return false;   // start already flooded out

        std::vector<std::vector<bool>> seen(n, std::vector<bool>(n, false));
        std::queue<std::pair<int, int>> q;
        q.emplace(0, 0);
        seen[0][0] = true;

        while (!q.empty()) {
            const auto [r, c] = q.front();
            q.pop();
            if (r == n - 1 && c == n - 1) return true;   // target reached
            for (int i = 0; i < 4; ++i) {
                const int nr = r + DR[i];
                const int nc = c + DC[i];
                // Skip out-of-bounds, visited, or still-dry cells.
                if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
                if (seen[nr][nc] || grid[nr][nc] > level) continue;
                seen[nr][nc] = true;
                q.emplace(nr, nc);
            }
        }
        return false;
    }
};

/* =====================================================================
 * APPROACH 2 : Binary search + DSU connectivity
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Earliest feasible water level, decided by union-find
     *           connectivity instead of BFS.
     * Inputs  : grid — n x n matrix of cell elevations.
     * Output  : int — earliest feasible water level.
     */
    int swimInWater(const std::vector<std::vector<int>>& grid) {
        const int n = static_cast<int>(grid.size());

        int lo = grid[0][0];
        int hi = grid[0][0];
        for (const auto& row : grid) {
            for (int v : row) hi = std::max(hi, v);
        }

        while (lo < hi) {
            const int mid = lo + (hi - lo) / 2;
            if (connected(grid, mid)) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

private:
    /* Disjoint-set union with path compression + union by rank.
       Cells are mapped to ids via id = r * n + c. */
    class DSU {
    public:
        explicit DSU(int size) : parent_(size), rank_(size, 0) {
            for (int i = 0; i < size; ++i) parent_[i] = i;
        }
        // Find with path compression: walk up then flatten the chain.
        int find(int x) {
            if (parent_[x] != x) parent_[x] = find(parent_[x]);
            return parent_[x];
        }
        // Union by rank: attach the shallower tree under the deeper one.
        void unite(int a, int b) {
            const int ra = find(a);
            const int rb = find(b);
            if (ra == rb) return;
            if (rank_[ra] < rank_[rb]) {
                parent_[ra] = rb;
            } else {
                parent_[rb] = ra;
                if (rank_[ra] == rank_[rb]) ++rank_[ra];
            }
        }
    private:
        std::vector<int> parent_;
        std::vector<int> rank_;
    };

    /*
     * Purpose : Union all underwater cells (<= level) with their
     *           underwater neighbours, then test connectivity of the
     *           start and target corners.
     * Inputs  : grid  — elevation matrix.
     *           level — probed water level.
     * Output  : bool — true iff (0,0) and (n-1,n-1) share a root.
     */
    bool connected(const std::vector<std::vector<int>>& grid, int level) {
        const int n = static_cast<int>(grid.size());
        DSU dsu(n * n);

        for (int r = 0; r < n; ++r) {
            for (int c = 0; c < n; ++c) {
                if (grid[r][c] > level) continue;   // dry cell — skip
                const int id = r * n + c;
                // Merge with the DOWN and RIGHT neighbours only:
                // each edge is considered exactly once this way.
                if (r + 1 < n && grid[r + 1][c] <= level) dsu.unite(id, id + n);
                if (c + 1 < n && grid[r][c + 1] <= level) dsu.unite(id, id + 1);
            }
        }
        // Connected iff the two corners share a union-find root.
        return dsu.find(0) == dsu.find(n * n - 1);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example 1 — path (0,0)->(1,0)->(1,1), max 3.
    const std::vector<std::vector<int>> g1 = {{0, 2}, {1, 3}};
    // Test 2: official example 2 — spiral grid, answer 16.
    const std::vector<std::vector<int>> g2 = {
        {0, 1, 2, 3, 4}, {24, 23, 22, 21, 5}, {12, 13, 14, 15, 16},
        {11, 17, 18, 19, 20}, {10, 9, 8, 7, 6}
    };
    // Test 3: mirror image — must cross the 3 before dropping to 1.
    const std::vector<std::vector<int>> g3 = {{3, 2}, {0, 1}};

    struct { const std::vector<std::vector<int>>& g; int want; } tests[] = {
        {g1, 3}, {g2, 16}, {g3, 3}
    };

    bool allOk = true;
    for (std::size_t i = 0; i < 3; ++i) {
        const auto& g = tests[i].g;
        const int want = tests[i].want;

        // --- Approach 1: binary search + BFS ---
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::steady_clock::now();
        int r1 = Solution_1().swimInWater(g);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;

        // --- Approach 2: binary search + DSU ---
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::steady_clock::now();
        int r2 = Solution_2().swimInWater(g);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;

        bool ok1 = r1 == want;
        bool ok2 = r2 == want;
        allOk = allOk && ok1 && ok2;

        std::cout << "Test " << (i + 1) << " A1 (BFS + binary search): " << r1
                  << "  " << (ok1 ? "PASS" : "FAIL") << "  time = " << us1
                  << " us  mem = " << kb1 << " KB\n";
        std::cout << "Test " << (i + 1) << " A2 (DSU + binary search): " << r2
                  << "  " << (ok2 ? "PASS" : "FAIL") << "  time = " << us2
                  << " us  mem = " << kb2 << " KB\n";
    }

    std::cout << (allOk ? "PASS : both approaches match the expected swim times."
                        : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}