/*
 * =====================================================================
 * LeetCode 338 : Counting Bits                                      (Easy)
 * https://leetcode.com/problems/counting-bits/
 * Category   : Bit Manipulation
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer n, return an array `ans` of length n + 1 such
 *   that ans[i] is the NUMBER OF 1 BITS in the binary representation
 *   of i, for every 0 ≤ i ≤ n. Example: n = 5 → [0,1,1,2,1,2].
 * ---------------------------------------------------------------------
 * INTUITION
 *   Computing popcount(i) from scratch for EVERY i costs O(n log n) —
 *   but the popcount of i is ALREADY computable from a SMALLER
 *   number's popcount. Right-shifting i by 1 (i >> 1) drops the
 *   lowest bit, so:
 *       popcount(i) = popcount(i >> 1) + (lowest bit of i)
 *   i >> 1 < i, so every popcount is known by the time we need it —
 *   a textbook DP recurrence with no decisions, just a carry.
 * ---------------------------------------------------------------------
 * APPROACH 1 — DP via right shift (BEST)
 *   dp[i] = dp[i >> 1] + (i & 1). One O(1) step per i, O(n) total.
 *   Time  Complexity : O(n)   Space Complexity : O(n).
 * ---------------------------------------------------------------------
 * APPROACH 2 — DP via last-set-bit clearing
 *   dp[i] = dp[i & (i - 1)] + 1. `i & (i-1)` removes the LOWEST set
 *   bit (the 0191 identity), leaving a smaller number that carries
 *   exactly one fewer set bit. Same O(n) total, same result —
 *   different identity, and it skips one bit-op per step on average.
 *   Time  Complexity : O(n)   Space Complexity : O(n).
 * ---------------------------------------------------------------------
 * DEEP DIVE — why dp[i] = dp[i >> 1] + (i & 1) is correct
 *   Splitting a number at the bit boundary: i = (i >> 1) << 1 | (i & 1).
 *   The set bits of i = the set bits of (i >> 1) — those are i's bits
 *   shifted down one position, count preserved — PLUS the lowest bit
 *   (i & 1), which the shift dropped. Since i >> 1 is strictly smaller
 *   than i for i > 0, induction on i gives every value in O(1).
 *   For i = 13 = 1101₂: dp[13] = dp[6] + 1 = dp[3] + 0 + 1 = 3. ✓
 * =====================================================================
 */

#include <iostream>      // std::cout — printing benchmark results
#include <vector>        // std::vector — the output dp array
#include <cstdint>       // std::int32_t — element type of the dp table
#include <climits>       // INT_MAX — scale check for the test table
#include <chrono>        // std::chrono::steady_clock — timing for benchmark
#include <sys/resource.h>// getrusage — peak RAM measurement for benchmark

/* =====================================================================
 * APPROACH 1 : DP via right shift — dp[i] = dp[i >> 1] + (i & 1)
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Popcount of every integer 0..n, via the right-shift
     *           DP recurrence.
     * Inputs  : n — the upper bound of the range to fill.
     * Output  : std::vector<int> — ans[i] = popcount(i).
     */
    std::vector<int> countBits(int n) {
        // dp table: one slot per value; dp[0] = 0 by construction.
        std::vector<int> dp(n + 1, 0);

        // i >> 1 is always smaller than i, so dp[i >> 1] is already
        // final when we read it — the dependency is acyclic.
        for (int i = 1; i <= n; ++i) {
            dp[i] = dp[i >> 1] + (i & 1);
        }
        return dp;
    }
};

/* =====================================================================
 * APPROACH 2 : DP via last-set-bit clearing — dp[i] = dp[i & (i-1)] + 1
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Popcount of every integer 0..n, via the
     *           last-set-bit-clearing DP recurrence.
     * Inputs  : n — the upper bound of the range to fill.
     * Output  : std::vector<int> — ans[i] = popcount(i).
     */
    std::vector<int> countBits(int n) {
        // dp table: one slot per value; dp[0] = 0 by construction.
        std::vector<int> dp(n + 1, 0);

        // i & (i - 1) deletes i's LOWEST set bit (0191's identity),
        // so it has exactly one fewer 1-bit than i and is smaller:
        // dp[i] = dp[that number] + 1. Also acyclic, also O(1) each.
        for (int i = 1; i <= n; ++i) {
            dp[i] = dp[i & (i - 1)] + 1;
        }
        return dp;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test table: { n, expected popcount array }.
    std::vector<std::pair<int, std::vector<int>>> tests = {
        {2, {0, 1, 1}},
        {5, {0, 1, 1, 2, 1, 2}},
        {8, {0, 1, 1, 2, 1, 2, 2, 3, 1}}
    };

    // --- Approach 1: run every test, measure time + peak RAM ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool ok_1 = true;
    for (const auto& t : tests) {
        std::vector<int> got = Solution_1().countBits(t.first);
        bool pass = got == t.second;
        ok_1 = ok_1 && pass;
        std::cout << "  A1 countBits(" << t.first << ") = [";
        for (size_t i = 0; i < got.size(); ++i) {
            std::cout << got[i] << (i + 1 < got.size() ? "," : "");
        }
        std::cout << "]  expected " << (pass ? "match" : "MISMATCH")
                  << (pass ? "  PASS" : "  FAIL") << "\n";
    }
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    // nanoseconds → microseconds; ru_maxrss is ALREADY in KB on Linux.
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;  // KB

    // --- Approach 2: run every test, measure time + peak RAM ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    bool ok_2 = true;
    for (const auto& t : tests) {
        std::vector<int> got = Solution_2().countBits(t.first);
        bool pass = got == t.second;
        ok_2 = ok_2 && pass;
        std::cout << "  A2 countBits(" << t.first << ") = [";
        for (size_t i = 0; i < got.size(); ++i) {
            std::cout << got[i] << (i + 1 < got.size() ? "," : "");
        }
        std::cout << "]  expected " << (pass ? "match" : "MISMATCH")
                  << (pass ? "  PASS" : "  FAIL") << "\n";
    }
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;  // KB

    // Summary lines: time in µs, memory delta in KB.
    std::cout << "Approach 1 (dp[i>>1] + (i&1)) : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (dp[i&(i-1)] + 1)  : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (ok_1 && ok_2
                  ? "PASS : both approaches produce identical popcount arrays."
                  : "FAIL : at least one test mismatched.")
              << "\n";

    return 0;
}
