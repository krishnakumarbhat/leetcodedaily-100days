/*
 * =====================================================================
 * LeetCode 121 : Best Time to Buy and Sell Stock                  (Easy)
 * https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
 * Category   : Sliding Window
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given `prices` where prices[i] is the price on day i, choose ONE
 *   day to buy and ONE LATER day to sell, maximizing profit
 *   (sell − buy). Return the max profit, or 0 if no profit exists.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The constraint is ORDER: buy index < sell index. This is a
 *   degenerate sliding window: as the "sell" pointer r advances,
 *   the best "buy" pointer is simply the index of the minimum price
 *   seen so far. Profit(day r) = prices[r] − min(prices[0..r−1]).
 *   The answer is the max over all r — no backtracking needed.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Brute force (all buy/sell pairs)
 *   For every buy day i, try every later sell day j and take the
 *   best difference. Correct but explores every pair.
 *   Time  Complexity : O(n²) — n(n−1)/2 pairs examined
 *   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — One pass, track the minimum price (BEST)
 *   Walk the array once. Keep minPrice = cheapest day seen so far
 *   (the optimal "buy" for any future "sell"). At each day, the best
 *   profit selling today is prices[i] − minPrice.
 *   Time  Complexity : O(n)  — single pass
 *   Space Complexity : O(1)  — two integers only
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — what makes this a "sliding window"
 *   No hash map is needed — the state is exactly ONE integer: the
 *   minimum price inside the implicit window [0 .. r−1]. The window
 *   never needs to shrink because the minimum is monotone non-
 *   increasing: min over [0..r] = min(min over [0..r−1], prices[r]).
 *   This is the same trick as Kadane's algorithm (running best),
 *   applied to the (price, minPrice) pair. C++ std::min/std::max are
 *   single CPU comparisons; the whole loop is branch-predictable.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — price arrays
#include <algorithm>      // std::min / std::max — running extremes
#include <climits>        // INT_MAX — minPrice sentinel before any day
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement (KB)

/* =====================================================================
 * APPROACH 1 : Brute force — try every (buy, sell) pair
 * ===================================================================== */
class Solution_BruteForce {
public:
    /*
     * Purpose : Return the maximum profit achievable by buying on one
     *           day and selling on a strictly later day.
     * Inputs  : prices — daily stock prices, oldest first.
     * Output  : int — best profit, or 0 if no profitable pair exists.
     */
    int maxProfit(const std::vector<int>& prices) {
        int best = 0;  // 0 = "no trade" baseline; profit may be negative

        // Buy day i: the outer loop fixes the purchase.
        for (int i = 0; i < static_cast<int>(prices.size()); ++i) {
            // Sell day j: must be AFTER i — the order constraint.
            for (int j = i + 1; j < static_cast<int>(prices.size()); ++j) {
                // Candidate profit for this single pair of days.
                best = std::max(best, prices[j] - prices[i]);
            }
        }
        return best;
    }
};

/* =====================================================================
 * APPROACH 2 : One pass — track the minimum price seen so far
 * ===================================================================== */
class Solution_OnePass {
public:
    /*
     * Purpose : Return the maximum profit achievable by buying on one
     *           day and selling on a strictly later day.
     * Inputs  : prices — daily stock prices, oldest first.
     * Output  : int — best profit, or 0 if no profitable pair exists.
     */
    int maxProfit(const std::vector<int>& prices) {
        int minPrice = INT_MAX;  // cheapest day among days visited so far
        int best = 0;            // best profit discovered so far

        for (int price : prices) {
            // A new candidate buy day: if cheaper than everything
            // before, it becomes the new left edge of the "window".
            minPrice = std::min(minPrice, price);
            // Selling TODAY against the best buy so far — the only
            // profit worth considering for this sell day.
            best = std::max(best, price - minPrice);
        }
        return best;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests + a longer series,
 * compare time and peak RAM, print PASS/FAIL per case.
 * ===================================================================== */
int main() {
    const std::vector<std::pair<std::vector<int>, int>> tests = {
        {{7, 1, 5, 3, 6, 4}, 5},  // buy 1 → sell 6 (profit 5)
        {{7, 6, 4, 3, 1}, 0},     // strictly falling → never buy
        {{2, 4, 1}, 2}            // buy 2 → sell 4 (profit 2)
    };

    bool allPass = true;
    for (const auto& t : tests) {
        const int r1 = Solution_BruteForce().maxProfit(t.first);
        const int r2 = Solution_OnePass().maxProfit(t.first);
        const bool ok = r1 == t.second && r2 == t.second;
        allPass = allPass && ok;
        std::cout << (ok ? "PASS " : "FAIL ")
                  << "prices=[";
        for (size_t i = 0; i < t.first.size(); ++i) {
            std::cout << t.first[i] << (i + 1 < t.first.size() ? "," : "");
        }
        std::cout << "] expected=" << t.second
                  << "  brute=" << r1 << "  onePass=" << r2 << "\n";
    }

    // Longer pseudo-random series (zig-zag) so both loops do real work.
    std::vector<int> bench;
    for (int i = 0; i < 2000; ++i) {
        bench.push_back(i % 2 == 0 ? (i * 37) % 1000 : 1000 - (i * 53) % 1000);
    }

    // --- Approach 1 timing ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    const int b1 = Solution_BruteForce().maxProfit(bench);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    const double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    const long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss; // KB on Linux

    // --- Approach 2 timing ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    const int b2 = Solution_OnePass().maxProfit(bench);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    const double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    const long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (brute force)  : result=" << b1
              << "  time=" << us_1 << " µs  peak-ram-delta=" << mem_1 << " KB\n";
    std::cout << "Approach 2 (one pass)     : result=" << b2
              << "  time=" << us_2 << " µs  peak-ram-delta=" << mem_2 << " KB\n";

    // Brute force is the ground truth — the O(n) pass must match it.
    allPass = allPass && (b1 == b2);
    std::cout << (allPass ? "PASS : all test cases and benchmark agree."
                          : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}