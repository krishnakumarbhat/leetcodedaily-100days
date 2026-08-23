/*
 * =====================================================================
 * LeetCode 329 : Longest Increasing Path in a Matrix                  (Hard)
 * https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
 * Category   : 2D DP + DFS memo
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an m×n integer matrix, find the length of the LONGEST
 *   STRICTLY INCREASING path. You may move only up/down/left/right to a
 *   neighbouring cell with a LARGER value.
 * ---------------------------------------------------------------------
 * INTUITION
 *   From any cell (r,c), the best path starts at (r,c) and then moves
 *   to the best neighbour that is strictly greater. That is a recursive
 *   definition whose sub-problems are OTHER cells of the same matrix →
 *   memoized DFS over the grid. Because values strictly increase along
 *   the path, the recursion is acyclic and memoization is safe.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Memoized DFS (BEST)
 *   dp[r][c] = length of the longest increasing path STARTING at (r,c).
 *     dp[r][c] = 1 + max( dp[nr][nc] )  over neighbours with
 *                matrix[nr][nc] > matrix[r][c];  dp[r][c] = 1 if none.
 *   Visit every cell exactly once (memo hit = O(1)); each cell probes
 *   4 neighbours → total work O(m·n).
 *   Time  Complexity : O(m·n)   Space Complexity : O(m·n)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Topological order by value (no recursion stack)
 *   Sort all cells by value ASCENDING; then dp[r][c] can be computed
 *   purely bottom-up: the neighbours it reads (strictly greater) are
 *   processed LATER, so propagate dp backwards while iterating cells
 *   from large → small... simpler: process in ascending order and
 *   UPDATE larger neighbours:
 *     dp[nr][nc] = max(dp[nr][nc], 1 + dp[r][c]) for neighbours larger
 *   Processing order guarantees correctness: an increasing path visits
 *   cells in ascending value order, so each cell is "finalized" exactly
 *   when its turn comes.
 *   Time  Complexity : O(m·n·log(m·n)) (sort)   Space : O(m·n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the DAG view unlocks both approaches
 *   Edge (a→b) exists iff b > a and adjacent → the matrix is a DAG
 *   (strict increase forbids cycles). Longest increasing path = longest
 *   path in this DAG. Memoized DFS = longest-path DP on DAG; the value
 *   sort gives a topological order → same DP without recursion.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <array>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Memoized DFS
 * ===================================================================== */
class Solution_1
{
private:
    std::vector<std::vector<int>> memo_;
    int rows_, cols_;

    // Four directions: up, down, left, right.
    static constexpr int DR[4] = {-1, 1, 0, 0};
    static constexpr int DC[4] = {0, 0, -1, 1};

    /*
     * Purpose : Length of the longest increasing path starting at (r,c).
     * Inputs  : r, c — cell coordinates; mat — the matrix.
     * Output  : path length (≥ 1).
     */
    int dfs(int r, int c, const std::vector<std::vector<int>>& mat)
    {
        if (memo_[r][c] != 0)
        {
            return memo_[r][c]; // already solved → memo hit, O(1)
        }
        int best = 1; // a path of length 1 is always legal
        for (int d = 0; d < 4; ++d)
        {
            const int nr = r + DR[d];
            const int nc = c + DC[d];
            if (nr < 0 || nr >= rows_ || nc < 0 || nc >= cols_)
            {
                continue; // off the grid
            }
            if (mat[nr][nc] > mat[r][c])
            {
                // Strictly greater neighbour → the path may extend there.
                best = std::max(best, 1 + dfs(nr, nc, mat));
            }
        }
        memo_[r][c] = best;
        return best;
    }

public:
    /*
     * Purpose : Compute the longest strictly increasing path in a matrix.
     * Inputs  : matrix — the m×n grid of values.
     * Output  : length of the longest increasing path.
     */
    int longestIncreasingPath(const std::vector<std::vector<int>>& matrix)
    {
        rows_ = static_cast<int>(matrix.size());
        if (rows_ == 0)
        {
            return 0;
        }
        cols_ = static_cast<int>(matrix[0].size());
        memo_.assign(rows_, std::vector<int>(cols_, 0));

        int answer = 0;
        for (int r = 0; r < rows_; ++r)
        {
            for (int c = 0; c < cols_; ++c)
            {
                answer = std::max(answer, dfs(r, c, matrix));
            }
        }
        return answer;
    }
};

/* =====================================================================
 * APPROACH 2 : Topological order (sort by value) + bottom-up DP
 * ===================================================================== */
class Solution_2
{
private:
    static constexpr int DR[4] = {-1, 1, 0, 0};
    static constexpr int DC[4] = {0, 0, -1, 1};

public:
    /*
     * Purpose : Compute the longest strictly increasing path in a matrix.
     * Inputs  : matrix — the m×n grid of values.
     * Output  : length of the longest increasing path.
     */
    int longestIncreasingPath(const std::vector<std::vector<int>>& matrix)
    {
        const int rows = static_cast<int>(matrix.size());
        if (rows == 0)
        {
            return 0;
        }
        const int cols = static_cast<int>(matrix[0].size());

        // Bundle every cell with its value for a value-sorted scan.
        std::vector<std::array<int, 3>> cells; // {value, r, c}
        for (int r = 0; r < rows; ++r)
        {
            for (int c = 0; c < cols; ++c)
            {
                cells.push_back({matrix[r][c], r, c});
            }
        }
        // Ascending by value = topological order of the "increase" DAG.
        std::sort(cells.begin(), cells.end());

        // dp[r][c] : longest increasing path STARTING at (r,c).
        std::vector<std::vector<int>> dp(rows, std::vector<int>(cols, 1));
        int answer = 1;
        for (const auto& cell : cells)
        {
            const int r = cell[1], c = cell[2];
            for (int d = 0; d < 4; ++d)
            {
                const int nr = r + DR[d];
                const int nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols)
                {
                    continue;
                }
                if (matrix[nr][nc] > matrix[r][c])
                {
                    // A larger neighbour is processed later → its dp is
                    // finalized; candidate = 1 + its longest path.
                    dp[nr][nc] = std::max(dp[nr][nc], 1 + dp[r][c]);
                }
            }
            answer = std::max(answer, dp[r][c]);
        }
        return answer;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on the official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        std::vector<std::vector<int>> matrix;
        int expected;
    };
    const std::vector<Test> tests = {
        {{{9, 9, 4}, {6, 6, 8}, {2, 1, 1}}, 4},  // official example 1
        {{{3, 4, 5}, {3, 2, 6}, {2, 2, 1}}, 4},  // official example 2
        {{{1}}, 1},                              // single cell
        {{{1, 2}, {3, 4}}, 3},                   // 1→2→4 (or 1→3→4) = 3
        {{{1, 2, 3}, {6, 5, 4}}, 6}              // full spiral = all 6 cells
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().longestIncreasingPath(t.matrix);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().longestIncreasingPath(t.matrix);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "longestIncreasingPath →  A1=" << r1
                  << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (memo DFS)    : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (topo sort)   : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}