/*
 * =====================================================================
 * LeetCode 136 : Single Number                                       (Easy)
 * https://leetcode.com/problems/single-number/
 * Category   : Bit Manipulation
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a non-empty array of integers where EVERY element appears
 *   EXACTLY TWICE except ONE which appears exactly ONCE, find the
 *   single one. Must run in O(n) time and O(1) extra space.
 *   Example: [4,1,2,1,2] → 4.
 * ---------------------------------------------------------------------
 * INTUITION
 *   XOR is its own inverse: applying it twice returns the original
 *   value. That means "xor everything together" annihilates every
 *   PAIR in the array and leaves exactly the one unpaired element.
 *   No extra memory, no counting, one pass. The bitwise view is
 *   even clearer: each pair of 1-bits at the same position cancels
 *   to 0, so only bits owned by the singleton survive.
 * ---------------------------------------------------------------------
 * APPROACH 1 — XOR everything (BEST)
 *   acc = 0; for every num: acc ^= num. Pairs vanish (x ^ x = 0),
 *   order does not matter (commutative + associative), and the lone
 *   survivor is acc. O(1) space — no data structure at all.
 *   Time  Complexity : O(n)   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Hash set toggle
 *   Add each number to a set; when a number is seen a SECOND time,
 *   remove it. The only element left in the set when the array ends
 *   is the singleton. O(n) space, so it fails the "O(1)" clause —
 *   shown here purely as the brute-force baseline that XOR beats.
 *   Time  Complexity : O(n)   Space Complexity : O(n).
 * ---------------------------------------------------------------------
 * DEEP DIVE — why XOR pairs vanish (the cancellation law)
 *   XOR truth table: 0^0=0, 0^1=1, 1^0=1, 1^1=0. Two identities:
 *       x ^ 0 = x     (xor with zero is identity)
 *       x ^ x = 0     (xor with itself cancels)
 *   And xor is commutative (a^b = b^a) and associative ((a^b)^c =
 *   a^(b^c)), so the array order is irrelevant. Group every pair:
 *       (v1 ^ v1) ^ (v2 ^ v2) ^ ... ^ s  =  0 ^ 0 ^ ... ^ s  =  s
 *   This is EXACTLY why disk arrays use XOR for parity: it can be
 *   undone by itself.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing benchmark results
#include <vector>        // std::vector — the input array
#include <cstdint>       // std::int32_t — fixed-width element type
#include <climits>       // INT_MIN — edge case for the test table
#include <chrono>        // std::chrono::steady_clock — timing for benchmark
#include <sys/resource.h>// getrusage — peak RAM measurement for benchmark
#include <unordered_set> // std::unordered_set — approach 2's toggle set

/* =====================================================================
 * APPROACH 1 : XOR everything — pairs cancel, singleton survives
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Find the element that appears exactly once, given
     *           that every other element appears exactly twice.
     * Inputs  : nums — the array to scan (must satisfy the guarantee).
     * Output  : int — the single non-paired element.
     */
    int singleNumber(const std::vector<int>& nums) {
        // Accumulator: 0 is the XOR identity, so starting here keeps
        // the FIRST element unchanged (x ^ 0 == x).
        int acc = 0;

        // One pass. Because xor is commutative and associative, the
        // order we visit elements is irrelevant: every pair cancels
        // itself out, wherever it lives in the array.
        for (int num : nums) {
            acc ^= num;
        }
        return acc;
    }
};

/* =====================================================================
 * APPROACH 2 : Hash set toggle — add once, remove on the second sight
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Find the unique element via add/remove toggling in a
     *           hash set — the O(n)-space baseline XOR beats.
     * Inputs  : nums — the array to scan (satisfies the guarantee).
     * Output  : int — the single non-paired element.
     */
    int singleNumber(const std::vector<int>& nums) {
        // seen : values currently holding an ODD count of visits.
        std::unordered_set<int> seen;

        // Toggle membership: first sight inserts, second sight erases.
        // After the loop, the ONLY remaining key is the singleton —
        // everything else was toggled out by its own second occurrence.
        for (int num : nums) {
            auto it = seen.find(num);
            if (it != seen.end()) {
                seen.erase(it);   // second occurrence → pair complete
            } else {
                seen.insert(num); // first occurrence → remember it
            }
        }

        // Exactly one key survives the toggling.
        return *seen.begin();
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test table: { array, expected singleton }.
    std::vector<std::pair<std::vector<int>, int>> tests = {
        {{2, 2, 1}, 1},
        {{4, 1, 2, 1, 2}, 4},
        {{1}, 1},
        {{INT_MIN, 7, 7, INT_MIN, 42}, 42}
    };

    // --- Approach 1: run every test, measure time + peak RAM ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool ok_1 = true;
    for (const auto& t : tests) {
        int got = Solution_1().singleNumber(t.first);
        bool pass = got == t.second;
        ok_1 = ok_1 && pass;
        std::cout << "  A1 singleNumber(" << t.first.size() << " elems) = "
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
        int got = Solution_2().singleNumber(t.first);
        bool pass = got == t.second;
        ok_2 = ok_2 && pass;
        std::cout << "  A2 singleNumber(" << t.first.size() << " elems) = "
                  << got << "  expected " << t.second
                  << (pass ? "  PASS" : "  FAIL") << "\n";
    }
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;  // KB

    // Summary lines: time in µs, memory delta in KB.
    std::cout << "Approach 1 (XOR, O(1) space) : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (hash set toggle) : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (ok_1 && ok_2
                  ? "PASS : both approaches find the singleton in every test."
                  : "FAIL : at least one test mismatched.")
              << "\n";

    return 0;
}
