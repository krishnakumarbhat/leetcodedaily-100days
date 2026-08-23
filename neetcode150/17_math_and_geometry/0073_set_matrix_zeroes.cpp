/*
 * =====================================================================
 * LeetCode 73 : Set Matrix Zeroes                               (Medium)
 * https://leetcode.com/problems/set-matrix-zeroes/
 * Category   : Math & Geometry
 * ---------------------------------------------------------------------
 * PROBLEM
 *   If a matrix cell is 0, set its ENTIRE row and column to 0,
 *   in place. Must run in O(m·n) time.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Naive: remember every zero row and column in two boolean arrays
 *   — O(m + n) extra memory. Trick: the matrix ITSELF has a spare
 *   row (row 0) and a spare column (col 0). Store the "should zero
 *   row r?" flags in cell (r, 0) and "should zero col c?" flags in
 *   cell (0, c). Only cell (0, 0) is shared by both — resolve the
 *   conflict with one extra boolean. Result: O(1) extra memory.
 * ---------------------------------------------------------------------
 * APPROACH 1 — First row/column as markers (BEST)
 *   Pass 1: walk every cell; if matrix[r][c] == 0, flag row r and
 *           column c by writing 0 into matrix[r][0] and matrix[0][c]
 *           (with matrix[0][0] standing for "row 0" and a separate
 *           bool for "column 0", since (0,0) cannot hold both).
 *   Pass 2: for every flagged row (r ≥ 1) zero the row; for every
 *           flagged column (c ≥ 1) zero the column — skipping row 0
 *           and col 0 so markers are not consumed mid-pass.
 *   Pass 3: handle row 0 and column 0 from the saved flags.
 *   Time  Complexity : O(m·n)   Space Complexity : O(1)
 *   WHY it works: the first row and first column are overwritten
 *   only AFTER being fully read in Pass 1; the markers then survive
 *   into Pass 2 untouched because we never re-write them.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Two boolean arrays (readable baseline)
 *   rows[r] and cols[c] remember which lines hold a zero; a final
 *   pass zeroes every marked line.
 *   Time  Complexity : O(m·n)   Space Complexity : O(m + n)
 *   WHY it fails the bonus: extra memory, but trivially correct and
 *   the version you write first in an interview.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why marker cells cannot be zeroed early
 *   The failure mode of a naive in-place attempt: you zero a row,
 *   and the zeros you just WROTE get re-read as "original zeros",
 *   cascading the zeroing everywhere. The marker trick sidesteps it
 *   because Pass 1 only READS original data and only WRITES to the
 *   marker row/column; Pass 2 only READS markers. The two passes
 *   never interleave — that separation is the whole algorithm.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — formatting result lines
#include <vector>         // std::vector — the matrix
#include <unordered_map>  // (unused here; kept for uniform include set)
#include <unordered_set>  // (unused here; kept for uniform include set)
#include <chrono>         // std::chrono — steady_clock timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : First row/column as markers (O(1) space)
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Zero every row and column that contains a zero.
     * Inputs  : matrix — m×n vector<vector<int>>, modified in place.
     * Output  : void (matrix is zeroed in place).
     */
    void setZeroes(std::vector<std::vector<int>>& matrix) {
        const int m = static_cast<int>(matrix.size());
        const int n = static_cast<int>(matrix[0].size());

        // (0,0) is shared by the row-0 flag and the col-0 flag, so
        // the column-0 flag lives in this dedicated boolean instead.
        bool zero_first_col = false;

        // PASS 1 — record which rows and columns must be zeroed.
        // Only WRITE to row 0 / col 0 markers; only READ original data.
        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                if (matrix[r][c] == 0) {
                    // Flag column c in the top row...
                    if (c == 0) {
                        zero_first_col = true;   // (0,0) is taken by row 0
                    } else {
                        matrix[0][c] = 0;
                    }
                    // ...and flag row r in the leftmost column.
                    matrix[r][0] = 0;
                }
            }
        }

        // PASS 2 — use the markers to zero everything EXCEPT row 0
        // and column 0 (their markers must survive this pass intact).
        for (int r = 1; r < m; ++r) {
            if (matrix[r][0] == 0) {        // row r carries a zero?
                for (int c = 1; c < n; ++c) {
                    matrix[r][c] = 0;
                }
            }
        }
        for (int c = 1; c < n; ++c) {
            if (matrix[0][c] == 0) {        // column c carries a zero?
                for (int r = 1; r < m; ++r) {
                    matrix[r][c] = 0;
                }
            }
        }

        // PASS 3 — row 0 itself, from the (0,0) marker.
        if (matrix[0][0] == 0) {
            for (int c = 1; c < n; ++c) {
                matrix[0][c] = 0;
            }
        }
        // Column 0 itself, from the dedicated boolean.
        if (zero_first_col) {
            for (int r = 0; r < m; ++r) {
                matrix[r][0] = 0;
            }
        }
    }
};

/* =====================================================================
 * APPROACH 2 : Two boolean arrays (O(m + n) space baseline)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Zero every row and column that contains a zero.
     * Inputs  : matrix — m×n vector<vector<int>>, modified in place.
     * Output  : void (matrix is zeroed in place).
     */
    void setZeroes(std::vector<std::vector<int>>& matrix) {
        const int m = static_cast<int>(matrix.size());
        const int n = static_cast<int>(matrix[0].size());

        // One flag per row and per column — O(m + n) extra memory.
        std::vector<bool> zero_row(m, false);
        std::vector<bool> zero_col(n, false);

        // Record: any zero at (r, c) marks its row and its column.
        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                if (matrix[r][c] == 0) {
                    zero_row[r] = true;
                    zero_col[c] = true;
                }
            }
        }

        // Apply: zero every marked row, then every marked column.
        for (int r = 0; r < m; ++r) {
            if (zero_row[r]) {
                for (int c = 0; c < n; ++c) {
                    matrix[r][c] = 0;
                }
            }
        }
        for (int c = 0; c < n; ++c) {
            if (zero_col[c]) {
                for (int r = 0; r < m; ++r) {
                    matrix[r][c] = 0;
                }
            }
        }
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 matrices; time + peak RAM
 * ===================================================================== */
int main() {
    const std::vector<std::vector<int>> tests[] = {
        { { 1, 1, 1 }, { 1, 0, 1 }, { 1, 1, 1 } },
        { { 0, 1, 2, 0 }, { 3, 4, 5, 2 }, { 1, 3, 1, 5 } },
        { { 1, 2, 3, 4 } },
    };
    const std::vector<std::vector<int>> expected[] = {
        { { 1, 0, 1 }, { 0, 0, 0 }, { 1, 0, 1 } },
        { { 0, 0, 0, 0 }, { 0, 4, 5, 0 }, { 0, 3, 1, 0 } },
        { { 1, 2, 3, 4 } },
    };

    bool all_ok = true;

    const auto run_all = [&](const std::string& label, const auto& solve) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        const auto t0 = std::chrono::steady_clock::now();

        bool ok = true;
        for (size_t t = 0; t < 3; ++t) {
            std::vector<std::vector<int>> m = tests[t];   // fresh copy
            solve(m);
            const bool pass = (m == expected[t]);
            ok = ok && pass;
            std::cout << "  test " << (t + 1) << " (" << m.size() << "x" << m[0].size()
                      << "):" << (pass ? "  PASS" : "  FAIL") << "\n";
        }

        const auto t1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        const double us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
        const long kb = after.ru_maxrss - before.ru_maxrss;
        std::cout << label << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " us  peak-mem = " << kb << " KB\n";
        all_ok = all_ok && ok;
    };

    std::cout << "Test suite: 3 fixed matrices\n";
    run_all("Approach 1 (first row/col markers)  ", [](std::vector<std::vector<int>>& m) {
        Solution_1().setZeroes(m);
    });
    run_all("Approach 2 (bool row/col arrays)    ", [](std::vector<std::vector<int>>& m) {
        Solution_2().setZeroes(m);
    });

    std::cout << (all_ok
                  ? "PASS : both approaches zero every marked row and column."
                  : "FAIL : at least one test failed.") << "\n";
    return all_ok ? 0 : 1;
}