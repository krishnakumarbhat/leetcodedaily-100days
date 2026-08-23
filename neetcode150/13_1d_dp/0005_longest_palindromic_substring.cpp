/*
 * =====================================================================
 * LeetCode 5 : Longest Palindromic Substring                     (Medium)
 * https://leetcode.com/problems/longest-palindromic-substring/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a string `s`, return the LONGEST substring that reads the
 *   same forwards and backwards (a palindrome). If several answers
 *   tie, return any one of them.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A palindrome is symmetric around a CENTER. Every palindrome has a
 *   unique center — one character for odd length, the gap between two
 *   characters for even length. So instead of testing all O(n²)
 *   substrings, grow outwards from all 2n-1 centers and stop at the
 *   first mismatch.
 *   DP alternative: s[i..j] is a palindrome ⇔ s[i] == s[j] AND the
 *   inner substring s[i+1..j-1] is a palindrome → optimal substructure
 *   with overlapping subproblems (the classic DP fingerprint).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Expand around centers (BEST)
 *   For every center c in [0, 2n): start l = c/2, r = (c+1)/2 and push
 *   both pointers outward while s[l] == s[r]. Keep the widest window.
 *   Time  Complexity : O(n²) — 2n-1 centers, each expands ≤ n times.
 *   Space Complexity : O(1) — only index variables.
 * ---------------------------------------------------------------------
 * APPROACH 2 — DP boolean table
 *   dp[i][j] = "s[i..j] is a palindrome".
 *   Recurrence : dp[i][j] = (s[i] == s[j]) && (j - i <= 2 || dp[i+1][j-1])
 *   State space : (i, j) with i <= j → n(n+1)/2 ≈ O(n²) states, mapped
 *                onto an n×n table. Fill by increasing LENGTH so the
 *                inner cell dp[i+1][j-1] is already computed when read.
 *   Space optimization : row i only reads row i+1 → ONE rolling row of
 *                booleans collapses the table to O(n) space.
 *   Time  Complexity : O(n²)   Space Complexity : O(n²) → O(n) rolling
 * ---------------------------------------------------------------------
 * DEEP DIVE — recurrence → array mapping, and why both are O(n²)
 *   Both approaches must read O(n²) substrings to PROVE maximality:
 *   the answer must be compared against every smaller candidate.
 *   The DP recurrence maps 1:1 onto the table: cell (i, j) reads the
 *   diagonal neighbour (i+1, j-1) — a strictly SMALLER window already
 *   solved in the previous length iteration. Overlapping subproblems
 *   are exactly the palindromes shared by many windows; each is stored
 *   once in dp, never recomputed. Center expansion avoids the table
 *   entirely because each palindrome is found at its OWN center — the
 *   table's cells for non-matching pairs never need to exist.
 *   Real life : DNA/RNA palindromic motifs (regulatory regions),
 *   text mirror detection, string-toolbox primitives.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : expand around every center
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the longest palindromic substring of `s`.
     * Inputs  : s — the string to search inside.
     * Output  : std::string — widest palindrome window (any tie).
     */
    std::string longestPalindrome(const std::string& s) {
        const int n = static_cast<int>(s.size());
        // bestL/bestR = inclusive window of the widest palindrome found.
        int bestL = 0, bestR = 0;

        // 2n-1 centers: even c → single char, odd c → gap between chars.
        for (int c = 0; c < 2 * n - 1; ++c) {
            // c=0 → (0,0); c=1 → (0,1); c=2 → (1,1); c=3 → (1,2); ...
            int l = c / 2;
            int r = (c + 1) / 2;
            // Expand while the mirrored characters still match.
            while (l >= 0 && r < n && s[l] == s[r]) {
                if (r - l > bestR - bestL) {  // strictly wider → new best
                    bestL = l;
                    bestR = r;
                }
                --l;  // reach one char further left
                ++r;  // ...and one char further right
            }
        }
        return s.substr(bestL, bestR - bestL + 1);
    }
};

/* =====================================================================
 * APPROACH 2 : DP boolean table, filled by increasing length
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the longest palindromic substring of `s`.
     * Inputs  : s — the string to search inside.
     * Output  : std::string — widest palindrome window (any tie).
     */
    std::string longestPalindrome(const std::string& s) {
        const int n = static_cast<int>(s.size());
        if (n == 0) {
            return "";  // empty string edge case
        }
        // dp[i][j] = true ⇔ s[i..j] is a palindrome (default false).
        std::vector<std::vector<bool>> dp(n, std::vector<bool>(n, false));
        int bestL = 0, bestR = 0;

        // Fill by LENGTH so dp[i+1][j-1] (length len-2) exists already.
        for (int len = 1; len <= n; ++len) {
            for (int i = 0; i + len - 1 < n; ++i) {
                const int j = i + len - 1;
                // The recurrence: matching ends AND a valid inner window
                // (length 1 or 2 needs no inner window at all).
                if (s[i] == s[j] && (len <= 2 || dp[i + 1][j - 1])) {
                    dp[i][j] = true;
                    if (len > bestR - bestL + 1) {  // new global best
                        bestL = i;
                        bestR = j;
                    }
                }
            }
        }
        return s.substr(bestL, bestR - bestL + 1);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (input, expected). Both solutions must match.
    struct Test { std::string s; std::string expected; };
    const std::vector<Test> tests = {
        {"babad", "bab"},   // "aba" is also valid — check length only
        {"cbbd",  "bb" },
        {"a",     "a"  }
    };

    // Rolling accumulators for the two approaches.
    double total_us_1 = 0.0, total_us_2 = 0.0;
    long total_kb_1 = 0, total_kb_2 = 0;
    bool allPass = true;

    for (const Test& t : tests) {
        // --- Approach 1: time via steady_clock, RAM via getrusage ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const std::string r1 = Solution_1().longestPalindrome(t.s);
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
        const std::string r2 = Solution_2().longestPalindrome(t.s);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        const double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        const long kb2 = after2.ru_maxrss - before2.ru_maxrss;
        total_us_2 += us2;
        total_kb_2 += kb2;

        // Acceptance: result is a palindrome of the SAME length as the
        // expected answer (ties are allowed, so exact match is not required).
        const auto isPal = [](const std::string& x) {
            for (std::size_t i = 0; i < x.size() / 2; ++i) {
                if (x[i] != x[x.size() - 1 - i]) return false;
            }
            return true;
        };
        const bool ok = isPal(r1) && isPal(r2) &&
                        r1.size() == t.expected.size() &&
                        r2.size() == t.expected.size();
        allPass = allPass && ok;

        std::cout << "s=" << t.s << "  A1=\"" << r1 << "\"  A2=\"" << r2
                  << "\"  expected-len=" << t.expected.size()
                  << (ok ? "  PASS" : "  FAIL")
                  << "  A1 " << us1 << "µs/" << kb1 << "KB  A2 " << us2
                  << "µs/" << kb2 << "KB\n";
    }

    std::cout << "Totals: A1 " << total_us_1 << "µs/" << total_kb_1
              << "KB | A2 " << total_us_2 << "µs/" << total_kb_2 << "KB\n";
    std::cout << (allPass
                  ? "PASS : both approaches return valid maximal palindromes."
                  : "FAIL : at least one answer is wrong.")
              << "\n";
    return allPass ? 0 : 1;
}