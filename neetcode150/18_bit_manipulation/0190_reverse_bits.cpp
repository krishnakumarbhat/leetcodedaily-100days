/*
 * =====================================================================
 * LeetCode 190 : Reverse Bits                                       (Easy)
 * https://leetcode.com/problems/reverse-bits/
 * Category   : Bit Manipulation
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Reverse the bits of a given 32-bit unsigned integer. Bit 31 of
 *   the input becomes bit 0 of the output, bit 30 becomes bit 1, etc.
 *   Example: 43261596 (00000010100101000001111010011100)
 *         →  964176192 (00111001011110000010100101000000).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Bit reversal is the same motion as digit reversal in decimal:
 *   take one bit off the right end of the input and place it onto the
 *   LEFT end of an accumulator 32 times. A faster route is "divide
 *   and conquer": swap the 16-bit halves, then the 8-bit quarters,
 *   then 4-bit blocks, 2-bit blocks, and finally adjacent bits — five
 *   masked swaps total, each halving the block size.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Shift-and-OR assembly, 32 iterations (clear)
 *   result = 0; repeat 32 times: result = (result << 1) | (n & 1);
 *   n >>= 1. Each round lifts the input's rightmost bit and drops it
 *   into the accumulator's rightmost slot, which is about to be
 *   promoted one position left. The input's bits are thus consumed
 *   low-to-high and emitted high-to-low — a reversal.
 *   Time  Complexity : O(1) — exactly 32 fixed iterations.
 *   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * APPROACH 2 — 5 masked block swaps (divide & conquer)
 *   x = swap 16-bit halves; x = swap 8-bit quarters; x = swap 4-bit
 *   blocks; x = swap 2-bit blocks; x = swap adjacent bits. Each swap
 *   moves the block to its mirror position. After the 5th, every bit
 *   has been mirrored exactly once → the full reversal.
 *   Time  Complexity : O(1) — FIVE operations, no loop.
 *   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — deriving the block-swap masks
 *   Start from the requirement: output bit b must equal input bit
 *   31−b. Split at the midpoint: input bits 0..15 must land in
 *   output bits 16..31, i.e. SWAP THE HALVES. Repeat inside each
 *   half (8-bit quarters), then inside each quarter (4-bit blocks),
 *   etc. The masks isolate every other block of size 2^k:
 *       swap halves:  (x >> 16) | (x << 16)
 *       swap 8s:      ((x & 0xFF00FF00) >> 8)  | ((x & 0x00FF00FF) << 8)
 *       swap 4s:      ((x & 0xF0F0F0F0) >> 4)  | ((x & 0x0F0F0F0F) << 4)
 *       swap 2s:      ((x & 0xCCCCCCCC) >> 2)  | ((x & 0x33333333) << 2)
 *       swap 1s:      ((x & 0xAAAAAAAA) >> 1)  | ((x & 0x55555555) << 1)
 *   Each stage preserves the work of the previous one because the
 *   masks only touch bits that already live in mirrored positions.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing benchmark results
#include <vector>        // std::vector — the test-case table
#include <cstdint>       // std::uint32_t — the 32-bit operand type
#include <climits>       // UINT32_MAX — edge case for the test table
#include <chrono>        // std::chrono::steady_clock — timing for benchmark
#include <sys/resource.h>// getrusage — peak RAM measurement for benchmark

/* =====================================================================
 * APPROACH 1 : Shift-and-OR assembly — 32 iterations
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Reverse all 32 bits of an unsigned 32-bit integer.
     * Inputs  : n — the value whose bits must be mirrored.
     * Output  : std::uint32_t — the bit-reversed value.
     */
    std::uint32_t reverseBits(std::uint32_t n) {
        // Accumulator that the input's bits are poured into, one per
        // round, each arriving at the top of the pile.
        std::uint32_t result = 0;

        // Exactly 32 rounds — one per bit of a uint32_t.
        for (int i = 0; i < 32; ++i) {
            // Shift the pile left (making room at bit 0) and OR in the
            // input's current lowest bit.
            result = (result << 1) | (n & 1);
            // Drop the consumed bit: the next round reads n bit 1,
            // then bit 2, ... i.e. the input is read LOW → HIGH while
            // the result is written HIGH → LOW.
            n >>= 1;
        }
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : Five masked block swaps (divide & conquer)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Reverse all 32 bits using 5 halving block swaps.
     * Inputs  : n — the value whose bits must be mirrored.
     * Output  : std::uint32_t — the bit-reversed value.
     */
    std::uint32_t reverseBits(std::uint32_t n) {
        // Stage 1: mirror the two 16-bit halves.
        //     x >> 16   → moves the HIGH half down to the LOW position
        //     x << 16   → moves the LOW  half up to the HIGH position
        n = (n >> 16) | (n << 16);

        // Stage 2: mirror the four 8-bit blocks. Mask keeps every
        // other byte:  0xFF00FF00 = high byte of each 16-bit pair.
        n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8);

        // Stage 3: mirror the eight 4-bit nibbles.
        n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4);

        // Stage 4: mirror the sixteen 2-bit blocks.
        //   0xCCCCCCCC = 1100 1100 ... (every other 2-bit block)
        n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2);

        // Stage 5: swap adjacent bits — the finest granularity.
        //   0xAAAAAAAA = 1010 1010 ... (every other single bit)
        n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1);

        return n;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test table: { input, expected reversal } — the official example
    // plus its boundary neighbours (0 and all-ones).
    std::vector<std::pair<std::uint32_t, std::uint32_t>> tests = {
        {43261596u, 964176192u},
        {0u, 0u},
        {UINT32_MAX, UINT32_MAX}
    };

    // --- Approach 1: run every test, measure time + peak RAM ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool ok_1 = true;
    for (const auto& t : tests) {
        std::uint32_t got = Solution_1().reverseBits(t.first);
        bool pass = got == t.second;
        ok_1 = ok_1 && pass;
        std::cout << "  A1 reverseBits(" << t.first << ") = " << got
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
        std::uint32_t got = Solution_2().reverseBits(t.first);
        bool pass = got == t.second;
        ok_2 = ok_2 && pass;
        std::cout << "  A2 reverseBits(" << t.first << ") = " << got
                  << "  expected " << t.second
                  << (pass ? "  PASS" : "  FAIL") << "\n";
    }
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;  // KB

    // Summary lines: time in µs, memory delta in KB.
    std::cout << "Approach 1 (shift-and-OR ×32)  : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (5 block swaps)     : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (ok_1 && ok_2
                  ? "PASS : both approaches reverse every test value correctly."
                  : "FAIL : at least one test mismatched.")
              << "\n";

    return 0;
}
