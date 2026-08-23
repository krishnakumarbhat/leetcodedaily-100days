/*
 * =====================================================================
 * LeetCode 312 : Burst Balloons                                       (Hard)
 * https://leetcode.com/problems/burst-balloons/
 * Category   : 2D DP (interval DP)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array nums of balloons (each with a value), you burst them
 *   one at a time. Bursting balloon i with live neighbours l and r
 *   earns nums[l] · nums[i] · nums[r]. Max total coins. (Padding: out-
 *   of-range neighbours count as 1.)
 * ---------------------------------------------------------------------
 * INTUITION
 *   The first balloon you burst has TWO arbitrary live neighbours, but
 *   the LAST balloon you burst in any interval has the FIXED boundary
 *   balloons as neighbours — so it is easier to think "which balloon do
 *   I burst LAST inside (l, r)?" Once it is chosen, the two sides never
 *   interact again → interval DP with independent sub-intervals.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bottom-up interval DP (BEST)
 *   Pad: nums' = [1] + nums + [1], size n+2. State is an interval
 *   (l, r) EXCLUSIVE of the boundary balloons l and r:
 *   dp[l][r] = max coins from bursting all balloons strictly inside (l, r)
 *     Base: dp[l][l+1] = 0 (no balloon inside).
 *     dp[l][r] = max over k in (l, r) of:
 *         dp[l][k] + dp[k][r] + nums'[l]·nums'[k]·nums'[r]
 *   Fill order by GAP (r - l) = 2, 3, ..., n+1: a gap-g interval only
 *   depends on smaller gaps, so every dependency is already computed.
 *   Time  Complexity : O(n³)   Space Complexity : O(n²)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down memoized recursion (same recurrence)
 *   solve(l, r) computes the same interval value lazily; recursion
 *   mirrors the sub-interval structure without ordering bookkeeping.
 *   Time  Complexity : O(n³)   Space Complexity : O(n²)
 * ---------------------------------------------------------------------
 * DEEP DIVE — gap-length ordering is the entire trick
 *   dp[l][r] reads dp[l][k] and dp[k][r], whose gaps (k-l) and (r-k)
 *   are STRICTLY smaller than (r-l). Iterating gap 2 → n+1 guarantees
 *   both are ready. The answer is dp[0][n+1] — the full interval with
 *   the two virtual "1" boundaries.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Bottom-up interval DP, gap-length ordering
 * ===================================================================== */
class Solution_1
{
public:
    /*
     * Purpose : Compute the maximum coins obtainable by bursting balloons.
     * Inputs  : nums — balloon values.
     * Output  : maximum total coins.
     */
    int maxCoins(const std::vector<int>& nums)
    {
        const int n = static_cast<int>(nums.size());
        // Pad both ends with virtual "1" balloons so the boundary product
        // formula never needs bounds checks.
        std::vector<int> a(n + 2, 1);
        for (int i = 0; i < n; ++i)
        {
            a[i + 1] = nums[i];
        }
        // dp[l][r] : max coins bursting everything strictly between l and r.
        std::vector<std::vector<int>> dp(n + 2, std::vector<int>(n + 2, 0));

        // gap = r - l: grow the interval from 2 (one balloon inside)
        // up to n+1 (everything inside, boundaries at the two virtual 1s).
        for (int gap = 2; gap <= n + 1; ++gap)
        {
            for (int l = 0; l + gap <= n + 1; ++l)
            {
                const int r = l + gap;
                // Choose the LAST balloon k to burst in (l, r): its
                // neighbours are exactly the boundaries l and r, and the
                // two sides become independent sub-intervals.
                for (int k = l + 1; k < r; ++k)
                {
                    dp[l][r] = std::max(dp[l][r],
                        dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]);
                }
            }
        }
        return dp[0][n + 1];
    }
};

/* =====================================================================
 * APPROACH 2 : Top-down memoized recursion
 * ===================================================================== */
class Solution_2
{
private:
    std::vector<std::vector<int>> memo_;
    std::vector<int> a_;

    /*
     * Purpose : Solve the interval (l, r) recursively (l, r exclusive).
     * Inputs  : l, r — interval boundaries in the padded array.
     * Output  : max coins from bursting everything strictly inside (l, r).
     */
    int solve(int l, int r)
    {
        if (r - l <= 1)
        {
            return 0; // nothing to burst inside
        }
        if (memo_[l][r] != -1)
        {
            return memo_[l][r]; // memoized interval → reuse
        }
        int best = 0;
        for (int k = l + 1; k < r; ++k)
        {
            // Last-burst balloon k: independent left/right intervals plus
            // the coin burst of k between the fixed boundaries l and r.
            best = std::max(best, solve(l, k) + solve(k, r) + a_[l] * a_[k] * a_[r]);
        }
        memo_[l][r] = best;
        return best;
    }

public:
    /*
     * Purpose : Compute the maximum coins (top-down interval DP).
     * Inputs  : nums — balloon values.
     * Output  : maximum total coins.
     */
    int maxCoins(const std::vector<int>& nums)
    {
        const int n = static_cast<int>(nums.size());
        a_.assign(n + 2, 1);
        for (int i = 0; i < n; ++i)
        {
            a_[i + 1] = nums[i];
        }
        memo_.assign(n + 2, std::vector<int>(n + 2, -1));
        return solve(0, n + 1);
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
        int expected;
    };
    const std::vector<Test> tests = {
        {{3, 1, 5, 8}, 167},  // official example 1
        {{1, 5}, 10},         // official example 2
        {{1}, 1},             // single balloon: 1·1·1
        {{1, 2, 3}, 12},      // burst 2 first (6) then 1 (3) then 3 (3)
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().maxCoins(t.nums);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().maxCoins(t.nums);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "maxCoins([";
        for (size_t i = 0; i < t.nums.size(); ++i)
        {
            std::cout << t.nums[i] << (i + 1 < t.nums.size() ? "," : "");
        }
        std::cout << "])  A1=" << r1 << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (interval DP) : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (memo DFS)    : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}