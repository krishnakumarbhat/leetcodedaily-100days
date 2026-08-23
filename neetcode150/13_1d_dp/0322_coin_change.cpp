/*
 * =====================================================================
 * LeetCode 322 : Coin Change                                       (Medium)
 * https://leetcode.com/problems/coin-change/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given coin denominations `coins` (unlimited supply of each) and an
 *   amount, return the MINIMUM number of coins needed to make that
 *   amount, or -1 if it is impossible.
 * ---------------------------------------------------------------------
 * INTUITION
 *   To make amount X, the LAST coin we add is some coin c; before it
 *   we must have made amount X-c optimally. So the answer for X is
 *   1 + min over coins of (answer for X-c). The same amounts reappear
 *   from many different coin paths → overlapping subproblems. This is
 *   the UNBOUNDED KNAPSACK pattern (minimisation version).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bottom-up tabulation (BEST)
 *   dp[x] = min coins to make amount x.
 *   Recurrence : dp[x] = min( dp[x - c] + 1 ) over coins c <= x
 *                dp[0] = 0 ; dp[x] = +inf until first reached
 *   State space : x ∈ [0, amount] → amount+1 states on array dp[],
 *                filled left→right. Cell x reads EVERY dp[x-c] → the
 *                whole prefix table must stay (no rolling shortcut).
 *   Time  Complexity : O(amount × n_coins)   Space : O(amount)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down memoized recursion
 *   f(x) = min coins for x; branch over each coin and cache f(x).
 *   Trade-off : only visits reachable amounts, natural to derive;
 *               recursion depth up to amount/min-coin.
 *   Time  Complexity : O(amount × n_coins)   Space : O(amount)
 * ---------------------------------------------------------------------
 * DEEP DIVE — unbounded knapsack vs bounded coin change
 *   Because every coin can be reused any number of times, the table
 *   is filled forward (left→right) with NO reverse iteration — the
 *   "unbounded" flag. Compare with 0416 Partition Equal Subset Sum,
 *   where each item is usable ONCE → the same table must be iterated
 *   BACKWARD to avoid reusing an item.
 *   State-space math: amount+1 states × n_coins combine ops each =
 *   O(amount·n). The recurrence reads strictly SMALLER indices
 *   (x-c < x) → the dependency graph is a DAG → tabulation in index
 *   order is always safe.
 *   Real life : vending machine change dispensers, resource
 *   allocation, parcel-fill minimisation.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <sys/resource.h>
#include <algorithm>

namespace {
// Sentinel for "unreachable" amounts — must exceed any real answer.
const int INF = 1e9;
}

/* =====================================================================
 * APPROACH 1 : bottom-up tabulation
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Minimum coins to make `amount` with unlimited `coins`.
     * Inputs  : coins  — available denominations.
     *           amount — target sum.
     * Output  : int — min coins, or -1 when impossible.
     */
    int coinChange(const std::vector<int>& coins, int amount) {
        // dp[x] = min coins for x; INF marks unreachable amounts.
        std::vector<int> dp(amount + 1, INF);
        dp[0] = 0;  // zero coins make zero amount
        for (int x = 1; x <= amount; ++x) {
            for (const int c : coins) {
                // Only usable when the coin fits and the remainder exists.
                if (c <= x && dp[x - c] != INF) {
                    dp[x] = std::min(dp[x], dp[x - c] + 1);
                }
            }
        }
        return dp[amount] == INF ? -1 : dp[amount];
    }
};

/* =====================================================================
 * APPROACH 2 : top-down memoized recursion
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Minimum coins to make `amount` with unlimited `coins`.
     * Inputs  : coins  — available denominations.
     *           amount — target sum.
     * Output  : int — min coins, or -1 when impossible.
     */
    int coinChange(const std::vector<int>& coins, int amount) {
        denoms = coins;
        // memo[x] = -2 unknown, -1 impossible, else min coins for x.
        memo.assign(amount + 1, -2);
        memo[0] = 0;
        const int ans = f(amount);
        return ans >= INF ? -1 : ans;
    }

private:
    std::vector<int> denoms;
    std::vector<int> memo;

    /*
     * Purpose : Recursive amount solver with caching (top-down DP).
     * Inputs  : x — remaining amount to make.
     * Output  : int — min coins for x (INF when impossible).
     */
    int f(int x) {
        if (x < 0) {
            return INF;              // overshot → invalid path
        }
        if (memo[x] != -2) {
            return memo[x];          // overlapping subproblem → reuse
        }
        int best = INF;
        for (const int c : denoms) {
            best = std::min(best, f(x - c) + 1);  // add one coin c
        }
        return memo[x] = best;       // cache before returning
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (coins, amount, expected). Both solutions must match.
    struct Test { std::vector<int> coins; int amount; int expected; };
    const std::vector<Test> tests = {
        {{1, 2, 5}, 11, 3},   // 5+5+1
        {{2}, 3, -1},         // odd amount, even coins only → impossible
        {{1}, 0, 0}           // zero amount needs zero coins
    };

    double total_us_1 = 0.0, total_us_2 = 0.0;
    long total_kb_1 = 0, total_kb_2 = 0;
    bool allPass = true;

    for (const Test& t : tests) {
        // --- Approach 1: time via steady_clock, RAM via getrusage ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().coinChange(t.coins, t.amount);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        // ru_maxrss delta = peak RAM consumed by THIS run (KB on Linux).
        const double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        const long kb1 = after1.ru_maxrss - before1.ru_maxrss;
        total_us_1 += us1;
        total_kb_1 += kb1;

        // --- Approach 2 ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().coinChange(t.coins, t.amount);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        const double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        const long kb2 = after2.ru_maxrss - before2.ru_maxrss;
        total_us_2 += us2;
        total_kb_2 += kb2;

        const bool ok = (r1 == t.expected) && (r2 == t.expected);
        allPass = allPass && ok;

        std::cout << "A1=" << r1 << "  A2=" << r2
                  << "  expected=" << t.expected
                  << (ok ? "  PASS" : "  FAIL")
                  << "  A1 " << us1 << "µs/" << kb1 << "KB  A2 " << us2
                  << "µs/" << kb2 << "KB\n";
    }

    std::cout << "Totals: A1 " << total_us_1 << "µs/" << total_kb_1
              << "KB | A2 " << total_us_2 << "µs/" << total_kb_2 << "KB\n";
    std::cout << (allPass
                  ? "PASS : both approaches match every expected output."
                  : "FAIL : at least one answer is wrong.")
              << "\n";
    return allPass ? 0 : 1;
}