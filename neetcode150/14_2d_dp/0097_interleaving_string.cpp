/*
 * =====================================================================
 * LeetCode 97 : Interleaving String                                 (Medium)
 * https://leetcode.com/problems/interleaving-string/
 * Category   : 2D DP
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given strings s1, s2 and s3, decide whether s3 can be formed by
 *   INTERLEAVING s1 and s2 — merging their characters while keeping
 *   the RELATIVE ORDER inside each string intact.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Any prefix of s3 of length i+j is built from i chars of s1 and j
 *   chars of s2. That prefix is valid iff its LAST character came from
 *   s1 (and the preceding prefix was valid) OR from s2 (same idea) →
 *   boolean 2D DP over the "amount consumed from each string".
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full 2D table (BEST for understanding)
 *   dp[i][j] = can s3[0..i+j-1] be an interleaving of s1[0..i-1] and
 *              s2[0..j-1]?
 *     Base: dp[0][0] = true (empty + empty = empty).
 *           dp[i][0] = dp[i-1][0] && s1[i-1]==s3[i-1]  (s2 unused)
 *           dp[0][j] = dp[0][j-1] && s2[j-1]==s3[j-1]  (s1 unused)
 *     dp[i][j] = (dp[i-1][j] && s1[i-1] == s3[i+j-1])
 *              || (dp[i][j-1] && s2[j-1] == s3[i+j-1])
 *   Time  Complexity : O(m·n)   Space Complexity : O(m·n)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Row-compressed 1D DP (BEST for memory)
 *   Row i reads ONLY the previous row (dp[j]) and the same row
 *   (dp[j-1]) → one boolean vector suffices.
 *   Time  Complexity : O(m·n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why this is NOT a substring/order-free problem
 *   Interleaving preserves per-string order, so the "choice" of which
 *   string feeds the next char is local (last char of s3). That local
 *   choice maps to the OR above. The total length check
 *   (|s1|+|s2| == |s3|) is a cheap necessary condition we test FIRST.
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
     * Purpose : Decide whether s3 is an interleaving of s1 and s2.
     * Inputs  : s1, s2, s3 — the three strings to check.
     * Output  : true iff s3 can be formed by interleaving s1 and s2.
     */
    bool isInterleave(const std::string& s1, const std::string& s2, const std::string& s3)
    {
        const int m = static_cast<int>(s1.size());
        const int n = static_cast<int>(s2.size());
        if (m + n != static_cast<int>(s3.size()))
        {
            return false; // length mismatch → impossible, O(1) exit
        }

        // dp[i][j] : can the first i+j chars of s3 interleave s1[0..i-1]
        //            and s2[0..j-1]?
        std::vector<std::vector<bool>> dp(m + 1, std::vector<bool>(n + 1, false));
        dp[0][0] = true;

        // First row: only s1 is consumed.
        for (int i = 1; i <= m; ++i)
        {
            dp[i][0] = dp[i - 1][0] && (s1[i - 1] == s3[i - 1]);
        }
        // First column: only s2 is consumed.
        for (int j = 1; j <= n; ++j)
        {
            dp[0][j] = dp[0][j - 1] && (s2[j - 1] == s3[j - 1]);
        }

        for (int i = 1; i <= m; ++i)
        {
            for (int j = 1; j <= n; ++j)
            {
                // s3[i+j-1] must be the next char of EITHER string.
                dp[i][j] = (dp[i - 1][j] && s1[i - 1] == s3[i + j - 1])
                        || (dp[i][j - 1] && s2[j - 1] == s3[i + j - 1]);
            }
        }
        return dp[m][n];
    }
};

/* =====================================================================
 * APPROACH 2 : Row-compressed 1D DP
 * ===================================================================== */
class Solution_2
{
public:
    /*
     * Purpose : Decide whether s3 is an interleaving of s1 and s2.
     * Inputs  : s1, s2, s3 — the three strings to check.
     * Output  : true iff s3 can be formed by interleaving s1 and s2.
     */
    bool isInterleave(const std::string& s1, const std::string& s2, const std::string& s3)
    {
        const int m = static_cast<int>(s1.size());
        const int n = static_cast<int>(s2.size());
        if (m + n != static_cast<int>(s3.size()))
        {
            return false;
        }

        // dp[j] : current row i; dp[j-1] (same row, left) and the OLD
        // dp[j] (row i-1) reproduce both OR branches of the recurrence.
        std::vector<bool> dp(n + 1, false);
        dp[0] = true;

        // Row 0: only s2 consumed.
        for (int j = 1; j <= n; ++j)
        {
            dp[j] = dp[j - 1] && (s2[j - 1] == s3[j - 1]);
        }

        for (int i = 1; i <= m; ++i)
        {
            // Column 0 of this row: only s1 consumed so far.
            dp[0] = dp[0] && (s1[i - 1] == s3[i - 1]);
            for (int j = 1; j <= n; ++j)
            {
                // `dp[j]` here is STILL row i-1 → the s1 branch;
                // `dp[j-1]` was just overwritten with row i → the s2 branch.
                dp[j] = (dp[j] && s1[i - 1] == s3[i + j - 1])
                     || (dp[j - 1] && s2[j - 1] == s3[i + j - 1]);
            }
        }
        return dp[n];
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on the official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        std::string s1;
        std::string s2;
        std::string s3;
        bool expected;
    };
    const std::vector<Test> tests = {
        {"aabcc", "dbbca", "aadbbcbcac", true},   // official example 1
        {"aabcc", "dbbca", "aadbbbaccc", false},  // official example 2
        {"", "", "", true},                       // all empty
        {"ab", "cd", "acbd", true},               // perfect alternation
        {"ab", "cd", "abcdx", false}              // length mismatch
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const bool r1 = Solution_1().isInterleave(t.s1, t.s2, t.s3);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const bool r2 = Solution_2().isInterleave(t.s1, t.s2, t.s3);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "isInterleave(\"" << t.s1 << "\", \"" << t.s2 << "\", \""
                  << t.s3 << "\")  A1=" << (r1 ? "true" : "false")
                  << "  A2=" << (r2 ? "true" : "false")
                  << "  expected=" << (t.expected ? "true" : "false") << "\n";
    }

    std::cout << "Approach 1 (2D table)   : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (1D row)     : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}