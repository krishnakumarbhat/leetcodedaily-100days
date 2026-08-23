/*
 * =====================================================================
 * LeetCode 48 : Rotate Image                                     (Medium)
 * https://leetcode.com/problems/rotate-image/
 * Category   : Math & Geometry
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Rotate an n×n matrix 90 degrees CLOCKWISE, in place, with O(1)
 *   extra memory. Every cell (r, c) must move to (c, n-1-r).
 * ---------------------------------------------------------------------
 * INTUITION
 *   A 90° clockwise rotation is two cheap linear-algebra steps:
 *   transpose (swap rows ↔ columns) followed by reversing every row.
 *   Both steps are easily done in place, so the whole rotation costs
 *   zero extra memory.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Transpose + reverse (BEST)
 *   Step 1: transpose — swap (r, c) with (c, r) for r < c only.
 *   Step 2: reverse each row — the "flip" that turns a transpose
 *           (a mirror across the main diagonal) into a full 90° turn.
 *   Time  Complexity : O(n²)   Space Complexity : O(1)
 *   WHY it works: transpose maps (r,c)→(c,r); reversing row r maps
 *   (r,c)→(r,n-1-c). Composing: (r,c)→(c,r)→(c,n-1-r) — exactly the
 *   90° clockwise rule. Two O(1)-space passes, trivial to verify.
 * ---------------------------------------------------------------------
 * APPROACH 2 — In-place 4-way ring swaps
 *   Rotate by rings: for each ring layer and each position on the top
 *   edge, move the 4 partners in a cycle
 *       top ← left ← bottom ← right ← top
 *   using one temp variable. No transpose needed; one pass per cell.
 *   Time  Complexity : O(n²)   Space Complexity : O(1)
 *   WHY it works: the orbit of (r,c) under a 90° rotation is a cycle
 *   of length 4 (rotating four times returns home), and the four
 *   partners are (r,c) → (c,n-1-r) → (n-1-r,n-1-c) → (n-1-c,r).
 * ---------------------------------------------------------------------
 * DEEP DIVE — matrix transforms as linear algebra
 *   Rotation is the linear map R = [[0,-1],[1,0]] in matrix form.
 *   Transpose T swaps indices; row-reversal F flips the second index.
 *   The identity F·T = R (right-multiply check: (F·T)(r,c) = F(c,r)
 *   = (c, n-1-r)) is why "transpose then reverse rows" is EXACTLY a
 *   90° turn — no angles, no trigonometry, just index arithmetic.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — formatting rows for output
#include <vector>         // std::vector — the matrix
#include <unordered_map>  // (unused here; kept for uniform include set)
#include <unordered_set>  // (unused here; kept for uniform include set)
#include <chrono>         // std::chrono — steady_clock timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Transpose, then reverse every row
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Rotate an n×n matrix 90° clockwise, in place.
     * Inputs  : matrix — n×n vector<vector<int>>, modified in place.
     * Output  : void (the matrix reference is rotated in place).
     */
    void rotate(std::vector<std::vector<int>>& matrix) {
        const int n = static_cast<int>(matrix.size());

        // STEP 1 — transpose: mirror across the main diagonal.
        // Only visit r < c so each pair is swapped exactly once.
        for (int r = 0; r < n; ++r) {
            for (int c = r + 1; c < n; ++c) {
                const int tmp = matrix[r][c];
                matrix[r][c] = matrix[c][r];
                matrix[c][r] = tmp;
            }
        }

        // STEP 2 — reverse every row: this flips the mirrored image
        // into a proper clockwise quarter-turn.
        for (int r = 0; r < n; ++r) {
            int lo = 0;
            int hi = n - 1;
            while (lo < hi) {
                const int tmp = matrix[r][lo];
                matrix[r][lo] = matrix[r][hi];
                matrix[r][hi] = tmp;
                ++lo;
                --hi;
            }
        }
    }
};

/* =====================================================================
 * APPROACH 2 : In-place 4-way ring swaps (single pass)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Rotate an n×n matrix 90° clockwise via ring cycles.
     * Inputs  : matrix — n×n vector<vector<int>>, modified in place.
     * Output  : void (the matrix reference is rotated in place).
     */
    void rotate(std::vector<std::vector<int>>& matrix) {
        const int n = static_cast<int>(matrix.size());

        // Peel the matrix ring by ring: ring `i` spans rows/cols i ..
        // n-1-i. The innermost ring (n odd) is a single cell — no move.
        for (int i = 0; i < n / 2; ++i) {
            const int last = n - 1 - i;
            // j walks along the TOP edge of the ring; each position
            // rotates exactly 4 cells (its full orbit).
            for (int j = i; j < last; ++j) {
                const int offset = j - i;   // how far along the edge

                // Save top; then fill top ← left ← bottom ← right.
                const int top = matrix[i][j];

                // left → top   (cell (last-offset, i) moves up)
                matrix[i][j] = matrix[last - offset][i];

                // bottom → left (cell (last, last-offset) moves left)
                matrix[last - offset][i] = matrix[last][last - offset];

                // right → bottom (cell (j, last) moves down)
                matrix[last][last - offset] = matrix[j][last];

                // saved top → right (cell (i, j) moves right)
                matrix[j][last] = top;
            }
        }
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 matrices; time + peak RAM
 * ===================================================================== */
int main() {
    // Three fixed tests. Each expected matrix is the true 90° turn.
    const std::vector<std::vector<int>> tests[] = {
        { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } },
        { { 5, 1, 9, 11 }, { 2, 4, 8, 10 }, { 13, 3, 6, 7 }, { 15, 14, 12, 16 } },
        { { 1 } },
    };
    const std::vector<std::vector<int>> expected[] = {
        { { 7, 4, 1 }, { 8, 5, 2 }, { 9, 6, 3 } },
        { { 15, 13, 2, 5 }, { 14, 3, 4, 1 }, { 12, 6, 8, 9 }, { 16, 7, 10, 11 } },
        { { 1 } },
    };

    // Helper: pretty-print one matrix as a row string for the report.
    const auto to_str = [](const std::vector<std::vector<int>>& m) {
        std::string out = "{";
        for (size_t r = 0; r < m.size(); ++r) {
            out += (r ? "},{" : "");
            for (size_t c = 0; c < m[r].size(); ++c) {
                if (c) { out += ","; }
                out += std::to_string(m[r][c]);
            }
        }
        return out + "}";
    };

    bool all_ok = true;

    // Time both solutions over all tests; memory = delta of ru_maxrss.
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
            std::cout << "  test " << (t + 1) << " (n=" << m.size() << "): "
                      << to_str(m) << (pass ? "  PASS" : "  FAIL") << "\n";
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
    run_all("Approach 1 (transpose + reverse)   ", [](std::vector<std::vector<int>>& m) {
        Solution_1().rotate(m);
    });
    run_all("Approach 2 (4-way ring swaps)      ", [](std::vector<std::vector<int>>& m) {
        Solution_2().rotate(m);
    });

    std::cout << (all_ok
                  ? "PASS : both approaches produce the exact 90° rotation on all tests."
                  : "FAIL : at least one test failed.") << "\n";
    return all_ok ? 0 : 1;
}
