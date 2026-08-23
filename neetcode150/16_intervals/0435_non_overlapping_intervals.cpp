/*
 * =====================================================================
 * LeetCode 435 : Non-overlapping Intervals                      (Medium)
 * https://leetcode.com/problems/non-overlapping-intervals/
 * Category   : Intervals
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a list of intervals [start, end], return the MINIMUM number
 *   of intervals to REMOVE so the rest are pairwise non-overlapping.
 *   Equivalently: keep the LARGEST possible non-overlapping subset.
 *   (Closed intervals: [1,2] and [2,3] DO overlap at point 2.)
 * ---------------------------------------------------------------------
 * INTUITION
 *   We cannot remove any interval unless we must; the cheapest choice
 *   is to keep the interval that leaves the most room afterwards —
 *   i.e. the one that ends EARLIEST. Greedy: sort by end, keep it,
 *   skip everything that overlaps it. WHY it is optimal (exchange
 *   argument): take any optimal keep-set; swap its first interval for
 *   the globally earliest-ending interval — it ends no later, so
 *   nothing it overlaps is lost, and the set stays valid.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Greedy: sort by END, keep the earliest-ending (BEST)
 *   Sort by end. Track the end of the last KEPT interval; every
 *   interval that starts before it overlaps the kept one -> remove.
 *   Otherwise keep it (new last end) and continue.
 *   Time  Complexity : O(n log n) — the sort.
 *   Space Complexity : O(1) — in-place sort, two counters.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort by start + DP (interval scheduling DP)
 *   dp[i] = largest non-overlapping subset among the first i sorted
 *   intervals that INCLUDES interval i:
 *       dp[i] = 1 + max{ dp[j] : j < i and end[j] <= start[i] }
 *   Answer = n - max(dp). Provably correct, no greedy leap of faith —
 *   but O(n^2) because the inner max over j scans everything.
 *   Time  Complexity : O(n^2) — nested loop over pairs.
 *   Space Complexity : O(n) — the dp table.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — the exchange argument in one paragraph
 *   Greedy needs a proof, and interval scheduling has the cleanest
 *   one: if an optimal solution keeps some interval x first and x
 *   does not end first overall, swap x for the earliest-ending
 *   interval g (end[g] <= end[x]). Since g ends no later, every
 *   interval that was compatible with x is compatible with g — the
 *   swapped set is still optimal. Repeating the swap yields the
 *   greedy solution. The DP in Approach 2 needs no such argument but
 *   pays O(n^2); the binary-search-over-dp-ends variant recovers
 *   O(n log n) with the same DP table (upper_bound on ends).
 * =====================================================================
 */

#include <vector>         // std::vector — intervals + dp table
#include <algorithm>      // std::sort, std::max
#include <chrono>         // std::chrono — benchmark timing
#include <iostream>       // std::cout — printing results
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : greedy by end time (exchange-argument optimal)
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Minimum removals so the rest are non-overlapping.
     * Inputs  : intervals — [start, end] closed intervals.
     * Output  : int — number of intervals that must be removed.
     */
    int eraseOverlapIntervals(std::vector<std::vector<int>>& intervals) {
        if (intervals.empty()) return 0;

        // Sort by END — the greedy key: finish early, leave room.
        std::sort(intervals.begin(), intervals.end(),
                  [](const std::vector<int>& a, const std::vector<int>& b) {
                      return a[1] < b[1];
                  });

        int kept = 1;                       // first interval is always kept
        int lastEnd = intervals[0][1];      // end of the last KEPT interval
        for (int i = 1; i < static_cast<int>(intervals.size()); ++i) {
            if (intervals[i][0] < lastEnd) {
                // Starts before the kept interval ends -> it overlaps
                // (closed intervals -> strict <) -> must remove it.
                continue;
            }
            // Disjoint from everything kept so far -> keep it.
            ++kept;
            lastEnd = intervals[i][1];
        }
        return static_cast<int>(intervals.size()) - kept;
    }
};

/* =====================================================================
 * APPROACH 2 : sort by start + O(n^2) DP
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Minimum removals, computed with interval-scheduling DP.
     * Inputs  : intervals — [start, end] closed intervals.
     * Output  : int — number of intervals that must be removed.
     */
    int eraseOverlapIntervals(std::vector<std::vector<int>>& intervals) {
        int n = static_cast<int>(intervals.size());
        if (n == 0) return 0;

        std::sort(intervals.begin(), intervals.end()); // by start

        // dp[i] = best kept-count of a subset whose LAST element is i.
        std::vector<int> dp(n, 1);
        int best = 1;
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                // closed intervals: j may precede i only if end[j] <= start[i]
                if (intervals[j][1] <= intervals[i][0]) {
                    dp[i] = std::max(dp[i], dp[j] + 1);
                }
            }
            best = std::max(best, dp[i]);
        }
        return n - best; // remove everything we did not keep
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, verify + time + RAM
 * ===================================================================== */
int main() {
    std::vector<std::vector<std::vector<int>>> tests = {
        {{1, 2}, {2, 3}, {3, 4}, {1, 3}},          // remove 1 ([1,3])
        {{1, 2}, {1, 2}, {1, 2}},                  // remove 2 (two duplicates)
        {{1, 100}, {11, 22}, {1, 11}, {2, 12}}     // remove 1 ([1,100])
    };

    // brute force over all subsets (tests are small): max subset that
    // stays pairwise non-overlapping = n - minimum removals.
    auto brute = [](const std::vector<std::vector<int>>& ivs) {
        int n = static_cast<int>(ivs.size()), bestKeep = 0;
        for (int mask = 0; mask < (1 << n); ++mask) {
            bool ok = true;
            int cnt = 0;
            for (int i = 0; i < n && ok; ++i) {
                if (!(mask & (1 << i))) continue;
                ++cnt;
                for (int j = i + 1; j < n; ++j)
                    if ((mask & (1 << j)) &&
                        ivs[i][0] < ivs[j][1] && ivs[j][0] < ivs[i][1]) {
                        ok = false; break; // overlapping pair inside subset
                    }
            }
            if (ok) bestKeep = std::max(bestKeep, cnt);
        }
        return n - bestKeep;
    };

    bool allPass = true;
    for (size_t t = 0; t < tests.size(); ++t) {

        std::vector<std::vector<int>> in1 = tests[t];
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_1().eraseOverlapIntervals(in1);
        auto e1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;
        bool ok1 = r1 == brute(tests[t]);

        std::vector<std::vector<int>> in2 = tests[t];
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_2().eraseOverlapIntervals(in2);
        auto e2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;
        bool ok2 = r2 == brute(tests[t]);

        bool pass = ok1 && ok2;
        allPass = allPass && pass;
        std::cout << "Test " << (t + 1) << " : "
                  << (pass ? "PASS" : "FAIL")
                  << "  A1=" << us1 << "us/" << kb1 << "KB  A2=" << us2 << "us/" << kb2 << "KB  "
                  << "removals=" << r1 << "\n";
    }
    std::cout << (allPass ? "PASS : greedy and DP agree with the exhaustive optimum."
                          : "FAIL : at least one approach disagrees with brute force.")
              << "\n";
    return allPass ? 0 : 1;
}