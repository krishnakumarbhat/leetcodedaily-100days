/*
 * =====================================================================
 * LeetCode 115 : Distinct Subsequences                                (Hard)
 * https://leetcode.com/problems/distinct-subsequences/
 * Category   : 2D DP
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two strings s and t, count the number of DISTINCT subsequences
 *   of s that equal t. A subsequence deletes any characters of s while
 *   keeping the relative order of the survivors.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Walk s left→right. For each character we decide: does it take part
 *   in forming t, and if so, which position of t does it fill? The
 *   count of ways to build t[0..j-1] from s[0..i-1] either skips s[i-1]
 *   (count unchanged) or, when the characters match, uses s[i-1] as the
 *   j-th character (then the rest must come from the earlier prefix).
 *   This "skip-or-take" dichotomy is a 2D DP recurrence.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full 2D table (BEST for understanding)
 *   dp[i][j] = number of subsequences of s[0..i-1] equal to t[0..j-1].
 *     Base: dp[0][0] = 1 (empty subsequence of empty string);
 *           dp[i][0] = 1 (empty target: one way — delete everything);
 *           dp[0][j] = 0 for j > 0 (cannot build from nothing).
 *     If s[i-1] == t[j-1]:
 *         dp[i][j] = dp[i-1][j-1] + dp[i-1][j]   (take it + skip it)
 *     Else:
 *         dp[i][j] = dp[i-1][j]                   (only skip it)
 *   Time  Complexity : O(|s|·|t|)   Space Complexity : O(|s|·|t|)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Row-compressed 1D DP (BEST for memory)
 *   dp[j] alone suffices if we iterate j BACKWARD: dp[j-1] is then the
 *   previous row's value (still un-overwritten) — exactly the "take it"
 *   term; dp[j] itself is "skip it".
 *   Time  Complexity : O(|s|·|t|)   Space Complexity : O(|t|)
 * ---------------------------------------------------------------------
 * DEEP DIVE — take-or-skip is a COUNTING recurrence
 *   Counting problems OR the two mutually exclusive options (ADD them);
 *   existence problems OR them (LOGICAL OR). Same table shape, different
 *   operator — that is why dp here grows values instead of flags.
 *   Answer: dp[|s|][|t|].
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
     * Purpose : Count distinct subsequences of `s` equal to `t`.
     * Inputs  : s — the source string; t — the target subsequence.
     * Output  : the number of distinct ways (fits in a 64-bit int here).
     */
    long long numDistinct(const std::string& s, const std::string& t)
    {
        const int n = static_cast<int>(s.size());
        const int m = static_cast<int>(t.size());
        // dp[i][j] : ways to form t[0..j-1] from s[0..i-1].
        std::vector<std::vector<long long>> dp(n + 1, std::vector<long long>(m + 1, 0));

        // Empty target is reachable from ANY prefix (delete everything).
        for (int i = 0; i <= n; ++i)
        {
            dp[i][0] = 1;
        }

        for (int i = 1; i <= n; ++i)
        {
            for (int j = 1; j <= m; ++j)
            {
                // Skipping s[i-1] is ALWAYS legal.
                dp[i][j] = dp[i - 1][j];
                if (s[i - 1] == t[j - 1])
                {
                    // Also legal: match s[i-1] against t[j-1], then count
                    // the ways to build the REST from the earlier prefix.
                    dp[i][j] += dp[i - 1][j - 1];
                }
            }
        }
        return dp[n][m];
    }
};

/* =====================================================================
 * APPROACH 2 : Row-compressed 1D DP (backward inner loop)
 * ===================================================================== */
class Solution_2
{
public:
    /*
     * Purpose : Count distinct subsequences of `s` equal to `t`.
     * Inputs  : s — the source string; t — the target subsequence.
     * Output  : the number of distinct ways (fits in a 64-bit int here).
     */
    long long numDistinct(const std::string& s, const std::string& t)
    {
        const int m = static_cast<int>(t.size());
        // dp[j] : ways for the CURRENT row i. dp[j] before update = row i-1
        // → the "skip" term; dp[j-1] AFTER update = row i's own take-term.
        std::vector<long long> dp(m + 1, 0);
        dp[0] = 1; // dp[i][0] = 1 for every row, kept alive by never touching j=0

        for (int i = 0; i < static_cast<int>(s.size()); ++i)
        {
            // Backward: overwriting high j first keeps dp[j-1] as the OLD
            // row while we still need it for the "take" addition.
            for (int j = m; j >= 1; --j)
            {
                if (s[i] == t[j - 1])
                {
                    dp[j] += dp[j - 1]; // take s[i] → add previous row's ways
                }
                // skip term dp[j] is implicit: it already holds row i-1.
            }
        }
        return dp[m];
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on the official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        std::string s;
        std::string t;
        long long expected;
    };
    const std::vector<Test> tests = {
        {"rabbbit", "rabbit", 3},   // official example 1
        {"babgbag", "bag", 5},      // official example 2
        {"", "", 1},                // empty target from empty source
        {"", "a", 0},               // cannot build from nothing
        {"aaa", "a", 3}             // any of the three 'a's
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const long long r1 = Solution_1().numDistinct(t.s, t.t);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const long long r2 = Solution_2().numDistinct(t.s, t.t);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "numDistinct(\"" << t.s << "\", \"" << t.t << "\")  A1=" << r1
                  << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (2D table)   : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (1D row)     : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}