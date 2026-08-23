/*
 * =====================================================================
 * LeetCode 494 : Target Sum                                          (Medium)
 * https://leetcode.com/problems/target-sum/
 * Category   : 2D DP
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer array nums and a target, assign each nums[i] the
 *   sign + or − and count how many distinct assignments make the signed
 *   sum equal to target.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Process numbers one at a time. After i numbers, only ONE thing
 *   matters for the future: the accumulated sum s. The number of ways
 *   to reach s after i numbers is the sum of the ways to reach s−nums[i]
 *   and s+nums[i] after i−1 numbers → a 2D DP over (i, sum).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full 2D table over offset sums (BEST for understanding)
 *   dp[i][s] = ways to reach sum s using the FIRST i numbers.
 *     Base: dp[0][0] = 1 (one way to reach 0 with no numbers).
 *     dp[i][s] = dp[i-1][s - nums[i-1]] + dp[i-1][s + nums[i-1]]
 *   Sums live in [−S, +S] (S = Σnums) → offset by +S to index arrays.
 *   Time  Complexity : O(n·S)   Space Complexity : O(n·S)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Subset-sum transform + 1D knapsack (BEST)
 *   Let P = indices with '+', N = indices with '−'.
 *     P − N = target,  P + N = S  →  P = (S + target) / 2
 *   So: if (S + target) is odd or |target| > S → 0 ways. Otherwise
 *   count the subsets of nums that sum to (S + target)/2 — classic
 *   0/1 knapsack count with ONE array, iterated BACKWARD per item:
 *     dp[s] += dp[s - num]  (s descending)
 *   Time  Complexity : O(n·S)   Space Complexity : O(S)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the knapsack backward loop works
 *   dp[s] must read the PREVIOUS item's dp[s-num]. Iterating s downward
 *   ensures dp[s-num] (a lower index, so visited LATER in this pass) is
 *   still the previous-item value → each item used at most once. The
 *   table DP's second axis (sum) collapses to one array exactly like
 *   the coin-change row compression.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <numeric>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Full 2D DP over (i, offset sum)
 * ===================================================================== */
class Solution_1
{
public:
    /*
     * Purpose : Count sign assignments that sum to `target`.
     * Inputs  : nums — the numbers to sign; target — the desired sum.
     * Output  : number of distinct assignments.
     */
    int findTargetSumWays(const std::vector<int>& nums, int target)
    {
        const int n = static_cast<int>(nums.size());
        const int S = std::accumulate(nums.begin(), nums.end(), 0);
        if (target > S || target < -S)
        {
            return 0; // impossible: even extreme sums cannot reach it
        }
        const int offset = S;            // shift sums into [0, 2S]
        const int width = 2 * S + 1;
        // dp[i][s+offset] : ways to reach sum s with the first i numbers.
        std::vector<std::vector<int>> dp(n + 1, std::vector<int>(width, 0));
        dp[0][offset] = 1;               // sum 0, zero numbers: one way

        for (int i = 1; i <= n; ++i)
        {
            for (int s = -S; s <= S; ++s)
            {
                int ways = 0;
                // Take nums[i-1] with '+': the previous sum was s - num.
                if (s - nums[i - 1] >= -S)
                {
                    ways += dp[i - 1][s - nums[i - 1] + offset];
                }
                // Take it with '−': the previous sum was s + num.
                if (s + nums[i - 1] <= S)
                {
                    ways += dp[i - 1][s + nums[i - 1] + offset];
                }
                dp[i][s + offset] = ways;
            }
        }
        return dp[n][target + offset];
    }
};

/* =====================================================================
 * APPROACH 2 : Subset-sum transform + 1D backward knapsack
 * ===================================================================== */
class Solution_2
{
public:
    /*
     * Purpose : Count sign assignments that sum to `target`.
     * Inputs  : nums — the numbers to sign; target — the desired sum.
     * Output  : number of distinct assignments.
     */
    int findTargetSumWays(const std::vector<int>& nums, int target)
    {
        const int S = std::accumulate(nums.begin(), nums.end(), 0);
        if ((S + target) % 2 != 0 || target > S || target < -S)
        {
            return 0; // parity/range check: P = (S+target)/2 must be integer
        }
        const int P = (S + target) / 2;
        if (P < 0)
        {
            return 0;
        }
        // dp[s] : subsets (of the processed prefix) summing exactly to s.
        std::vector<int> dp(P + 1, 0);
        dp[0] = 1; // empty subset sums to 0
        for (const int num : nums)
        {
            // Descending order = each num used at most once (0/1 knapsack).
            for (int s = P; s >= num; --s)
            {
                dp[s] += dp[s - num];
            }
        }
        return dp[P];
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on the official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        std::vector<int> nums;
        int target;
        int expected;
    };
    const std::vector<Test> tests = {
        {{1, 1, 1, 1, 1}, 3, 5},   // official example 1
        {{1}, 1, 1},               // official example 2
        {{1, 0}, 1, 2},            // zero participates in both signs
        {{1, 2, 3, 4, 5}, 3, 3},   // manual count
        {{7, 9, 3, 8, 0, 2, 4, 8, 3, 9}, 0, 0} // odd S+target parity? S=53,
                                               // target 0 → 53 odd → 0
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().findTargetSumWays(t.nums, t.target);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().findTargetSumWays(t.nums, t.target);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "findTargetSumWays(target=" << t.target << ")  A1=" << r1
                  << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (2D table)    : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (1D knapsack) : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}