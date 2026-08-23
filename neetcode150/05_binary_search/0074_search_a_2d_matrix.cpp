/*
 * =====================================================================
 * LeetCode 0074 : Search a 2D Matrix                                (Medium)
 * https://leetcode.com/problems/search-a-2d-matrix/
 * Category   : Binary Search
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an m x n matrix where each row is sorted ASCENDING and the
 *   first value of every row is greater than the last value of the
 *   previous row (rows are "linked"), search for `target`. Return
 *   true if found, false otherwise. Must run in O(log(m·n)).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Because rows are chained (row[i][0] > row[i-1][n-1]), reading
 *   the matrix row-by-row yields ONE fully sorted array of m·n
 *   elements. A single binary search over that virtual array is the
 *   whole solution; the only trick is mapping the flat index
 *   mid -> (mid/n, mid%n). The matrix is sorted; search it like 0704.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Flattened-index binary search (BEST, O(log(m·n)))
 *   Binary search over [0, m*n). For each probe index `mid`, the
 *   matrix coordinates are row = mid / n, col = mid % n — division
 *   and modulo of an INTEGER index, no copy needed. Compare, then
 *   discard half the flattened array exactly like 0704.
 *   Time  Complexity : O(log(m·n))   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Two-level binary search (O(log m + log n))
 *   Phase 1: binary search the FIRST COLUMN to find the unique row
 *   that could hold target (last row with first-value <= target —
 *   the lower_bound of target in column 0, minus one). Phase 2:
 *   plain 0704 binary search inside that row. Conceptually nicer
 *   (two clean 1D searches), one extra boundary check, and log m +
 *   log n steps vs log(m·n) — asymptotically identical.
 *   Time  Complexity : O(log m + log n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * DEEP DIVE — the flat-index invariant
 *   A m·n matrix is "row-major": virtual index k maps to (k/n, k%n),
 *   and the chained-rows property makes virtual[k] strictly sorted.
 *   So the 0704 invariant ("answer in [lo, hi]") transfers verbatim
 *   to the flattened array — the probe is the only difference:
 *   nums[k] becomes matrix[k/n][k%n]. This "pretend the structure
 *   is a flat array" trick generalizes: segment trees, sparse
 *   tables, and SQL row-wise storage all rely on the same mapping.
 *   Approach 2's phase-1 is the false→true predicate again:
 *   "matrix[r][0] <= target" is false then true down column 0.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing results
#include <vector>       // std::vector — the matrix and its rows
#include <string>       // std::string — PASS/FAIL verdicts
#include <unordered_map>// (included per section convention; unused here)
#include <map>          // (included per section convention; unused here)
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Single binary search over the flattened index space
 * ===================================================================== */
class Solution_FlattenedBS {
public:
    /*
     * Purpose : Decide whether `target` exists in the sorted matrix.
     * Inputs  : matrix — m x n sorted-and-chained rows of ints.
     *           target — integer being searched for.
     * Output  : bool true if found, false otherwise.
     */
    bool searchMatrix(const std::vector<std::vector<int>>& matrix, int target) {
        int m = static_cast<int>(matrix.size());
        int n = static_cast<int>(matrix[0].size());

        // Virtual array size = m*n; invariant: target lives in [lo,hi].
        int lo = 0;
        int hi = m * n - 1;

        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;      // probe in the FLAT array.

            // Map the flat index to 2D coordinates: row-major order.
            int r = mid / n;                   // how many full rows fit.
            int c = mid % n;                   // leftover position in row.
            int v = matrix[r][c];              // virtual[mid] = matrix[r][c].

            if (v == target) {
                return true;                   // exact hit.
            }
            if (v < target) {
                lo = mid + 1;                  // discard left half.
            } else {
                hi = mid - 1;                  // discard right half.
            }
        }

        return false;                          // window inverted → absent.
    }
};

/* =====================================================================
 * APPROACH 2 : Find the row (first column), then search within it
 * ===================================================================== */
class Solution_TwoLevelBS {
public:
    /*
     * Purpose : Decide whether `target` exists in the sorted matrix.
     * Inputs  : matrix — m x n sorted-and-chained rows of ints.
     *           target — integer being searched for.
     * Output  : bool true if found, false otherwise.
     */
    bool searchMatrix(const std::vector<std::vector<int>>& matrix, int target) {
        int m = static_cast<int>(matrix.size());
        int n = static_cast<int>(matrix[0].size());

        // --- Phase 1: binary search column 0 for the candidate row ---
        // Predicate "matrix[row][0] <= target" is false→true down the
        // column; we want the LAST true row (lower_bound minus one).
        int lo = 0;
        int hi = m - 1;
        int row = 0;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (matrix[mid][0] <= target) {
                row = mid;                     // feasible row — keep going down.
                lo = mid + 1;
            } else {
                hi = mid - 1;                  // first value too big — go up.
            }
        }

        // --- Phase 2: plain 0704 binary search inside that row ---
        lo = 0;
        hi = n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int v = matrix[row][mid];
            if (v == target) {
                return true;
            }
            if (v < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }

        return false;                          // not in the candidate row.
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, print time + peak RAM
 * ===================================================================== */
int main() {
    // The official example matrix plus edge-case shapes.
    std::vector<std::vector<int>> matrix = {
        {1, 3, 5, 7},
        {10, 11, 16, 20},
        {23, 30, 34, 60}
    };
    std::vector<int> targets = {3, 13, 60, 1};   // hit, miss, edge hit, corner.

    for (size_t t = 0; t < targets.size(); ++t) {
        int target = targets[t];

        // --- Approach 1 timing + peak-RAM delta ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto start1 = std::chrono::high_resolution_clock::now();
        bool r1 = Solution_FlattenedBS().searchMatrix(matrix, target);
        auto end1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        long kb1 = after1.ru_maxrss - before1.ru_maxrss; // ru_maxrss is KB on Linux

        // --- Approach 2 timing + peak-RAM delta ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto start2 = std::chrono::high_resolution_clock::now();
        bool r2 = Solution_TwoLevelBS().searchMatrix(matrix, target);
        auto end2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        long kb2 = after2.ru_maxrss - before2.ru_maxrss;

        // --- Verdict: linear scan of the flattened matrix is truth ---
        bool expect = false;
        for (const auto& row : matrix) {
            for (int v : row) {
                if (v == target) { expect = true; }
            }
        }
        bool ok = (r1 == expect) && (r2 == expect);

        std::cout << "Test " << (t + 1) << ": target " << target
                  << " | A1 flattened = " << (r1 ? "true" : "false") << " ("
                  << us1 << " us, +" << kb1 << " KB) | A2 two-level = "
                  << (r2 ? "true" : "false") << " (" << us2 << " us, +"
                  << kb2 << " KB) | expect " << (expect ? "true" : "false")
                  << " | " << (ok ? "PASS" : "FAIL") << "\n";
    }

    return 0;
}