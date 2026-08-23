/*
 * =====================================================================
 * LeetCode 91 : Decode Ways                                      (Medium)
 * https://leetcode.com/problems/decode-ways/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A message of digits maps letters as 'A'→1 … 'Z'→26. Given a digit
 *   string `s`, count how many ways it can be decoded back to letters.
 *   Invalid if some digit cannot be consumed (e.g. a lone '0').
 * ---------------------------------------------------------------------
 * INTUITION
 *   Scanning left→right, position i can END a code of length 1 (digit
 *   in 1..9) or length 2 (previous two digits in 10..26). Decodings of
 *   prefix s[0..i) = decodings of the prefix ending one step back +
 *   decodings of the prefix ending two steps back — Fibonacci with
 *   validity gates. Overlapping subproblems: prefix counts are reused
 *   by every longer prefix that ends with the same suffix window.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bottom-up with rolling variables (BEST)
 *   dp[i] = decodings of prefix s[0..i) (i = consumed characters).
 *   Recurrence :
 *       one = dp[i-1] if s[i-1] != '0' else 0      (code '1'..'9')
 *       two = dp[i-2] if 10 <= s[i-2..i-1] <= 26 else 0
 *       dp[i] = one + two
 *   State space : i ∈ [0, n] → n+1 states on array dp[n+1], filled
 *                left→right; dp[i] reads only i-1 and i-2 → collapse
 *                the table into two rolling variables → O(1) space.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down memoized recursion
 *   f(i) = decodings of suffix s[i:]. Two branches: take 1 char (if
 *   in 1..9) or take 2 chars (if in 10..26). memo[i] caches suffixes.
 *   Trade-off : mirrors human backtracking; recursion depth = n, each
 *   call carries stack + memo lookup overhead.
 *   Time  Complexity : O(n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — the gates ARE the optimal substructure
 *   dp[i] = dp[i-1] + dp[i-2] is only valid when each term's ending
 *   code is legal: '0' kills the 1-digit branch, '27'..'99' kills the
 *   2-digit branch. This is Fibonacci with a filter matrix — the same
 *   recurrence pattern as 0070 (unfiltered) and 0198 (max instead of
 *   sum). State-space math: n+1 states, each O(1) to combine → O(n).
 *   The backward-only reads (i-1, i-2) again justify rolling vars:
 *   cell i is independent of cells < i-2, so those can be discarded.
 *   Real life : T9/text messaging digit-to-word mapping, ISBN and
 *   barcode check decoding, prefix-code word segmentation.
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
 * APPROACH 1 : bottom-up with two rolling variables
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Count valid decodings of the digit string `s`.
     * Inputs  : s — digits-only string (may start with '0').
     * Output  : int — number of ways, 0 when undecodable.
     */
    int numDecodings(const std::string& s) {
        const int n = static_cast<int>(s.size());
        // Rolling window: prev2 = dp[i-2], prev1 = dp[i-1].
        int prev2 = 1;  // dp[0] = 1 — the empty prefix decodes one way
        int prev1 = 1;  // dp[1] provisional; overwritten on first loop
        for (int i = 1; i <= n; ++i) {
            int cur = 0;
            // Length-1 code: this digit alone must be '1'..'9'.
            if (s[i - 1] != '0') {
                cur += prev1;  // extend every dp[i-1] decoding by s[i-1]
            }
            // Length-2 code: the previous pair must form 10..26.
            if (i >= 2 && s[i - 2] == '1') {
                cur += prev2;                       // "10".."19"
            } else if (i >= 2 && s[i - 2] == '2' && s[i - 1] <= '6') {
                cur += prev2;                       // "20".."26"
            }
            prev2 = prev1;  // slide the window right
            prev1 = cur;
        }
        return prev1;  // dp[n]
    }
};

/* =====================================================================
 * APPROACH 2 : top-down memoized recursion over suffixes
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Count valid decodings of the digit string `s` (memoized).
     * Inputs  : s — digits-only string.
     * Output  : int — number of ways, 0 when undecodable.
     */
    int numDecodings(const std::string& s) {
        n = static_cast<int>(s.size());
        str = s;
        // memo[i] = -1 → suffix s[i:] not solved yet.
        memo.assign(n + 1, -1);
        return f(0);
    }

private:
    int n;
    std::string str;
    std::vector<int> memo;

    /*
     * Purpose : Recursive suffix solver with caching (top-down DP).
     * Inputs  : i — start index of the remaining suffix.
     * Output  : int — decodings of str[i:].
     */
    int f(int i) {
        if (i == n) {
            return 1;            // consumed everything → exactly one way
        }
        if (str[i] == '0') {
            return 0;            // '0' cannot START a code
        }
        if (memo[i] != -1) {
            return memo[i];      // overlapping subproblem → reuse
        }
        // Branch 1: take one digit (valid: it is 1..9 here).
        int ways = f(i + 1);
        // Branch 2: take two digits if they form 10..26.
        if (i + 1 < n && (str[i] == '1' || (str[i] == '2' && str[i + 1] <= '6'))) {
            ways += f(i + 2);
        }
        return memo[i] = ways;   // cache before returning
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (s, expected ways). Both solutions must match.
    struct Test { std::string s; int expected; };
    const std::vector<Test> tests = {
        {"12",  2},  // "AB"(1,2), "L"(12)
        {"226", 3},  // "BZ"(2,26), "VF"(22,6), "BBF"(2,2,6)
        {"06",  0}   // '0' cannot lead a code → undecodable
    };

    double total_us_1 = 0.0, total_us_2 = 0.0;
    long total_kb_1 = 0, total_kb_2 = 0;
    bool allPass = true;

    for (const Test& t : tests) {
        // --- Approach 1: time via steady_clock, RAM via getrusage ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().numDecodings(t.s);
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
        const int r2 = Solution_2().numDecodings(t.s);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        const double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        const long kb2 = after2.ru_maxrss - before2.ru_maxrss;
        total_us_2 += us2;
        total_kb_2 += kb2;

        const bool ok = (r1 == t.expected) && (r2 == t.expected);
        allPass = allPass && ok;

        std::cout << "s=" << t.s << "  A1=" << r1 << "  A2=" << r2
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