/*
 * =====================================================================
 * LeetCode 1143 : Longest Common Subsequence                      (Medium)
 * https://leetcode.com/problems/longest-common-subsequence/
 * Category   : 1-D dynamic programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Longest subsequence common to two strings (subsequence = delete
 *   any chars, keep order). Return its length.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Classic 2-sequence DP: dp[i][j] = LCS of prefixes text1[0..i),
 *   text2[0..j). Match → +1 along the diagonal; mismatch → take the
 *   max of dropping either tail. The table only needs the previous
 *   row, so memory collapses to O(min(m, n)).
 * ---------------------------------------------------------------------
 * APPROACH 1 · O(m·n) table (best)
 *   1. dp[i][j] = dp[i-1][j-1]+1 if chars equal (use the diagonal).
 *   2. Else max(dp[i-1][j], dp[i][j-1]).
 * APPROACH 2 · Rolling two rows (memory-optimized)
 *   Keep prev[] and cur[]; same recurrences, O(n) memory.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why the recurrence is "longest path in a grid"
 *   Think of matching as walking a grid: (i,j) is the state; equal
 *   chars are a diagonal step worth +1, unequal chars move you right
 *   or down for free. dp then is exactly the longest-path value, and
 *   the optimal substructure (prefix of an optimal solution is
 *   optimal) holds — the foundation of the recurrence. With both
 *   strings 1000 chars, the O(n²) memory table is 1M ints ≈ 8 MB;
 *   the rolling row drops that to 8 KB.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(m·n).
 * MEMORY COMPLEXITY: O(m·n) or O(n) rolling.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int longestCommonSubsequence(std::string text1, std::string text2) {
        int m = static_cast<int>(text1.size());
        int n = static_cast<int>(text2.size());
        std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
        for (int i = 1; i <= m; ++i)
            for (int j = 1; j <= n; ++j)
                dp[i][j] = (text1[i - 1] == text2[j - 1])
                               ? dp[i - 1][j - 1] + 1
                               : std::max(dp[i - 1][j], dp[i][j - 1]);
        return dp[m][n];
    }
};

class Solution_2 {
public:
    int longestCommonSubsequence(std::string text1, std::string text2) {
        int m = static_cast<int>(text1.size());
        int n = static_cast<int>(text2.size());
        std::vector<int> prev(n + 1, 0), cur(n + 1, 0);
        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j)
                cur[j] = (text1[i - 1] == text2[j - 1])
                             ? prev[j - 1] + 1
                             : std::max(prev[j], cur[j - 1]);
            std::swap(prev, cur);
        }
        return prev[n];
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::string a, b; int want; };
    const Case cases[] = {
        {"abcde", "ace", 3},
        {"abc", "abc", 3},
        {"abc", "def", 0},
        {"bsbininm", "jmjkbkjkv", 1}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        int r1 = Solution_1().longestCommonSubsequence(c.a, c.b);
        int r2 = Solution_2().longestCommonSubsequence(c.a, c.b);
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "\"" << c.a << "\" × \"" << c.b << "\" → A1=" << r1
                  << " A2=" << r2 << " (want " << c.want << ") "
                  << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
