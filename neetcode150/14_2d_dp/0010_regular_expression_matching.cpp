/*
 * =====================================================================
 * LeetCode 10 : Regular Expression Matching                         (Hard)
 * https://leetcode.com/problems/regular-expression-matching/
 * Category   : 2D DP
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an input string `s` and a pattern `p`, implement regular
 *   expression matching with two wildcards:
 *     '.'  — matches ANY single character.
 *     '*'  — matches ZERO or MORE of the PRECEDING element.
 *   The match must cover the ENTIRE string (no partial matching).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Each prefix pair (s[0..i), p[0..j)) is a self-contained sub-problem
 *   whose answer only depends on SMALLER prefix pairs → a 2D DP table
 *   where dp[i][j] answers "does s[0..i-1] match p[0..j-1]?".
 *   The '*' rule is the only tricky case: it gives us a CHOICE (use
 *   zero copies, or keep consuming matching characters), which is
 *   exactly an OR over two sub-problems.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bottom-up 2D DP (BEST)
 *   dp[i][j] = does s[0..i-1] match p[0..j-1]?
 *     Base: dp[0][0] = true (empty matches empty).
 *     If p[j-1] != '*':
 *         dp[i][j] = dp[i-1][j-1] AND (s[i-1] == p[j-1] OR p[j-1] == '.')
 *     If p[j-1] == '*':
 *         dp[i][j] = dp[i][j-2]                                   (zero copies)
 *                 OR (dp[i-1][j] AND (s[i-1] == p[j-2] OR p[j-2] == '.'))
 *                                                  (one more copy, pattern
 *                                                   char p[j-2] repeats)
 *   Fill order: rows top→bottom, columns left→right — every cell reads
 *   dp[i-1][*] (previous row) and dp[i][j-2] (earlier in the SAME row).
 *   Time  Complexity : O(|s|·|p|)  — one pass over every cell.
 *   Space Complexity : O(|s|·|p|)  — the full table.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down memoized DFS (same recurrence, recursion-first)
 *   Same dp semantics but computed lazily: solve(i, j) asks the same
 *   question, recurses only on the states it needs, and memoizes.
 *   Avoids computing unreachable states; identical worst-case bounds.
 *   Time  Complexity : O(|s|·|p|)  Space Complexity : O(|s|·|p|)
 * ---------------------------------------------------------------------
 * DEEP DIVE — the '*' recurrence, decoded
 *   p = "c*" against s = "ccca": at dp[4][2] (s="cccc"? no — s[0..3]
 *   = "cccc", p = "c*") the '*' must decide:
 *     • zero copies → dp[4][0] (drop "c*" entirely, keep all of s);
 *     • one more copy → s[3]=='c' == p[0] → dp[3][2] (consume one 'c',
 *       pattern stays "c*" so it may repeat).
 *   The OR is what lets one '*' absorb ANY run length — including zero.
 *   Table shape: (|s|+1) × (|p|+1) so index i/j means "first i / first j
 *   characters consumed" and the empty-string prefixes are representable.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : Bottom-up 2D DP
 * ===================================================================== */
class Solution_1
{
public:
    /*
     * Purpose : Decide whether the entire string `s` matches pattern `p`.
     * Inputs  : s — the subject string; p — the pattern with '.' and '*'.
     * Output  : true iff the full s matches the full p.
     */
    bool isMatch(const std::string& s, const std::string& p)
    {
        const int n = static_cast<int>(s.size());
        const int m = static_cast<int>(p.size());
        // dp[i][j] : do the FIRST i chars of s match the FIRST j of p?
        std::vector<std::vector<bool>> dp(n + 1, std::vector<bool>(m + 1, false));
        dp[0][0] = true; // empty string matches empty pattern

        // Seed row 0: a pattern like "a*b*c*" can match the empty string
        // only when every non-'*' char is "neutralized" by its '*' pair.
        for (int j = 2; j <= m; ++j)
        {
            if (p[j - 1] == '*')
            {
                dp[0][j] = dp[0][j - 2]; // drop "x*" → match nothing
            }
        }

        for (int i = 1; i <= n; ++i)
        {
            for (int j = 1; j <= m; ++j)
            {
                const char pc = p[j - 1];
                if (pc != '*')
                {
                    // Literal or '.': both sides must consume one char.
                    dp[i][j] = dp[i - 1][j - 1]
                            && (s[i - 1] == pc || pc == '.');
                }
                else
                {
                    // '*' = zero copies of p[j-2] (dp[i][j-2]) OR one more
                    // copy (consume s[i-1] when it equals p[j-2]).
                    dp[i][j] = dp[i][j - 2];
                    if (s[i - 1] == p[j - 2] || p[j - 2] == '.')
                    {
                        dp[i][j] = dp[i][j] || dp[i - 1][j];
                    }
                }
            }
        }
        return dp[n][m];
    }
};

/* =====================================================================
 * APPROACH 2 : Top-down memoized DFS (identical recurrence)
 * ===================================================================== */
class Solution_2
{
private:
    std::vector<std::vector<int>> memo_; // -1 unknown, 0 false, 1 true

    /*
     * Purpose : Solve the sub-problem "do s[i..] and p[j..] match?".
     * Inputs  : i — index into s; j — index into p; s, p — the strings.
     * Output  : true iff the suffixes starting at i and j match.
     */
    bool solve(int i, int j, const std::string& s, const std::string& p)
    {
        if (memo_[i][j] != -1)
        {
            return memo_[i][j] == 1; // already answered → reuse (memo hit)
        }
        bool ans = false;
        if (j == static_cast<int>(p.size()))
        {
            ans = (i == static_cast<int>(s.size())); // pattern spent: string must be too
        }
        else
        {
            // Does THIS position match? (literal, or '.' wildcard)
            const bool firstMatch = (i < static_cast<int>(s.size()))
                    && (s[i] == p[j] || p[j] == '.');
            if (j + 1 < static_cast<int>(p.size()) && p[j + 1] == '*')
            {
                // 'x*' ahead → skip it entirely, or consume one matching char
                // and keep the 'x*' so it can repeat.
                ans = solve(i, j + 2, s, p)
                   || (firstMatch && solve(i + 1, j, s, p));
            }
            else
            {
                // No '*' after p[j]: both must consume exactly one char.
                ans = firstMatch && solve(i + 1, j + 1, s, p);
            }
        }
        memo_[i][j] = ans ? 1 : 0;
        return ans;
    }

public:
    /*
     * Purpose : Decide whether `s` fully matches pattern `p` (memo DFS).
     * Inputs  : s — subject string; p — pattern with '.' and '*'.
     * Output  : true iff full match.
     */
    bool isMatch(const std::string& s, const std::string& p)
    {
        // (|s|+1)×(|p|+1) memo grid; +1 rows cover "i past the end".
        memo_.assign(s.size() + 1, std::vector<int>(p.size() + 1, -1));
        return solve(0, 0, s, p);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on LeetCode's official examples
 * ===================================================================== */
int main()
{
    struct Test
    {
        std::string s;
        std::string p;
        bool expected;
    };
    const std::vector<Test> tests = {
        {"aa", "a", false},       // '*' missing → cannot cover "aa"
        {"aa", "a*", true},       // 'a*' absorbs both 'a's
        {"aab", "c*a*b", true},   // "c*" matches zero 'c's
        {"mississippi", "mis*is*p*.", false}, // trailing '*' pair mismatch
        {"ab", ".*", true}        // ".*" = any run of any characters
    };

    long peak1 = 0, peak2 = 0;
    double us1 = 0.0, us2 = 0.0;
    bool pass1 = true, pass2 = true;

    for (const Test& t : tests)
    {
        // --- Approach 1 timing + peak RAM (delta of ru_maxrss) ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const bool r1 = Solution_1().isMatch(t.s, t.p);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        us1 += std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        peak1 += (after1.ru_maxrss - before1.ru_maxrss); // ru_maxrss is already KB
        pass1 = pass1 && (r1 == t.expected);

        // --- Approach 2 ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const bool r2 = Solution_2().isMatch(t.s, t.p);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        us2 += std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        peak2 += (after2.ru_maxrss - before2.ru_maxrss);
        pass2 = pass2 && (r2 == t.expected);

        std::cout << "isMatch(\"" << t.s << "\", \"" << t.p << "\")  A1="
                  << (r1 ? "true" : "false") << "  A2=" << (r2 ? "true" : "false")
                  << "  expected=" << (t.expected ? "true" : "false") << "\n";
    }

    std::cout << "Approach 1 (2D DP)      : " << (pass1 ? "PASS" : "FAIL")
              << "  time = " << us1 << " µs  peak-ram-delta = " << peak1 << " KB\n";
    std::cout << "Approach 2 (memo DFS)   : " << (pass2 ? "PASS" : "FAIL")
              << "  time = " << us2 << " µs  peak-ram-delta = " << peak2 << " KB\n";

    return (pass1 && pass2) ? 0 : 1;
}