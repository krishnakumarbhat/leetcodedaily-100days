/*
 * =====================================================================
 * LeetCode 57 : Insert Interval                                  (Medium)
 * https://leetcode.com/problems/insert-interval/
 * Category   : Intervals
 * ---------------------------------------------------------------------
 * PROBLEM
 *   You are given a SORTED, non-overlapping interval list and a single
 *   `newInterval`. Insert it, merging any overlaps, and return the
 *   list still sorted and non-overlapping.
 *   Example: [[1,3],[6,9]] + [2,5] -> [[1,5],[6,9]]  ([2,5] eats [1,3]).
 * ---------------------------------------------------------------------
 * INTUITION
 *   The sortedness is the gift: intervals come in three zones.
 *     1. BEFORE zone  : end < new.start      -> copy untouched.
 *     2. MERGE zone   : touches newInterval  -> melt into one block
 *                        (min start, max end).
 *     3. AFTER zone   : start > new.end      -> copy untouched.
 *   The merge zone is ONE contiguous window of the sorted list, so a
 *   single left-to-right sweep with a phase flag is enough.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Three-phase linear sweep (BEST)
 *   Phase A: append every interval with end < new[0]. Phase B: while
 *   interval.start <= new[1], absorb it (new = [min, max]). Phase C:
 *   append everything that remains. One pass, impossible to miss a
 *   zone because the phases are exhaustive and ordered.
 *   Time  Complexity : O(n) — every interval touched exactly once.
 *   Space Complexity : O(n) — the output list.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Binary search the merge window, then splice
 *   left  = first index with end   >= new[0]  (binary search #1)
 *   right = last  index with start <= new[1]  (binary search #2)
 *   The whole merge zone is [left, right] — possibly empty (new
 *   interval slots in between). Splice: copy [0,left) + merged +
 *   (right, n). Uses the sortedness to jump straight to the zone.
 *   Time  Complexity : O(log n + n) — searches O(log n), the splice
 *                        itself is still O(n) copying.
 *   Space Complexity : O(n) — the output list.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — why binary search helps here (and in 1851)
 *   Two variants of the same question:
 *     • "first index where end >= x"   -> std::lower_bound over ends
 *     • "last  index where start <= x" -> upper_bound over starts - 1
 *   When the interval list lives in a balanced tree / sorted array,
 *   these become O(log n) window queries — the pattern behind range
 *   trees and interval trees. For ONE insert, linear sweep is simpler
 *   and equally fast; the binary-search version shines when intervals
 *   are huge (n = 10^7) or when many inserts stream in (each one
 *   O(log n) to locate + O(k) to splice).
 * =====================================================================
 */

#include <vector>         // std::vector — interval storage
#include <algorithm>      // std::sort, std::min, std::max
#include <utility>        // std::pair — coverage validator
#include <chrono>         // std::chrono — benchmark timing
#include <iostream>       // std::cout — printing results
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : three-phase linear sweep
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Insert newInterval into a sorted, disjoint interval
     *           list, merging overlaps; keep the result sorted/disjoint.
     * Inputs  : intervals    — sorted, non-overlapping [start, end] list.
     *           newInterval  — the interval to insert.
     * Output  : merged sorted interval vector.
     */
    std::vector<std::vector<int>> insert(
            std::vector<std::vector<int>>& intervals,
            std::vector<int>& newInterval) {

        std::vector<std::vector<int>> out;
        int i = 0, n = static_cast<int>(intervals.size());

        // Phase A : strictly BEFORE the new interval — ends before its
        // start means no contact at all (closed intervals).
        while (i < n && intervals[i][1] < newInterval[0]) {
            out.push_back(intervals[i]);
            ++i;
        }

        // Phase B : the merge zone. Overlap test: start <= newEnd.
        // Absorbing also extends newEnd, so the zone swallows anything
        // the growing block touches — chain merges handled for free.
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = std::min(newInterval[0], intervals[i][0]);
            newInterval[1] = std::max(newInterval[1], intervals[i][1]);
            ++i;
        }
        out.push_back(newInterval);   // the merged block, placed in order

        // Phase C : strictly AFTER — everything remaining is untouched.
        while (i < n) {
            out.push_back(intervals[i]);
            ++i;
        }
        return out;
    }
};

/* =====================================================================
 * APPROACH 2 : binary-search the merge window, then splice
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Insert newInterval via binary search + splice.
     * Inputs  : intervals    — sorted, non-overlapping interval list.
     *           newInterval  — the interval to insert.
     * Output  : merged sorted interval vector.
     */
    std::vector<std::vector<int>> insert(
            std::vector<std::vector<int>>& intervals,
            std::vector<int>& newInterval) {

        int n = static_cast<int>(intervals.size());
        // left = first index whose END >= new.start (candidate to merge).
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (intervals[mid][1] >= newInterval[0]) hi = mid;
            else lo = mid + 1;
        }
        int left = lo;

        // right = last index whose START <= new.end (candidate to merge).
        lo = -1; hi = n - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo + 1) / 2;   // +1 -> upper-mid (right bias)
            if (intervals[mid][0] <= newInterval[1]) lo = mid;
            else hi = mid - 1;
        }
        int right = lo;

        std::vector<std::vector<int>> out;
        // Copy the untouched BEFORE window.
        out.insert(out.end(), intervals.begin(), intervals.begin() + left);

        // Melt the whole window [left, right] into newInterval — the
        // window is empty when newInterval slots in without touching.
        if (left <= right) {
            newInterval[0] = std::min(newInterval[0], intervals[left][0]);
            newInterval[1] = std::max(newInterval[1], intervals[right][1]);
        }
        out.push_back(newInterval);

        // Copy the untouched AFTER window.
        out.insert(out.end(), intervals.begin() + right + 1, intervals.end());
        return out;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, verify + time + RAM
 * ===================================================================== */
int main() {
    // (intervals, newInterval) triplets.
    std::vector<std::pair<std::vector<std::vector<int>>, std::vector<int>>> tests = {
        {{{1, 3}, {6, 9}}, {2, 5}},                       // official example
        {{{1, 2}, {3, 5}, {6, 7}, {8, 10}, {12, 16}}, {4, 8}}, // official ex2
        {{{1, 3}, {4, 5}}, {6, 7}}                        // no overlap at all
    };

    // point-coverage of a set of intervals (union as a sorted int list)
    auto coverage = [](const std::vector<std::vector<int>>& ivs) {
        std::vector<int> pts;
        for (const std::vector<int>& it : ivs)
            for (int p = it[0]; p <= it[1]; ++p) pts.push_back(p);
        std::sort(pts.begin(), pts.end());
        pts.erase(std::unique(pts.begin(), pts.end()), pts.end());
        return pts;
    };

    // result must be sorted, disjoint, and cover input ∪ newInterval
    auto valid = [&](const std::vector<std::vector<int>>& res,
                     const std::vector<std::vector<int>>& base,
                     const std::vector<int>& ni) {
        for (int i = 1; i < static_cast<int>(res.size()); ++i)
            if (res[i][0] <= res[i - 1][1]) return false;
        std::vector<std::vector<int>> expect = base;
        expect.push_back(ni);
        return coverage(res) == coverage(expect);
    };

    bool allPass = true;
    for (size_t t = 0; t < tests.size(); ++t) {

        std::vector<std::vector<int>> in1 = tests[t].first;
        std::vector<int> ni1 = tests[t].second;
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::high_resolution_clock::now();
        std::vector<std::vector<int>> r1 = Solution_1().insert(in1, ni1);
        auto e1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;
        bool ok1 = valid(r1, tests[t].first, tests[t].second);

        std::vector<std::vector<int>> in2 = tests[t].first;
        std::vector<int> ni2 = tests[t].second;
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::high_resolution_clock::now();
        std::vector<std::vector<int>> r2 = Solution_2().insert(in2, ni2);
        auto e2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;
        bool ok2 = valid(r2, tests[t].first, tests[t].second);

        bool pass = ok1 && ok2;
        allPass = allPass && pass;
        std::cout << "Test " << (t + 1) << " : "
                  << (pass ? "PASS" : "FAIL")
                  << "  A1=" << us1 << "us/" << kb1 << "KB  A2=" << us2 << "us/" << kb2 << "KB  "
                  << "merged=[" << r1.size() << " blocks]\n";
    }
    std::cout << (allPass ? "PASS : both approaches insert correctly on all tests."
                          : "FAIL : at least one approach produced a wrong insert.")
              << "\n";
    return allPass ? 0 : 1;
}