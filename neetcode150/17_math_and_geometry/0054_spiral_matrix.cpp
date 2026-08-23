/*
 * =====================================================================
 * LeetCode 54 : Spiral Matrix                                   (Medium)
 * https://leetcode.com/problems/spiral-matrix/
 * Category   : Math & Geometry
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an m×n matrix, return every element in SPIRAL order:
 *   right along the top edge, down the right edge, left along the
 *   bottom, up the left edge — shrinking inward until all cells
 *   are visited.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A spiral is just repeated boundary peeling: walk one full loop
 *   around the outer rectangle (top → right → bottom → left), then
 *   shrink the rectangle by one on every side and repeat. When the
 *   top boundary passes the bottom (or left passes right), we are
 *   done — every cell was claimed exactly once.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Boundary shrinking with 4 pointers (BEST)
 *   Keep top, bottom, left, right. Loop: sweep top row left→right,
 *   then right column top→bottom, then bottom row right→left, then
 *   left column bottom→top; shrink each bound after its sweep.
 *   Time  Complexity : O(m·n)   Space Complexity : O(1) extra
 *   (the returned vector of m·n values is the required output, not
 *   auxiliary space).
 *   WHY it works: each boundary defines one straight segment of the
 *   spiral; shrinking them in order guarantees every cell is visited
 *   once and the corner cells are never double-visited (guards like
 *   top <= bottom check the degenerate single-row/single-column case).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Layer-by-layer (recursive peeling)
 *   Same spiral, expressed as a recursion: peel the outer layer,
 *   then recurse on the inner (m-2)×(n-2) rectangle. Same O(m·n)
 *   work; the call stack costs O(min(m, n)/2) memory instead of O(1).
 *   Time  Complexity : O(m·n)   Space Complexity : O(min(m, n)/2)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the 4-pointer bound shrinking cannot skip cells
 *   The spiral partitions the grid into disjoint segments: every
 *   cell belongs to exactly one of the four sweeps of exactly one
 *   layer. Invariant: after processing layer k, all cells with
 *   k ≤ min(r, c, m-1-r, n-1-c) are visited. The layer index of any
 *   cell is min of its 4 edge distances — exactly what the guards
 *   track. Total work = Σ over layers of (perimeter) = m·n.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — formatting result lines
#include <vector>         // std::vector — matrix + spiral output
#include <unordered_map>  // (unused here; kept for uniform include set)
#include <unordered_set>  // (unused here; kept for uniform include set)
#include <chrono>         // std::chrono — steady_clock timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Boundary shrinking with 4 pointers
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return all matrix elements in spiral order.
     * Inputs  : matrix — m×n vector<vector<int>>.
     * Output  : vector<int> with elements in spiral order.
     */
    std::vector<int> spiralOrder(const std::vector<std::vector<int>>& matrix) {
        std::vector<int> out;

        // The four shrinking boundaries of the current layer.
        int top = 0;
        int bottom = static_cast<int>(matrix.size()) - 1;
        int left = 0;
        int right = static_cast<int>(matrix[0].size()) - 1;

        // Keep peeling layers until the rectangle collapses.
        while (top <= bottom && left <= right) {

            // 1) top row, left → right.
            for (int c = left; c <= right; ++c) {
                out.push_back(matrix[top][c]);
            }
            ++top;   // top edge consumed → shrink from above

            // 2) right column, top → bottom.
            for (int r = top; r <= bottom; ++r) {
                out.push_back(matrix[r][right]);
            }
            --right; // right edge consumed → shrink from the right

            // 3) bottom row, right → left. Guarded: a single-row
            //    matrix (top > bottom now) must NOT double-visit.
            if (top <= bottom) {
                for (int c = right; c >= left; --c) {
                    out.push_back(matrix[bottom][c]);
                }
                --bottom;
            }

            // 4) left column, bottom → top. Guarded: a single-column
            //    matrix must NOT double-visit the remaining column.
            if (left <= right) {
                for (int r = bottom; r >= top; --r) {
                    out.push_back(matrix[r][left]);
                }
                ++left;
            }
        }
        return out;
    }
};

/* =====================================================================
 * APPROACH 2 : Layer-by-layer recursive peeling
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return all matrix elements in spiral order.
     * Inputs  : matrix — m×n vector<vector<int>>.
     * Output  : vector<int> with elements in spiral order.
     */
    std::vector<int> spiralOrder(const std::vector<std::vector<int>>& matrix) {
        std::vector<int> out;

        // Peel one layer, then recurse on the inner rectangle. The
        // recursion exits when the layer degenerates (empty rows/cols).
        peel(matrix, 0, static_cast<int>(matrix.size()) - 1,
             0, static_cast<int>(matrix[0].size()) - 1, out);
        return out;
    }

private:
    /*
     * Purpose : Append one spiral layer to `out`, then recurse inward.
     * Inputs  : matrix — the grid; t/b/l/r — current layer bounds;
     *           out — accumulator, filled in spiral order.
     * Output  : void (out is appended in place).
     */
    void peel(const std::vector<std::vector<int>>& matrix,
              int t, int b, int l, int r, std::vector<int>& out) const {
        if (t > b || l > r) {
            return;   // layer collapsed → whole spiral is emitted
        }

        for (int c = l; c <= r; ++c) { out.push_back(matrix[t][c]); }      // top →
        for (int row = t + 1; row <= b; ++row) { out.push_back(matrix[row][r]); } // right ↓
        if (t < b) { for (int c = r - 1; c >= l; --c) { out.push_back(matrix[b][c]); } } // bottom ←
        if (l < r) { for (int row = b - 1; row > t; --row) { out.push_back(matrix[row][l]); } } // left ↑

        // Recurse one layer deeper on every side.
        peel(matrix, t + 1, b - 1, l + 1, r - 1, out);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 matrices; time + peak RAM
 * ===================================================================== */
int main() {
    const std::vector<std::vector<int>> tests[] = {
        { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } },
        { { 1, 2, 3, 4 }, { 5, 6, 7, 8 }, { 9, 10, 11, 12 } },
        { { 1 }, { 2 }, { 3 }, { 4 } },
    };
    const std::vector<int> expected[] = {
        { 1, 2, 3, 6, 9, 8, 7, 4, 5 },
        { 1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7 },
        { 1, 2, 3, 4 },
    };

    bool all_ok = true;

    const auto run_all = [&](const std::string& label, const auto& solve) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        const auto t0 = std::chrono::steady_clock::now();

        bool ok = true;
        for (size_t t = 0; t < 3; ++t) {
            const std::vector<int> got = solve(tests[t]);
            const bool pass = (got == expected[t]);
            ok = ok && pass;
            std::cout << "  test " << (t + 1) << " (" << tests[t].size() << "x"
                      << tests[t][0].size() << "): [";
            for (size_t i = 0; i < got.size(); ++i) {
                if (i) { std::cout << ","; }
                std::cout << got[i];
            }
            std::cout << "]" << (pass ? "  PASS" : "  FAIL") << "\n";
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
    run_all("Approach 1 (boundary shrinking)    ", [](const std::vector<std::vector<int>>& m) {
        return Solution_1().spiralOrder(m);
    });
    run_all("Approach 2 (recursive layer peel)  ", [](const std::vector<std::vector<int>>& m) {
        return Solution_2().spiralOrder(m);
    });

    std::cout << (all_ok
                  ? "PASS : both approaches produce the exact spiral order on all tests."
                  : "FAIL : at least one test failed.") << "\n";
    return all_ok ? 0 : 1;
}
