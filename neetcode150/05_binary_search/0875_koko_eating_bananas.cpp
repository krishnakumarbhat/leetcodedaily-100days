/*
 * =====================================================================
 * LeetCode 0875 : Koko Eating Bananas                                (Medium)
 * https://leetcode.com/problems/koko-eating-bananas/
 * Category   : Binary Search (on the ANSWER space)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Koko must eat `piles[i]` bananas from pile i; she eats at most `k`
 *   bananas per hour, takes ⌈piles[i]/k⌉ hours per pile, and may not
 *   move on until a pile is finished. Return the MINIMUM k that lets
 *   her finish all piles within `h` hours.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The speed k lives in [1, max(piles)]. "canFinish(k)" is a
 *   monotone predicate: k too small → FALSE, once k is large enough →
 *   TRUE forever (faster can never need MORE hours). The answer is
 *   the FIRST TRUE speed — a textbook lower-bound binary search.
 *   This is the "binary search on the answer" pattern: the data is
 *   not searched directly; the PREDICATE over the answer space is.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Binary search on speed (BEST, O(n log maxPile))
 *   lo = 1, hi = max(piles). Probe mid = (lo+hi)/2 and evaluate
 *   canFinish(mid) in O(n) by summing ⌈piles[i]/mid⌉. If it finishes
 *   in ≤ h hours → mid is feasible, so the optimum is mid or less
 *   (hi = mid). Otherwise mid is too slow (lo = mid + 1). The loop
 *   `lo < hi` collapses onto the smallest feasible speed.
 *   Time  Complexity : O(n log M)   M = max(piles); every probe is
 *                        an O(n) sweep and there are log M probes.
 *   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Linear sweep of speeds (contrast, O(n·M))
 *   Try every k from 1 to max(piles) and return the first feasible
 *   one. Identical result, but with max(piles) = 1e9 it would take
 *   a billion sweeps — the O(log M) probe count of approach 1 is
 *   what makes the difference at scale.
 *   Time  Complexity : O(n·M)   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — searching the ANSWER space, not the data
 *   In 0704 the predicate was "nums[i] == target" over indices; here
 *   the predicate is "canFinish(k)" over SPEEDS. Both are monotone,
 *   so the same halving loop applies — this is why lower_bound-style
 *   BS generalizes: you only need (1) a bounded monotone answer
 *   range and (2) an O(f(n)) feasibility oracle. That combination is
 *   everywhere in real systems: rate limiting ("fastest rate that
 *   still passes QoS"), network congestion control, job scheduling
 *   ("minimum throughput that meets the deadline"), and capacity
 *   planning (maximizing throughput under latency budgets).
 * =====================================================================
 */

#include <iostream>     // std::cout — printing results
#include <vector>       // std::vector — the piles array
#include <string>       // std::string — PASS/FAIL verdicts
#include <unordered_map>// (included per section convention; unused here)
#include <map>          // (included per section convention; unused here)
#include <algorithm>    // std::max — max pile scan
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Binary search on the speed (minimize feasible k)
 * ===================================================================== */
class Solution_BinarySearchSpeed {
public:
    /*
     * Purpose : Return the minimum eating speed that finishes in h hours.
     * Inputs  : piles — vector<int> of bananas per pile.
     *           h     — hours available (h >= piles.size()).
     * Output  : int minimum feasible speed k.
     */
    int minEatingSpeed(const std::vector<int>& piles, int h) {
        // The answer lives in [1, max(piles)] — the speed space.
        int lo = 1;
        int hi = 1;
        for (size_t i = 0; i < piles.size(); ++i) {
            hi = std::max(hi, piles[i]);       // upper bound: 1 pile/hour worst case.
        }

        // `lo < hi` + hi = mid collapses onto the FIRST feasible k.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;      // probe a speed.

            // canFinish(mid): sum of ceil(pile/mid) must be <= h.
            long long hours = 0;
            for (size_t i = 0; i < piles.size(); ++i) {
                // ceil(a/b) = (a + b - 1) / b — integer division trick.
                hours += (piles[i] + mid - 1) / mid;
            }

            if (hours <= h) {
                hi = mid;                      // feasible → try slower.
            } else {
                lo = mid + 1;                  // too slow → speed up.
            }
        }

        return lo;                             // smallest feasible speed.
    }
};

/* =====================================================================
 * APPROACH 2 : Linear sweep of speeds (contrast)
 * ===================================================================== */
class Solution_LinearSpeed {
public:
    /*
     * Purpose : Return the minimum eating speed that finishes in h hours.
     * Inputs  : piles — vector<int> of bananas per pile.
     *           h     — hours available (h >= piles.size()).
     * Output  : int minimum feasible speed k.
     */
    int minEatingSpeed(const std::vector<int>& piles, int h) {
        int hi = 1;
        for (size_t i = 0; i < piles.size(); ++i) {
            hi = std::max(hi, piles[i]);
        }

        // Try every speed from 1 upward; first feasible one wins.
        for (int k = 1; k <= hi; ++k) {
            long long hours = 0;
            for (size_t i = 0; i < piles.size(); ++i) {
                hours += (piles[i] + k - 1) / k;
            }
            if (hours <= h) {
                return k;                      // smallest feasible speed.
            }
        }
        return hi;                             // unreachable per constraints.
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, print time + peak RAM
 * ===================================================================== */
int main() {
    // Test cases from the official examples.
    std::vector<std::pair<std::vector<int>, int>> tests = {
        { {3, 6, 7, 11}, 8 },                  // expect 4
        { {30, 11, 23, 4, 20}, 5 },            // expect 30
        { {30, 11, 23, 4, 20}, 6 }             // expect 23
    };

    for (size_t t = 0; t < tests.size(); ++t) {
        const std::vector<int>& piles = tests[t].first;
        int h = tests[t].second;

        // --- Approach 1 timing + peak-RAM delta ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto start1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_BinarySearchSpeed().minEatingSpeed(piles, h);
        auto end1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        long kb1 = after1.ru_maxrss - before1.ru_maxrss; // ru_maxrss is KB on Linux

        // --- Approach 2 timing + peak-RAM delta ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto start2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_LinearSpeed().minEatingSpeed(piles, h);
        auto end2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        long kb2 = after2.ru_maxrss - before2.ru_maxrss;

        // --- Verdict: both must agree with each other ---
        bool ok = (r1 == r2);
        std::cout << "Test " << (t + 1) << ": h=" << h
                  << " | A1 BS-speed = " << r1 << " (" << us1 << " us, +"
                  << kb1 << " KB) | A2 linear = " << r2 << " (" << us2
                  << " us, +" << kb2 << " KB) | " << (ok ? "PASS" : "FAIL")
                  << "\n";
    }

    return 0;
}