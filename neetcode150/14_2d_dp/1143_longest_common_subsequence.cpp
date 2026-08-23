/*
 * =====================================================================
 * LeetCode 1143 : Longest Common Subsequence                          (Medium)
 * https://leetcode.com/problems/longest-common-subsequence/
 * Category   : 2D DP
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two strings text1 and text2, return the length of their
 *   LONGEST COMMON SUBSEQUENCE: the longest string obtainable from
 *   both by deleting characters (relative order preserved).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Compare the LAST characters. If they match they must belong to any
 *   optimal common subsequence together (greedy-safe for LCS) → shrink
 *   both strings. If they differ, at least one of them is useless for
 *   the optimal solution → drop one side, take the max. This binary
 *   decision over prefix pairs is exactly a 2D DP recurrence.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full 2D table (BEST for understanding)
 *   dp[i][j] = length of LCS of text1[0..i-1] and text2[0..j-1].
 *     Base: dp[*][0] = dp[0][*] = 0 (empty string has no common chars).
 *     If text1[i-1] == text2[j-1]:
 *         dp[i][j] = dp[i-1][j-1] + 1            (extend the LCS)
 *     Else:
 *         dp[i][j] = max(dp[i-1][j], dp[i][j-1]) (drop one last char)
 *   Fill order: row-major — both dependencies are strictly earlier.
 *   Time  Complexity : O(m·n)   Space Complexity : O(m·n)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Row-compressed 1D DP (BEST for memory)
 *   dp[j] (row i-1) and dp[j-1] (row i) supply both recurrence terms;
 *   the diagonal dp[i-1][j-1] is preserved in a `diag` variable before
 *   dp[j] is overwritten.
 *   Time  Complexity : O(m·n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — the match case is NOT a choice
 *   If text1[i-1] == text2[j-1], an optimal LCS always contains both
 *   characters: pairing them never hurts (any solution dropping one of
 *   them could re-append the pair). So we take dp[i-1][j-1]+1 directly
 *   instead of max()ing — the +1 is the new pair, guaranteed valid.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Full 2D DP table
 * ===================================================================== */
class Solution_1
{
public:
    /*
     * Purpose : Compute the length of the longest common subsequence.
     * Inputs  : text1, text2 — the two strings to compare.
     * Output  : LCS length.
     */
    int longestCommonSubsequence(const std::string& text1, const std::string& text2)
    {
        const int m = static_cast<int>(text1.size());
        const int n = static_cast<int>(text2.size());
        // dp[i][j] : LCS of text1[0..i-1] and text2[0..j-1].
        std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));

        for (int i = 1; i <= m; ++i)
        {
            for (int j = 1; j <= n; ++j)
            {
                if (text1[i - 1] == text2[j - 1])
                {
                    // Last chars match → they extend the LCS of the
                    // prefixes. +1 and the diagonal state.
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                }
                else
                {
                    // Mismatch → at least one last char is not in the LCS:
                    // keep the better of the two trimmed options.
                    dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[m][n];
    }
};

/* =====================================================================
 * APPROACH 2 : Row-compressed 1D DP with diagonal save
 * ===================================================================== */
class Solution_2
{
public:
    /*
     * Purpose : Compute the length of the longest common subsequence.
     * Inputs  : text1, text2 — the two strings to compare.
     * Output  : LCS length.
     */
    int longestCommonSubsequence(const std::string& text1, const std::string& text2)
    {
        const int n = static_cast<int>(text2.size());
        // dp[j] : LCS of the current row i against text2[0..j-1].
        std::vector<int> dp(n + 1, 0);

        for (int i = 0; i < static_cast<int>(text1.size()); ++i)
        {
            int diag = 0; // dp[i-1][j-1] for j=1 is dp[i-1][0] = 0
            for (int j = 1; j <= n; ++j)
            {
                // Save the OLD dp[j] (row i-1) BEFORE overwrite: it is
                // the "drop text1's char" option for the next iteration.
                const int up = dp[j];
                if (text1[i] == text2[j - 1])
                {
                    dp[j] = diag + 1; // extend via the preserved diagonal
                }
                else
                {
                    // max(drop text1's char = up, drop text2's = dp[j-1]).
                    dp[j] = std::max(up, dp[j - 1]);
                }
                diag = up; // advance the diagonal to (i-1, j)
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
        std::string text1;
        std::string text2;
        int expected;
    };
    const std::vector<Test> tests = {
        {"abcde", "ace", 3},       // official example 1
        {"abc", "abc", 3},         // official example 2
        {"abc", "def", 0},         // official example 3
        {"", "xyz", 0},            // empty side → 0
        {"bsbininm", "jmjkbkjkv", 1} // only 'j' (or 'b'?) common — verify:
                                     // chars in both: 'b','m'? → LCS = 1
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().longestCommonSubsequence(t.text1, t.text2);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().longestCommonSubsequence(t.text1, t.text2);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "LCS(\"" << t.text1 << "\", \"" << t.text2 << "\")  A1=" << r1
                  << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (2D table)    : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (1D row)      : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}