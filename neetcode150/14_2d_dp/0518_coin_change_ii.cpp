/*
 * =====================================================================
 * LeetCode 518 : Coin Change II                                       (Medium)
 * https://leetcode.com/problems/coin-change-ii/
 * Category   : 2D DP (unbounded knapsack, counting)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given coins of different denominations and an amount, count the
 *   number of COMBINATIONS that make up that amount (order of coins
 *   does NOT matter: 2+2+1 == 2+1+2 is ONE combination).
 * ---------------------------------------------------------------------
 * INTUITION
 *   For every coin we decide how many copies it contributes. Processing
 *   coins one at a time, "number of coins used so far" and "amount
 *   built so far" are the two axes of a 2D table. A coin may be reused
 *   any number of times → the recurrence reads the SAME ROW (i) for
 *   smaller amounts, not just the previous row.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full 2D table (BEST for understanding)
 *   dp[i][a] = ways to form amount a using ONLY the first i coins.
 *     Base: dp[i][0] = 1 for all i (empty combination = 1 way).
 *     dp[i][a] = dp[i-1][a]               (use zero copies of coin i)
 *              + dp[i][a - coins[i-1]]    (use one more copy of coin i)
 *   Time  Complexity : O(n·amount)   Space Complexity : O(n·amount)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Row-compressed 1D knapsack (BEST)
 *   The same-row dependency means the 1D array is updated LEFT→RIGHT
 *   (an ascending inner loop keeps adding copies of the current coin).
 *   Coins in the OUTER loop, amounts INNER → combinations only, never
 *   permutations.
 *   Time  Complexity : O(n·amount)   Space Complexity : O(amount)
 * ---------------------------------------------------------------------
 * DEEP DIVE — loop order is the difference between combos and perms
 *   amounts-outer / coins-inner (the "unbounded permutation" order)
 *   would count 1+2 and 2+1 as DIFFERENT ways. Coins-outer fixes the
 *   order in which denominations may appear in a sum, so each multiset
 *   of coins is generated exactly once. One-line swap, different count.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Full 2D DP table
 * ===================================================================== */
class Solution_1
{
public:
    /*
     * Purpose : Count coin combinations summing to `amount`.
     * Inputs  : amount — target sum; coins — available denominations.
     * Output  : number of combinations (order-insensitive).
     */
    int change(int amount, const std::vector<int>& coins)
    {
        const int n = static_cast<int>(coins.size());
        // dp[i][a] : ways to form a using only the first i coin types.
        std::vector<std::vector<int>> dp(n + 1, std::vector<int>(amount + 1, 0));
        for (int i = 0; i <= n; ++i)
        {
            dp[i][0] = 1; // one empty combination reaches 0
        }

        for (int i = 1; i <= n; ++i)
        {
            for (int a = 1; a <= amount; ++a)
            {
                // Exclude coin i entirely: carry the previous row.
                dp[i][a] = dp[i - 1][a];
                // Include ANOTHER copy of coin i: same row, smaller amount
                // (this is what makes the knapsack "unbounded").
                if (a >= coins[i - 1])
                {
                    dp[i][a] += dp[i][a - coins[i - 1]];
                }
            }
        }
        return dp[n][amount];
    }
};

/* =====================================================================
 * APPROACH 2 : Row-compressed 1D knapsack
 * ===================================================================== */
class Solution_2
{
public:
    /*
     * Purpose : Count coin combinations summing to `amount`.
     * Inputs  : amount — target sum; coins — available denominations.
     * Output  : number of combinations (order-insensitive).
     */
    int change(int amount, const std::vector<int>& coins)
    {
        // dp[a] : ways to form amount a with the coins processed so far.
        std::vector<int> dp(amount + 1, 0);
        dp[0] = 1;

        // COINS OUTER: the loop order that counts combinations only.
        for (const int coin : coins)
        {
            // ASCENDING: dp[a-coin] may have already used this coin → the
            // "one more copy" branch of the 2D recurrence comes for free.
            for (int a = coin; a <= amount; ++a)
            {
                dp[a] += dp[a - coin];
            }
        }
        return dp[amount];
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on the official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        int amount;
        std::vector<int> coins;
        int expected;
    };
    const std::vector<Test> tests = {
        {5, {1, 2, 5}, 4},     // official example 1
        {3, {2}, 0},           // official example 2
        {10, {10}, 1},         // official example 3
        {0, {1}, 1},           // amount 0 → empty combination
        {4, {1, 2}, 3}         // {1×4},{2×2},{1×2+2}
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().change(t.amount, t.coins);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().change(t.amount, t.coins);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "change(" << t.amount << ", [";
        for (size_t i = 0; i < t.coins.size(); ++i)
        {
            std::cout << t.coins[i] << (i + 1 < t.coins.size() ? "," : "");
        }
        std::cout << "])  A1=" << r1 << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (2D table)    : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (1D knapsack) : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}