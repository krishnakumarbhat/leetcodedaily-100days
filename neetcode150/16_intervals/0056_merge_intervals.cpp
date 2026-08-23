/*
 * =====================================================================
 * LeetCode 56 : Merge Intervals                                    (Medium)
 * https://leetcode.com/problems/merge-intervals/
 * Category   : Intervals
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of intervals `intervals[i] = [start_i, end_i]`,
 *   merge ALL overlapping intervals and return the resulting array.
 *   Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
 *   because [1,3] and [2,6] share the point 2, so they melt into [1,6].
 * ---------------------------------------------------------------------
 * INTUITION
 *   Overlap is a LOCAL relation: two intervals overlap iff
 *       a.start <= b.end && b.start <= a.end
 *   (closed intervals: sharing ONE point still counts as overlap).
 *   If we SORT by start, then all intervals that touch the current
 *   merged block arrive CONSECUTIVELY — a single sweep suffices, and
 *   every merge only needs to look at the block's end.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sort by start + sweep into a result vector (BEST)
 *   Sort ascending by [start, end]. Walk the sorted list. If the
 *   current interval starts after the result's last block ends, it
 *   cannot merge with anything behind it -> append as a NEW block.
 *   Otherwise it overlaps the last block -> extend that block's end
 *   to max(lastEnd, it.end).
 *   Time  Complexity : O(n log n) — dominated by the sort; sweep O(n).
 *   Space Complexity : O(n)       — the result vector (sort is in-place).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort by start + in-place compaction (no extra vector)
 *   Same sort, same rule, but the merged blocks are written back into
 *   the FRONT of the input array (slot k), compacting it. Saves the
 *   result allocation; the input array itself becomes the answer.
 *   Time  Complexity : O(n log n) — identical asymptotic cost.
 *   Space Complexity : O(1)       — extra space, the compaction is
 *                        in-place (only the resize() tail is trimmed).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — the overlap test & why sort first
 *   Two closed intervals [a1,a2], [b1,b2] overlap when
 *       a1 <= b2 && b1 <= a2.
 *   Sorting by start turns "does it merge?" into a one-sided question:
 *       it.start <= lastEnd  ?  merge  :  new block.
 *   No hash map, no heap, no tree: a plain sort + sweep is optimal
 *   because the merge relation is transitive along the sorted order.
 *   (Contrast: for INSERT-INTERVAL style problems the same sorted
 *   sweep pattern works — one interval at a time instead of a batch.)
 * =====================================================================
 */

#include <vector>         // std::vector — intervals storage
#include <algorithm>      // std::sort, std::max — sort + merge bookkeeping
#include <utility>        // std::pair — used by the coverage validator
#include <chrono>         // std::chrono — high-resolution benchmark timing
#include <iostream>       // std::cout — printing PASS/FAIL + timings
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Sort by start, sweep, merge into a result vector
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Merge all overlapping intervals in `intervals`.
     * Inputs  : intervals — vector of [start, end] closed intervals.
     * Output  : vector of merged, non-overlapping, start-sorted intervals.
     */
    std::vector<std::vector<int>> merge(std::vector<std::vector<int>>& intervals) {
        // Sort lexicographically: by start first, then by end.
        // Overlapping intervals become neighbours — the whole trick.
        std::sort(intervals.begin(), intervals.end());

        std::vector<std::vector<int>> out;
        for (const std::vector<int>& it : intervals) {

            if (out.empty() || out.back()[1] < it[0]) {
                // Previous block ends BEFORE this one starts -> no overlap:
                // it is guaranteed disjoint from everything behind it too.
                out.push_back(it);
            } else {
                // Overlap (or touching) -> absorb it into the current block
                // by extending the block's end as far as needed.
                out.back()[1] = std::max(out.back()[1], it[1]);
            }
        }
        return out;
    }
};

/* =====================================================================
 * APPROACH 2 : Sort by start, merge IN-PLACE (compaction)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Merge all overlapping intervals, reusing `intervals`
     *           itself as the output buffer (in-place compaction).
     * Inputs  : intervals — vector of [start, end] closed intervals.
     * Output  : the same vector, compacted to the merged blocks.
     */
    std::vector<std::vector<int>> merge(std::vector<std::vector<int>>& intervals) {
        // Sorting mutates the input — we are allowed to own it here.
        std::sort(intervals.begin(), intervals.end());

        // k = number of merged blocks already written to the front.
        int k = 0;
        for (int i = 1; i < static_cast<int>(intervals.size()); ++i) {

            if (intervals[k][1] >= intervals[i][0]) {
                // Block k overlaps intervals[i] -> extend block k in place.
                intervals[k][1] = std::max(intervals[k][1], intervals[i][1]);
            } else {
                // No overlap -> promote intervals[i] to be the next block.
                ++k;
                intervals[k] = intervals[i];
            }
        }
        // Trim the stale tail — everything past k was absorbed.
        intervals.resize(k + 1);
        return intervals;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, verify + time + RAM
 * ===================================================================== */
int main() {
    // Three fixed tests. The validator proves correctness WITHOUT a
    // reference implementation: the union of points covered by the
    // input must equal the union covered by the merged output.
    std::vector<std::vector<std::vector<int>>> tests = {
        {{1, 3}, {2, 6}, {8, 10}, {15, 18}},        // official example
        {{1, 4}, {4, 5}},                            // touching at 4 -> merges
        {{1, 4}, {0, 2}, {3, 5}, {6, 7}, {6, 9}, {10, 11}} // chains + dup starts
    };

    // coverage : the set of integer points an interval set covers.
    auto coverage = [](const std::vector<std::vector<int>>& ivs) {
        std::vector<int> pts;
        for (const std::vector<int>& it : ivs)
            for (int p = it[0]; p <= it[1]; ++p) pts.push_back(p);
        std::sort(pts.begin(), pts.end());
        pts.erase(std::unique(pts.begin(), pts.end()), pts.end());
        return pts;
    };

    // valid : output must be sorted, non-overlapping, and cover the
    // exact same point set as the input (union preserved).
    auto valid = [&](const std::vector<std::vector<int>>& res,
                     const std::vector<std::vector<int>>& orig) {
        for (int i = 1; i < static_cast<int>(res.size()); ++i)
            if (res[i][0] <= res[i - 1][1]) return false;   // overlap or unsorted
        std::vector<int> a = coverage(res), b = coverage(orig);
        return a == b;
    };

    bool allPass = true;
    for (size_t t = 0; t < tests.size(); ++t) {

        // --- Approach 1 ---
        std::vector<std::vector<int>> in1 = tests[t];
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto t0 = std::chrono::high_resolution_clock::now();
        std::vector<std::vector<int>> r1 = Solution_1().merge(in1);
        auto t1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1000.0;
        long kb1 = (after1.ru_maxrss - before1.ru_maxrss); // ru_maxrss is already KB on Linux
        bool ok1 = valid(r1, tests[t]);

        // --- Approach 2 ---
        std::vector<std::vector<int>> in2 = tests[t];
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto t2 = std::chrono::high_resolution_clock::now();
        std::vector<std::vector<int>> r2 = Solution_2().merge(in2);
        auto t3 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(t3 - t2).count() / 1000.0;
        long kb2 = (after2.ru_maxrss - before2.ru_maxrss);
        bool ok2 = valid(r2, tests[t]);

        bool pass = ok1 && ok2;
        allPass = allPass && pass;
        std::cout << "Test " << (t + 1) << " : "
                  << (pass ? "PASS" : "FAIL")
                  << "  A1=" << us1 << "us/" << kb1 << "KB  A2=" << us2 << "us/" << kb2 << "KB  "
                  << "merged=[" << r1.size() << " blocks]\n";
    }
    std::cout << (allPass ? "PASS : both approaches merge all tests correctly."
                          : "FAIL : at least one approach produced a wrong merge.")
              << "\n";
    return allPass ? 0 : 1;
}