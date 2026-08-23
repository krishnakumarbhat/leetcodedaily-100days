/*
 * =====================================================================
 * LeetCode 191 : Number of 1 Bits                                   (Easy)
 * https://leetcode.com/problems/number-of-1-bits/
 * Category   : Bit Manipulation
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an unsigned 32-bit integer, return the number of '1' bits
 *   in its binary representation (the Hamming weight / popcount).
 *   Example: 11 = 1011₂ → 3.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Counting needs a way to "remove one set bit per step". The trick
 *   x & (x - 1) clears exactly the LOWEST set bit of x — repeatedly
 *   applying it makes x zero in exactly `popcount(x)` steps, so the
 *   number of rounds IS the answer. No bit scanning, no wasted
 *   iterations over zero bits.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Kernighan's algorithm (BEST)
 *   count = 0; while (n) { n &= n - 1; ++count; }. One round per
 *   SET bit — zeros never cost an iteration.
 *   Time  Complexity : O(popcount) ≤ O(32) = O(1).
 *   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Scan all 32 bits
 *   count = 0; for i in 0..31: count += n & 1; n >>= 1. Checks every
 *   position, including zeros — simple, predictable 32 rounds.
 *   Time  Complexity : O(32) = O(1).   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — deriving x & (x - 1): why it clears the LOWEST 1-bit
 *   Write x in binary: ...1 0 0 0, where the lowest 1-bit sits at
 *   position k with only 0-bits below it. Subtracting 1 borrows
 *   through those zeros, flipping the bit at k to 0 and every bit
 *   below it to 1:
 *       x     = ...1 0 0 0  (bits above k unchanged)
 *       x - 1 = ...0 1 1 1  (bit k cleared, below becomes all-ones)
 *   Now AND them: positions above k match (both have the original
 *   bits), position k is 1 & 0 = 0, positions below are 0 & 1 = 0.
 *   Result: x with its lowest 1-bit removed — exactly one bit
 *   cleared, everything else untouched.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing benchmark results
#include <vector>        // std::vector — the test-case table
#include <cstdint>       // std::uint32_t — the 32-bit operand type
#include <climits>       // UINT32_MAX — edge case for the test table
#include <chrono>        // std::chrono::steady_clock — timing for benchmark
#include <sys/resource.h>// getrusage — peak RAM measurement for benchmark

/* =====================================================================
 * APPROACH 1 : Kernighan — one iteration per SET bit
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Count the set bits (Hamming weight) of a uint32_t.
     * Inputs  : n — the value to count bits of.
     * Output  : int — the number of 1-bits in n.
     */
    int hammingWeight(std::uint32_t n) {
        int count = 0;

        // Each round wipes exactly ONE set bit (the lowest one), so
        // the loop runs popcount(n) times — zero bits cost nothing.
        while (n != 0) {
            n &= n - 1;   // clears the lowest set bit (see deep dive)
            ++count;
        }
        return count;
    }
};

/* =====================================================================
 * APPROACH 2 : Scan all 32 bit positions
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Count the set bits by examining every one of the 32
     *           positions, including the zero bits.
     * Inputs  : n — the value to count bits of.
     * Output  : int — the number of 1-bits in n.
     */
    int hammingWeight(std::uint32_t n) {
        int count = 0;

        // Fixed 32 rounds: pull the lowest bit off, add it, shift.
        // n >>= 1 on an UNSIGNED int is a logical shift — zero fills
        // the top, so the loop runs exactly 32 times and stops.
        for (int i = 0; i < 32; ++i) {
            count += n & 1;
            n >>= 1;
        }
        return count;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test table: { input, expected popcount } — official example,
    // a sparse value, and the all-ones boundary.
    std::vector<std::pair<std::uint32_t, int>> tests = {
        {11u, 3},        // 1011₂ → three 1-bits
        {128u, 1},       // 10000000₂ → one 1-bit
        {UINT32_MAX, 32} // all ones → thirty-two 1-bits
    };

    // --- Approach 1: run every test, measure time + peak RAM ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool ok_1 = true;
    for (const auto& t : tests) {
        int got = Solution_1().hammingWeight(t.first);
        bool pass = got == t.second;
        ok_1 = ok_1 && pass;
        std::cout << "  A1 hammingWeight(" << t.first << ") = " << got
                  << "  expected " << t.second
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
        int got = Solution_2().hammingWeight(t.first);
        bool pass = got == t.second;
        ok_2 = ok_2 && pass;
        std::cout << "  A2 hammingWeight(" << t.first << ") = " << got
                  << "  expected " << t.second
                  << (pass ? "  PASS" : "  FAIL") << "\n";
    }
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;  // KB

    // Summary lines: time in µs, memory delta in KB.
    std::cout << "Approach 1 (Kernighan)      : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (32-bit scan)    : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (ok_1 && ok_2
                  ? "PASS : both approaches count every test value correctly."
                  : "FAIL : at least one test mismatched.")
              << "\n";

    return 0;
}
