/*
 * =====================================================================
 * LeetCode 202 : Happy Number                                     (Easy)
 * https://leetcode.com/problems/happy-number/
 * Category   : Math & Geometry
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Start with any positive integer. Replace it with the sum of the
 *   squares of its digits. Repeat. If the sequence ever reaches 1,
 *   the number is HAPPY; otherwise it loops forever (cycles) and the
 *   number is UNHAPPY. Return whether n is happy.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The digit-square-sum map is deterministic: every number has ONE
 *   successor, so starting from n we walk a chain. A chain either
 *   lands on 1 (happy) or enters a CYCLE (unhappy — provably the
 *   cycle 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 for n ≥ 1).
 *   Detection = classic linked-list cycle detection:
 *   hash set of seen states (O(k) memory) or Floyd's tortoise & hare
 *   (O(1) memory).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Hash set of visited states (BEST readability)
 *   Compute successors; insert each into an unordered_set; if we hit
 *   1 → happy; if we hit a value already in the set → cycle → unhappy.
 *   Time  Complexity : O(log n) per step × steps until repeat.
 *   Space Complexity : O(k) where k = distinct states visited
 *   (k is tiny: for n ≤ 2^31 every state is ≤ 4·81+… = 729 at worst
 *   after the first step, and the whole chain fits in the 81-400
 *   range — k is bounded by a small constant).
 *   WHY it works: a functional graph (each node one outgoing edge)
 *   decomposes into chains ending in 1 or in a cycle; the set tells
 *   us which case we are in the moment a state repeats.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Floyd's cycle detection (tortoise & hare)
 *   Two pointers advance at speed 1 and speed 2. They meet inside
 *   the cycle IFF a cycle exists. If they meet at 1 → happy;
 *   otherwise the meet point proves a cycle → unhappy.
 *   Time  Complexity : O(k)   Space Complexity : O(1)
 *   WHY it works: distance between tortoise and hare shrinks by 1
 *   per step once both are inside the cycle (classic invariant), so
 *   they collide in ≤ cycle length steps.
 * ---------------------------------------------------------------------
 * DEEP DIVE — digit-square-sum bounds
 *   For a k-digit number the successor is ≤ k·81. For k ≥ 4 that is
 *   strictly smaller than the number itself (10^(k-1) > 81k for
 *   k ≥ 4), so every chain drops into ≤ 3-digit territory fast and
 *   the state space is bounded → cycles are GUARANTEED to be found,
 *   never an infinite walk. This is the same argument that proves
 *   termination of the whole process.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — formatting result lines
#include <vector>         // std::vector — (unused; uniform include set)
#include <unordered_map>  // (unused here; kept for uniform include set)
#include <unordered_set>  // std::unordered_set — seen-state set (A1)
#include <chrono>         // std::chrono — steady_clock timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Hash set of visited states
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether n is a happy number.
     * Inputs  : n — positive integer to test.
     * Output  : true if the digit-square-sum chain reaches 1.
     */
    bool isHappy(int n) {
        std::unordered_set<int> seen;

        // Deterministic chain: keep applying the successor map until
        // we reach 1 (happy) or revisit a state (cycle → unhappy).
        while (n != 1 && seen.find(n) == seen.end()) {
            seen.insert(n);
            n = nextValue(n);
        }
        return n == 1;
    }

private:
    /*
     * Purpose : Compute the sum of squares of the digits of n.
     * Inputs  : n — the current state.
     * Output  : int successor state.
     */
    static int nextValue(int n) {
        int sum = 0;
        while (n > 0) {
            const int d = n % 10;       // peel the last digit
            sum += d * d;               // square it into the sum
            n /= 10;                    // drop the digit
        }
        return sum;
    }
};

/* =====================================================================
 * APPROACH 2 : Floyd's cycle detection (tortoise & hare)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether n is a happy number, O(1) memory.
     * Inputs  : n — positive integer to test.
     * Output  : true if the digit-square-sum chain reaches 1.
     */
    bool isHappy(int n) {
        // Tortoise advances one step, hare two — both on the chain.
        int slow = n;
        int fast = n;

        // Until the hare hits 1 (happy) or the pointers meet inside
        // a cycle (unhappy). Start by moving before the first check.
        do {
            slow = nextValue(slow);
            fast = nextValue(nextValue(fast));
        } while (slow != fast && fast != 1);

        // Meeting at 1 is the only non-cycle terminal state.
        return fast == 1;
    }

private:
    /*
     * Purpose : Compute the sum of squares of the digits of n.
     * Inputs  : n — the current state.
     * Output  : int successor state.
     */
    static int nextValue(int n) {
        int sum = 0;
        while (n > 0) {
            const int d = n % 10;
            sum += d * d;
            n /= 10;
        }
        return sum;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests; time + peak RAM
 * ===================================================================== */
int main() {
    // (n, expected) — 19 → 1²+9²=82 → 68 → 100 → 1 (happy);
    // 2 enters the 4-16-37-58-89-145-42-20 cycle (unhappy).
    const int tests[] = { 19, 2, 1 };
    const bool expected[] = { true, false, true };

    bool all_ok = true;

    const auto run_all = [&](const std::string& label, const auto& solve) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        const auto t0 = std::chrono::steady_clock::now();

        bool ok = true;
        for (size_t t = 0; t < 3; ++t) {
            const bool got = solve(tests[t]);
            const bool pass = (got == expected[t]);
            ok = ok && pass;
            std::cout << "  n = " << tests[t] << " → " << (got ? "happy" : "unhappy")
                      << (pass ? "  PASS" : "  FAIL") << "\n";
        }

        const auto t1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        const double us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
        const long kb = after.ru_maxrss - before.ru_maxrss;
        std::cout << label << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " us  peak-mem = " << kb << " KB\n";
        all_ok = all_ok && ok;
    };

    std::cout << "Test suite: 3 fixed cases\n";
    run_all("Approach 1 (hash set of states)    ", [](int n) {
        return Solution_1().isHappy(n);
    });
    run_all("Approach 2 (Floyd tortoise & hare) ", [](int n) {
        return Solution_2().isHappy(n);
    });

    std::cout << (all_ok
                  ? "PASS : both approaches classify every test correctly."
                  : "FAIL : at least one test failed.") << "\n";
    return all_ok ? 0 : 1;
}