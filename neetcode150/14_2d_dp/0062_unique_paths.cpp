/*
 * =====================================================================
 * LeetCode 62 : Unique Paths                                         (Medium)
 * https://leetcode.com/problems/unique-paths/
 * Category   : 2D DP
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A robot sits at the top-left corner of an m×n grid and must reach
 *   the bottom-right corner. It may only move RIGHT or DOWN. Count the
 *   number of distinct paths.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every cell (r,c) can only be entered FROM the cell above it or FROM
 *   the cell to its left → the number of ways to reach (r,c) is exactly
 *   ways(above) + ways(left). That local sum rule is a recurrence, so
 *   the whole answer is one pass over a DP table.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full 2D table (BEST for understanding)
 *   dp[r][c] = number of paths from (0,0) to (r,c).
 *     Base: dp[0][*] = dp[*][0] = 1  — the first row/column can only be
 *           reached by going all-right / all-down, ONE path each.
 *     dp[r][c] = dp[r-1][c] + dp[r][c-1]   (from above) + (from left)
 *   Fill order: row-major — both dependencies are strictly "earlier".
 *   Time  Complexity : O(m·n)  — one constant-time cell computation.
 *   Space Complexity : O(m·n)  — the full table.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Row-compressed 1D array (BEST for memory)
 *   dp[r][c] only ever reads the row ABOVE (previous iteration of the
 *   SAME array) and the cell LEFT (same iteration, previous column):
 *       new dp[c] = old dp[c] + dp[c-1]
 *   So one vector of n cells suffices: after column c of row r is done,
 *   dp[c] already holds row r's value for the next row.
 *   Time  Complexity : O(m·n)   Space Complexity : O(n)   (was O(m·n))
 * ---------------------------------------------------------------------
 * DEEP DIVE — 1D compression, why it is safe
 *   When row r is computed, dp[c] still holds the (r-1) value UNTIL we
 *   overwrite it. Computing left→right, dp[c-1] was already overwritten
 *   with row r's value → we get dp[r][c-1] for free, while dp[c] (still
 *   old) supplies dp[r-1][c]. One array, both dependencies, no copies.
 *   Answer location after all rows: dp[n-1].
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Full m×n DP table
 * ===================================================================== */
class Solution_1
{
public:
    /*
     * Purpose : Count distinct robot paths across an m×n grid.
     * Inputs  : m — number of rows; n — number of columns.
     * Output  : the total number of right/down paths.
     */
    int uniquePaths(int m, int n)
    {
        // dp[r][c] : paths from (0,0) to (r,c).
        std::vector<std::vector<int>> dp(m, std::vector<int>(n, 0));

        // First row and first column: only one straight-line path each.
        for (int c = 0; c < n; ++c)
        {
            dp[0][c] = 1;
        }
        for (int r = 0; r < m; ++r)
        {
            dp[r][0] = 1;
        }

        // Interior cells: arrive from above or from the left.
        for (int r = 1; r < m; ++r)
        {
            for (int c = 1; c < n; ++c)
            {
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1];
            }
        }
        return dp[m - 1][n - 1];
    }
};

/* =====================================================================
 * APPROACH 2 : Row-compressed 1D DP
 * ===================================================================== */
class Solution_2
{
public:
    /*
     * Purpose : Count distinct robot paths across an m×n grid.
     * Inputs  : m — number of rows; n — number of columns.
     * Output  : the total number of right/down paths.
     */
    int uniquePaths(int m, int n)
    {
        // dp[c] : paths to column c of the CURRENT row being processed.
        std::vector<int> dp(n, 1); // row 0: every cell reachable 1 way

        // Every further row reuses the same vector: dp[c] (old = row r-1)
        // plus dp[c-1] (new = row r) reproduces the 2D recurrence exactly.
        for (int r = 1; r < m; ++r)
        {
            for (int c = 1; c < n; ++c)
            {
                dp[c] = dp[c] + dp[c - 1];
            }
        }
        return dp[n - 1];
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on the official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        int m;
        int n;
        int expected;
    };
    const std::vector<Test> tests = {
        {3, 7, 28},   // official example 1
        {3, 2, 3},    // official example 2
        {7, 3, 28},   // transposed grid → same count (symmetry)
        {1, 1, 1},    // degenerate single cell
        {10, 10, 48620} // binomial C(18,9) — sanity vs closed form
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().uniquePaths(t.m, t.n);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().uniquePaths(t.m, t.n);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "uniquePaths(" << t.m << ", " << t.n << ")  A1=" << r1
                  << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (2D table)   : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (1D row)     : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}