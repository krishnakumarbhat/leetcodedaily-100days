/*
 * =====================================================================
 * LeetCode 268 : Missing Number                                     (Easy)
 * https://leetcode.com/problems/missing-number/
 * Category   : Bit Manipulation
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array `nums` containing n DISTINCT numbers taken from
 *   0, 1, 2, ..., n, return the ONE number that is missing from the
 *   range. Example: [3,0,1] → 2. Must run in O(n) time and O(1)
 *   extra space.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The array plus the missing value forms the full set {0..n}.
 *   Two algebraic lenses see the hole instantly:
 *     • SUM: the full range sums to n(n+1)/2; subtract the array's
 *       sum — the difference IS the missing number.
 *     • XOR: xor every index with every value. Every (index, value)
 *       pair that is present cancels (x ^ x = 0, exactly the 0136
 *       trick), leaving the index that never matched a value.
 * ---------------------------------------------------------------------
 * APPROACH 1 — XOR of all indices and values (BEST)
 *   acc = n; for i in 0..n-1: acc ^= i ^ nums[i]. Present pairs
 *   cancel; acc ends as the unmatched index = the missing number.
 *   No overflow possible — the sum approach can overflow int32 for
 *   large n; XOR cannot.
 *   Time  Complexity : O(n)   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sum formula
 *   expected = n(n+1)/2; return expected − Σ nums. O(n) time and
 *   O(1) space, but n(n+1)/2 grows quadratically — an int32 can
 *   overflow for n beyond ~65536 without 64-bit arithmetic.
 *   Time  Complexity : O(n)   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the XOR works, step by step
 *   We KNOW the full range {0..n} has n+1 distinct values. Its XOR
 *   depends only on n. Now xor in every ARRAY element:
 *       acc = n
 *       acc ^= 0 ^ nums[0] ^ 1 ^ nums[1] ^ ... ^ (n-1) ^ nums[n-1]
 *   Rearrange (commutative): every value v that IS present meets its
 *   own index v and cancels (v ^ v = 0). The one index m whose value
 *   is absent has nothing to cancel with — it is the sole survivor.
 *   Identical machinery to 0136 Single Number — same proof, new hat.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing benchmark results
#include <vector>        // std::vector — the input array
#include <cstdint>       // std::int64_t — overflow-free sum lane
#include <climits>       // INT_MAX — scale check for the test table
#include <chrono>        // std::chrono::steady_clock — timing for benchmark
#include <sys/resource.h>// getrusage — peak RAM measurement for benchmark

/* =====================================================================
 * APPROACH 1 : XOR of all indices and values — pairs cancel
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Find the single value missing from 0..n in `nums`.
     * Inputs  : nums — n distinct integers from the range 0..n.
     * Output  : int — the missing value.
     */
    int missingNumber(const std::vector<int>& nums) {
        // Start with n: it is the only index with NO counterpart in
        // the array a priori (the array spans indices 0..n-1).
        int acc = static_cast<int>(nums.size());

        // Pair every index with the value living at it. Present pairs
        // cancel to 0; the missing index never finds its partner.
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            acc ^= i ^ nums[i];
        }
        return acc;
    }
};

/* =====================================================================
 * APPROACH 2 : Sum formula — full range minus the array
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Find the missing value using the arithmetic-series
     *           formula; the 64-bit lane dodges the quadratic growth.
     * Inputs  : nums — n distinct integers from the range 0..n.
     * Output  : int — the missing value.
     */
    int missingNumber(const std::vector<int>& nums) {
        // Full range {0..n} sums to n(n+1)/2 — compute in a 64-bit
        // lane because n(n+1) overflows int32 for n > 65535.
        std::int64_t n = static_cast<std::int64_t>(nums.size());
        std::int64_t expected = n * (n + 1) / 2;

        // Accumulate the array's actual sum — int64 again for safety.
        std::int64_t actual = 0;
        for (int v : nums) {
            actual += v;
        }

        // The difference is the missing value, and it always fits int.
        return static_cast<int>(expected - actual);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test table: { array, expected missing value } — the official
    // examples plus a large-range case where the sum grows.
    std::vector<std::pair<std::vector<int>, int>> tests = {
        {{3, 0, 1}, 2},
        {{0, 1}, 2},
        {{9, 6, 4, 2, 3, 5, 7, 0, 1}, 8},
        {{0, 1, 2, 3, 4, 5, 6, 7, 9}, 8}
    };

    // --- Approach 1: run every test, measure time + peak RAM ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool ok_1 = true;
    for (const auto& t : tests) {
        int got = Solution_1().missingNumber(t.first);
        bool pass = got == t.second;
        ok_1 = ok_1 && pass;
        std::cout << "  A1 missingNumber(" << t.first.size() << " elems) = "
                  << got << "  expected " << t.second
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
        int got = Solution_2().missingNumber(t.first);
        bool pass = got == t.second;
        ok_2 = ok_2 && pass;
        std::cout << "  A2 missingNumber(" << t.first.size() << " elems) = "
                  << got << "  expected " << t.second
                  << (pass ? "  PASS" : "  FAIL") << "\n";
    }
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;  // KB

    // Summary lines: time in µs, memory delta in KB.
    std::cout << "Approach 1 (XOR pairs)       : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (sum formula)     : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (ok_1 && ok_2
                  ? "PASS : both approaches find every missing number."
                  : "FAIL : at least one test mismatched.")
              << "\n";

    return 0;
}
