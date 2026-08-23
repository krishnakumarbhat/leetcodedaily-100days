/*
 * =====================================================================
 * LeetCode 309 : Best Time to Buy and Sell Stock with Cooldown      (Medium)
 * https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
 * Category   : 2D DP (state DP)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   You may buy/sell stock on days 0..n-1 at prices[i]. You may hold
 *   at most one share, may NOT buy on the day after a sale (1-day
 *   cooldown), and may make unlimited transactions. Maximize profit.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every day ends in one of three states: HOLDING a share, SOLD today
 *   (cooldown starts), or RESTING (no share, no cooldown). Each state
 *   only transitions from the previous day's states → a state-machine
 *   DP, written as a (days × 3-states) table.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full state-table DP (BEST for understanding)
 *   dp[i][0] = max cash while HOLDING at end of day i
 *   dp[i][1] = max cash after SELLING on day i (entering cooldown)
 *   dp[i][2] = max cash RESTING at end of day i (no share, free to buy)
 *     dp[i][0] = max(dp[i-1][0], dp[i-1][2] - prices[i])  (hold / buy)
 *     dp[i][1] = dp[i-1][0] + prices[i]                   (sell today)
 *     dp[i][2] = max(dp[i-1][2], dp[i-1][1])              (stay rest /
 *                                                          cooldown over)
 *   Time  Complexity : O(n)   Space Complexity : O(n)  (3·n cells)
 * ---------------------------------------------------------------------
 * APPROACH 2 — O(1) state variables (BEST for memory)
 *   Day i only reads day i-1 → keep three running variables.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why cooldown is a STATE, not a constraint check
 *   The cooldown only blocks a BUY one day after a SELL — so the past
 *   that matters is exactly "did I just sell?" That single bit of
 *   history is what the SOLD state encodes. All three transitions are
 *   mutually exclusive and exhaustive, so max() over them is exact.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Full state table dp[i][0..2]
 * ===================================================================== */
class Solution_1
{
public:
    /*
     * Purpose : Compute maximum profit with a 1-day cooldown.
     * Inputs  : prices — daily stock prices.
     * Output  : the maximum achievable profit.
     */
    int maxProfit(const std::vector<int>& prices)
    {
        const int n = static_cast<int>(prices.size());
        if (n <= 1)
        {
            return 0; // need at least one buy + one sell
        }
        // dp[i][0..2] : hold / just-sold / rest states at end of day i.
        std::vector<std::vector<int>> dp(n, std::vector<int>(3, 0));
        dp[0][0] = -prices[0]; // day 0: only option is to buy

        for (int i = 1; i < n; ++i)
        {
            // Hold: keep yesterday's share, or buy today (must be resting).
            dp[i][0] = std::max(dp[i - 1][0], dp[i - 1][2] - prices[i]);
            // Sell today: you must have been holding yesterday.
            dp[i][1] = dp[i - 1][0] + prices[i];
            // Rest: keep resting, or the cooldown from yesterday ended.
            dp[i][2] = std::max(dp[i - 1][2], dp[i - 1][1]);
        }
        // Best end state: sold today or resting (holding is never better
        // than selling, but max covers all).
        return std::max(dp[n - 1][1], dp[n - 1][2]);
    }
};

/* =====================================================================
 * APPROACH 2 : O(1) rolling state variables
 * ===================================================================== */
class Solution_2
{
public:
    /*
     * Purpose : Compute maximum profit with a 1-day cooldown.
     * Inputs  : prices — daily stock prices.
     * Output  : the maximum achievable profit.
     */
    int maxProfit(const std::vector<int>& prices)
    {
        const int n = static_cast<int>(prices.size());
        if (n <= 1)
        {
            return 0;
        }
        int hold = -prices[0]; // dp[i-1][0]
        int sold = 0;          // dp[i-1][1]
        int rest = 0;          // dp[i-1][2]

        for (int i = 1; i < n; ++i)
        {
            // Compute the new states from the OLD ones (reads happen
            // before writes — exactly the 2D row-dependency structure).
            const int newHold = std::max(hold, rest - prices[i]);
            const int newSold = hold + prices[i];
            const int newRest = std::max(rest, sold);
            hold = newHold;
            sold = newSold;
            rest = newRest;
        }
        return std::max(sold, rest);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on the official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        std::vector<int> prices;
        int expected;
    };
    const std::vector<Test> tests = {
        {{1, 2, 3, 0, 2}, 3},   // official example 1
        {{1}, 0},               // official example 2 (single day)
        {{2, 1, 4}, 3},         // buy at 1, sell at 4
        {{1, 2, 4}, 3},         // buy at 1, sell at 4 (no cooldown penalty)
        {{6, 1, 3, 2, 4, 7}, 6} // buy 1 → sell 3, cooldown, buy 2 → sell 7
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().maxProfit(t.prices);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().maxProfit(t.prices);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "maxProfit([";
        for (size_t i = 0; i < t.prices.size(); ++i)
        {
            std::cout << t.prices[i] << (i + 1 < t.prices.size() ? "," : "");
        }
        std::cout << "])  A1=" << r1 << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (state table) : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (O(1) states) : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}