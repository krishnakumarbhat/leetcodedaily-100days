/*
 * =====================================================================
 * LeetCode 53 : Maximum Subarray                                 (Medium)
 * https://leetcode.com/problems/maximum-subarray/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer array `nums`, find the CONTIGUOUS subarray with
 *   the largest sum and return that sum. A subarray is a non-empty
 *   run of consecutive elements.
 * ---------------------------------------------------------------------
 * INTUITION
 *   For every index i we ask one question: "what is the best sum of a
 *   subarray that ENDS at i?" That subarray either (a) starts fresh
 *   at i, or (b) extends the best subarray ending at i-1. Between the
 *   two, only the larger matters — anything in the middle is just a
 *   worse prefix. This "keep only the locally optimal extension"
 *   choice is greedy, and it is GLOBALLY optimal because any subarray
 *   ending at i must have a suffix ending at i-1; the best such suffix
 *   is exactly `bestEnding[i-1]`.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Kadane's algorithm (BEST, O(1) space)
 *   Invariant: after visiting index i, `ending` = largest sum of any
 *   subarray ending exactly at i, and `best` = largest over all ends.
 *   Extension is only worthwhile when it beats starting fresh:
 *     ending = max(nums[i], ending + nums[i])
 *   Time  Complexity : O(n)   — single pass.
 *   Space Complexity : O(1)   — two running scalars.
 *   WHY it is correct (exchange argument): suppose the optimal
 *   subarray is A[l..r]. The greedy `ending` at r is at least the sum
 *   of A[l..r], because at every step greedily taking max(fresh,
 *   extend) never discards the extension that builds toward A[l..r];
 *   any discarded prefix had non-positive sum, so dropping it can only
 *   make the tail bigger.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Prefix sums + minimum prefix (same O(n), other lens)
 *   sum of A[l..r] = prefix[r] - prefix[l-1]. To maximize it, fix r
 *   and use the SMALLEST prefix seen before r. Track `minPref` (the
 *   minimum prefix strictly before the current index) in one sweep.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 *   The deep reason both O(n) approaches agree: the maximum-subarray
 *   value is a single statistic of the prefix-sum walk — its maximum
 *   vertical drop. Local-optimum reasoning (Kadane) and prefix-drop
 *   reasoning (this) are two views of the SAME quantity.
 * ---------------------------------------------------------------------
 * DEEP DIVE — when is local-optimum greedy provably global?
 *   Greedy is safe here because the subproblem has the OPTIMAL
 *   SUBSTRUCTURE property: the best subarray ending at i is built
 *   solely from the best subarray ending at i-1 plus the local
 *   decision "extend or restart". There is no hidden global coupling:
 *   future elements cannot invalidate the best-extension candidate
 *   from the past. Contrast: problems where greedy FAILS (e.g. 0/1
 *   knapsack, coin change) lack this — a local choice can block a
 *   better global combination. Kadane's invariant (best suffix at i-1
 *   is all that matters for i) is what makes the exchange argument
 *   airtight.
 * =====================================================================
 */

#include <iostream>       // std::cout — benchmark output
#include <vector>         // std::vector — input array / answers
#include <string>         // std::string — PASS/FAIL messages
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RSS measurement

/* =====================================================================
 * APPROACH 1 : Kadane's algorithm
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the largest sum of a contiguous subarray.
     * Inputs  : nums — vector of integers to search inside.
     * Output  : int — maximum subarray sum.
     */
    int maxSubArray(const std::vector<int>& nums) {
        // Invariant: `ending` = best subarray sum ENDING at current i,
        // `best`    = best subarray sum ending at ANY index ≤ i.
        int ending = nums[0];
        int best = nums[0];

        // Every later element must decide: restart a fresh subarray at
        // i (nums[i]) or extend the winning subarray from i-1. Taking
        // the max is safe: a negative `ending` only drags the sum down.
        for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
            // Extend-or-restart — the one greedy decision per step.
            ending = nums[i] > ending + nums[i] ? nums[i] : ending + nums[i];
            // Keep the global champion across all end positions.
            if (ending > best) best = ending;
        }
        return best;
    }
};

/* =====================================================================
 * APPROACH 2 : Prefix sums + minimum prefix seen so far
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the largest sum of a contiguous subarray.
     * Inputs  : nums — vector of integers to search inside.
     * Output  : int — maximum subarray sum.
     */
    int maxSubArray(const std::vector<int>& nums) {
        // subarray(l..r) = prefix[r] - prefix[l-1]. For a fixed r the
        // sum is maximized by the SMALLEST prefix that came before it.
        int pref = 0;       // running prefix sum
        int minPref = 0;    // smallest prefix seen BEFORE current index
        int best = nums[0]; // best drop observed so far

        for (int x : nums) {
            pref += x;                              // grow the prefix
            int drop = pref - minPref;              // best subarray ending here
            if (drop > best) best = drop;           // new champion
            if (pref < minPref) minPref = pref;     // tighter min for later
        }
        return best;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 2-3 tests, time + peak RAM
 * ===================================================================== */
int main() {
    // Fixed samples: official examples + a hand-crafted worst case.
    const std::vector<std::vector<int> > tests = {
        { -2, 1, -3, 4, -1, 2, 1, -5, 4 }, // official → 6
        { 1 },                             // single element → 1
        { 5, 4, -1, 7, 8 }                 // all-positive start → 23
    };
    const std::vector<int> expected = { 6, 1, 23 };

    // Generic runner: times a solver against every test and reports
    // whether ALL results matched the expected values.
    auto run_all = [&](int which, int (*solve)(const std::vector<int>&)) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto t0 = std::chrono::high_resolution_clock::now();

        bool ok = true;
        for (int t = 0; t < static_cast<int>(tests.size()); ++t) {
            int got = solve(tests[t]);
            if (got != expected[t]) ok = false; // mismatch → FAIL
        }

        auto t1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);
        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1000.0;
        long mem_kb = (after.ru_maxrss - before.ru_maxrss); // delta, already KB

        std::cout << "Approach " << which
                  << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " µs  peak-ram-delta = " << mem_kb << " KB\n";
        return ok;
    };

    // Run both solvers; final verdict requires BOTH to be green.
    bool a1 = run_all(1, [](const std::vector<int>& v) { return Solution_1().maxSubArray(v); });
    bool a2 = run_all(2, [](const std::vector<int>& v) { return Solution_2().maxSubArray(v); });
    std::cout << (a1 && a2 ? "PASS : both approaches return the correct max subarray sum."
                           : "FAIL : at least one approach is wrong.") << "\n";
    return 0;
}
