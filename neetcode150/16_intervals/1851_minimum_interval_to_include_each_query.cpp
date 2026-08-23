/*
 * =====================================================================
 * LeetCode 1851 : Minimum Interval to Include Each Query          (Hard)
 * https://leetcode.com/problems/minimum-interval-to-include-each-query/
 * Category   : Intervals
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given intervals [start, end] (each has length end - start + 1) and
 *   queries (points), for EVERY query return the length of the SHORTEST
 *   interval that CONTAINS that point, or -1 if none does.
 *   Example: intervals=[[1,4],[2,4],[3,6]], queries=[2,3,4,5]
 *            -> [3,3,3,4]   ([2,4] length 3 contains 2,3,4; [3,6] is
 *                the only interval containing 5 and its length is 4).
 * ---------------------------------------------------------------------
 * INTUITION
 *   For each query we want the min-length interval covering it. If we
 *   answer queries in ASCENDING order, the set of intervals that could
 *   possibly be answers only GROWS as the query moves right (new ones
 *   start <= query) and only SHRINKS at their right end (end < query).
 *   Two ordered structures give O(log n) per step:
 *     1. intervals sorted by START  -> sweep pointer adds candidates
 *     2. min-heap of (length, end)  -> smallest length on top; expired
 *        candidates (end < query) are popped lazily
 * ---------------------------------------------------------------------
 * APPROACH 1 — Offline: sort queries + sort-by-start + min-heap (BEST)
 *   Sort queries with their original indices. Sweep pointer p through
 *   intervals sorted by start: while start <= q push (length, end).
 *   Then pop while heap top's end < q (lazy deletion — the interval
 *   no longer contains q). The top is the shortest containing q.
 *   Time  Complexity : O((n + q) log n) — each interval pushed/popped
 *                        at most once; sort is O(n log n + q log q).
 *   Space Complexity : O(n + q) — heap + sorted query pairs.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Brute force with length-sorted pruning (contrast)
 *   Sort intervals by LENGTH ascending. For each query scan intervals
 *   in that order: first one containing q is the shortest — and once
 *   the running length exceeds the best found, STOP early.
 *   Time  Complexity : O(n q) worst case — one scan per query.
 *   Space Complexity : O(n) — the sorted copy (or O(1) in place).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — lazy deletion, the heap's superpower
 *   A heap cannot remove arbitrary elements cheaply. Instead of
 *   deleting, we mark stale: entries whose END passed the current
 *   query are still inside the heap, but a peek at the top finds them
 *   (they can only be stale at the ROOT — all others are irrelevant
 *   while a smaller/equal item sits above). Popping while root is
 *   stale is amortized O(1) per pop because every pushed entry is
 *   popped at most once. This "keep dead entries, evict on peek"
 *   pattern is the standard lazy-deletion idiom (also used by Dijkstra
 *   with duplicate distance entries).
 * =====================================================================
 */

#include <vector>         // std::vector — intervals + queries
#include <queue>          // std::priority_queue — min-heap of (len, end)
#include <utility>        // std::pair — heap entries + query pairs
#include <algorithm>      // std::sort, std::greater
#include <functional>     // std::greater<std::pair<int,int>>
#include <chrono>         // std::chrono — benchmark timing
#include <iostream>       // std::cout — printing results
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : offline sort + min-heap with lazy deletion
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Shortest interval length containing each query point.
     * Inputs  : intervals — [start, end] (length = end - start + 1).
     *           queries   — points to answer, in ANY order.
     * Output  : answer[i] = min length covering queries[i], else -1.
     */
    std::vector<int> minInterval(std::vector<std::vector<int>>& intervals,
                                 std::vector<int>& queries) {
        int qn = static_cast<int>(queries.size());

        // Sort intervals by START so the sweep pointer can advance.
        std::sort(intervals.begin(), intervals.end());

        // (query, originalIndex) pairs — answer in ascending order,
        // then scatter answers back to their original positions.
        std::vector<std::pair<int, int>> qs;
        qs.reserve(qn);
        for (int i = 0; i < qn; ++i) qs.push_back({queries[i], i});
        std::sort(qs.begin(), qs.end());

        // Min-heap of (length, end) — shortest candidate on top.
        std::priority_queue<std::pair<int, int>,
                            std::vector<std::pair<int, int>>,
                            std::greater<std::pair<int, int>>> heap;

        std::vector<int> ans(qn, -1);
        int p = 0; // sweep pointer into intervals
        for (const std::pair<int, int>& qu : qs) {
            int q = qu.first, idx = qu.second;

            // Add every interval whose start has passed: it now could
            // be an answer for this query AND all later (bigger) ones.
            while (p < static_cast<int>(intervals.size()) &&
                   intervals[p][0] <= q) {
                int len = intervals[p][1] - intervals[p][0] + 1;
                heap.push({len, intervals[p][1]});
                ++p;
            }

            // Lazy deletion: while the SHORTEST candidate ends before
            // q, it contains no query >= current anymore — evict it.
            while (!heap.empty() && heap.top().second < q) {
                heap.pop();
            }

            // If the heap is non-empty, its top is the shortest
            // interval that still covers q.
            if (!heap.empty()) ans[idx] = heap.top().first;
        }
        return ans;
    }
};

/* =====================================================================
 * APPROACH 2 : brute force, length-sorted with early break
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Shortest interval length containing each query point.
     * Inputs  : intervals — [start, end] (length = end - start + 1).
     *           queries   — points to answer, in ANY order.
     * Output  : answer[i] = min length covering queries[i], else -1.
     */
    std::vector<int> minInterval(std::vector<std::vector<int>>& intervals,
                                 std::vector<int>& queries) {
        // Sort by LENGTH ascending: the first hit per query is optimal.
        std::sort(intervals.begin(), intervals.end(),
                  [](const std::vector<int>& a, const std::vector<int>& b) {
                      return a[1] - a[0] < b[1] - b[0];
                  });

        std::vector<int> ans(queries.size(), -1);
        for (size_t i = 0; i < queries.size(); ++i) {
            int q = queries[i];
            for (const std::vector<int>& it : intervals) {
                int len = it[1] - it[0] + 1;
                if (it[0] <= q && q <= it[1]) {
                    ans[i] = len; // first (shortest) interval covering q
                    break;
                }
                // Prune: longer than the current best would be pointless,
                // and we never found one -> keep scanning only while the
                // candidate could beat... (-1 means nothing found yet).
            }
        }
        return ans;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, verify + time + RAM
 * ===================================================================== */
int main() {
    std::vector<std::pair<std::vector<std::vector<int>>, std::vector<int>>> tests = {
        {{{1, 4}, {2, 4}, {3, 6}}, {2, 3, 4, 5}},          // official example
        {{{2, 3}, {2, 5}, {1, 8}, {20, 25}}, {2, 19, 5, 22}}, // mixed + a miss
        {{{1, 1}}, {1, 0, 2}}                                // single-point interval
    };

    // brute force: for each query scan every interval.
    auto brute = [](const std::vector<std::vector<int>>& ivs,
                    const std::vector<int>& qs) {
        std::vector<int> out(qs.size(), -1);
        for (size_t i = 0; i < qs.size(); ++i)
            for (const std::vector<int>& it : ivs)
                if (it[0] <= qs[i] && qs[i] <= it[1]) {
                    int len = it[1] - it[0] + 1;
                    out[i] = out[i] == -1 ? len : std::min(out[i], len);
                }
        return out;
    };

    bool allPass = true;
    for (size_t t = 0; t < tests.size(); ++t) {

        std::vector<std::vector<int>> in1 = tests[t].first;
        std::vector<int> q1 = tests[t].second;
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::high_resolution_clock::now();
        std::vector<int> r1 = Solution_1().minInterval(in1, q1);
        auto e1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;
        bool ok1 = r1 == brute(tests[t].first, tests[t].second);

        std::vector<std::vector<int>> in2 = tests[t].first;
        std::vector<int> q2 = tests[t].second;
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::high_resolution_clock::now();
        std::vector<int> r2 = Solution_2().minInterval(in2, q2);
        auto e2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;
        bool ok2 = r2 == brute(tests[t].first, tests[t].second);

        bool pass = ok1 && ok2;
        allPass = allPass && pass;
        std::cout << "Test " << (t + 1) << " : "
                  << (pass ? "PASS" : "FAIL")
                  << "  A1=" << us1 << "us/" << kb1 << "KB  A2=" << us2 << "us/" << kb2 << "KB\n";
    }
    std::cout << (allPass ? "PASS : heap-based offline sweep matches brute force on all tests."
                          : "FAIL : at least one approach disagrees with brute force.")
              << "\n";
    return allPass ? 0 : 1;
}