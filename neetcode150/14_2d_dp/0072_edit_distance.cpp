/*
 * =====================================================================
 * LeetCode 72 : Edit Distance                                        (Medium)
 * https://leetcode.com/problems/edit-distance/
 * Category   : 2D DP
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two strings word1 and word2, return the MINIMUM number of
 *   operations to convert word1 into word2. Allowed operations (each
 *   costs 1): INSERT a character, DELETE a character, REPLACE a char.
 * ---------------------------------------------------------------------
 * INTUITION
 *   To convert word1[0..i) into word2[0..j) we look at the LAST
 *   characters. If they already match → ignore both, no cost. If they
 *   differ → the cheapest of three finishing moves:
 *     delete word1's last char, insert word2's last char, or replace.
 *   Each choice reduces to a SMALLER prefix pair → 2D DP table.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Full 2D table (BEST for understanding)
 *   dp[i][j] = minimum edit distance between word1[0..i-1] and
 *              word2[0..j-1] (first i / first j characters).
 *     Base: dp[i][0] = i  — delete i chars; dp[0][j] = j — insert j.
 *     If word1[i-1] == word2[j-1]:
 *         dp[i][j] = dp[i-1][j-1]                  (no new operation)
 *     Else:
 *         dp[i][j] = 1 + min(
 *             dp[i-1][j],      delete word1[i-1]
 *             dp[i][j-1],      insert word2[j-1]
 *             dp[i-1][j-1])    replace word1[i-1] with word2[j-1]
 *   Time  Complexity : O(m·n)   Space Complexity : O(m·n)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Row-compressed 1D DP (BEST for memory)
 *   Each cell needs the previous row AND the diagonal above-left.
 *   Trick: keep ONE array; before overwriting dp[j] we save its old
 *   value as `diag` so the (i-1, j-1) state survives the update.
 *   Time  Complexity : O(m·n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why delete/insert/replace is COMPLETE
 *   Any edit script can be reordered so its LAST operation is one of
 *   the three above — so the min over them is exact, never approximate.
 *   The "match" case cannot be beaten by deleting+reinserting the pair
 *   (that would cost 2), so we take dp[i-1][j-1] directly.
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
     * Purpose : Compute the minimum edit distance between two strings.
     * Inputs  : word1, word2 — the strings to align.
     * Output  : minimum number of insert/delete/replace operations.
     */
    int minDistance(const std::string& word1, const std::string& word2)
    {
        const int m = static_cast<int>(word1.size());
        const int n = static_cast<int>(word2.size());
        // dp[i][j] : edit distance of the prefixes word1[0..i-1], word2[0..j-1].
        std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));

        // Base cases: converting to/from the empty string.
        for (int i = 0; i <= m; ++i)
        {
            dp[i][0] = i; // delete everything
        }
        for (int j = 0; j <= n; ++j)
        {
            dp[0][j] = j; // insert everything
        }

        for (int i = 1; i <= m; ++i)
        {
            for (int j = 1; j <= n; ++j)
            {
                if (word1[i - 1] == word2[j - 1])
                {
                    // Matching last chars → align them for free.
                    dp[i][j] = dp[i - 1][j - 1];
                }
                else
                {
                    // Cheapest finishing move + the operation itself.
                    const int best = std::min(std::min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]);
                    dp[i][j] = 1 + best;
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
     * Purpose : Compute the minimum edit distance between two strings.
     * Inputs  : word1, word2 — the strings to align.
     * Output  : minimum number of insert/delete/replace operations.
     */
    int minDistance(const std::string& word1, const std::string& word2)
    {
        const int m = static_cast<int>(word1.size());
        const int n = static_cast<int>(word2.size());
        // dp[j] : edit distance of current row i against word2[0..j-1].
        std::vector<int> dp(n + 1, 0);
        for (int j = 0; j <= n; ++j)
        {
            dp[j] = j; // row 0 = insert j characters
        }

        for (int i = 1; i <= m; ++i)
        {
            int diag = dp[0]; // dp[i-1][j-1] for j=0 is dp[i-1][0]
            dp[0] = i;        // first column: delete i characters
            for (int j = 1; j <= n; ++j)
            {
                // Save the OLD dp[j] (row i-1) BEFORE overwriting: it is
                // the "delete" option for the NEXT column's diagonal.
                const int up = dp[j];
                if (word1[i - 1] == word2[j - 1])
                {
                    dp[j] = diag; // free diagonal alignment
                }
                else
                {
                    dp[j] = 1 + std::min(std::min(up, dp[j - 1]), diag);
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
        std::string word1;
        std::string word2;
        int expected;
    };
    const std::vector<Test> tests = {
        {"horse", "ros", 3},        // official example 1
        {"intention", "execution", 5}, // official example 2
        {"", "", 0},                // both empty → no ops
        {"a", "b", 1},              // single replace
        {"abcdef", "azced", 3}      // classic textbook case
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().minDistance(t.word1, t.word2);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss);
        pass1 = pass1 && (r1 == t.expected);

        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().minDistance(t.word1, t.word2);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "minDistance(\"" << t.word1 << "\", \"" << t.word2 << "\")  A1=" << r1
                  << "  A2=" << r2 << "  expected=" << t.expected << "\n";
    }

    std::cout << "Approach 1 (2D table)   : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (1D row)     : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}