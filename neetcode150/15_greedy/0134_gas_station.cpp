/*
 * =====================================================================
 * LeetCode 134 : Gas Station                                     (Medium)
 * https://leetcode.com/problems/gas-station/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   There are n gas stations in a circle (index i → i+1 mod n). From
 *   station i you gain gas[i] and the ride to i+1 costs cost[i].
 *   Starting with an EMPTY tank, find the station index where a full
 *   circle is possible, or -1. The answer is UNIQUE if it exists.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Define net[i] = gas[i] - cost[i]. A circle is feasible iff the
 *   TOTAL sum of net ≥ 0 (necessary AND sufficient — tank never needs
 *   to exceed total surplus). Now pick a start: walk with a running
 *   `tank`. The moment tank < 0 at station j, NO station in
 *   [start, j] can be a valid start — because any station s in that
 *   window enters with at least the same deficit (its own prefix of
 *   net is no better than the full prefix). So the candidate is
 *   reset to j+1. This single reset is the greedy move, and it is
 *   provably safe: a prefix with negative sum can be DISCARDED from
 *   every valid start consideration (exchange argument on prefixes).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Total sum + single-pass candidate (BEST)
 *     pass 1: total = Σ net → if total < 0 return -1.
 *     pass 2: tank += net[i]; if tank < 0 → start = i+1, tank = 0.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 *   WHY unique answer: if two starts s1 < s2 both worked, the segment
 *   [s1, s2) would have non-negative AND the whole circle feasible —
 *   forcing two disjoint feasible splits, contradicting uniqueness
 *   (only one start can work per problem guarantee).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Brute force O(n²) (for contrast)
 *   Try every start; simulate n stops keeping tank ≥ 0 at all times.
 *   Time  Complexity : O(n²)   Space Complexity : O(1)
 *   Correct but ignores the KEY insight: once a prefix goes negative
 *   the whole window is dead — the quadratic retry is pure waste.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why discarding a negative prefix is safe (greedy proof)
 *   Let P = prefix sum of net over [start, j], and P < 0 at j. For
 *   ANY s in [start, j), the tank at j when starting at s equals
 *   (prefix sum of [s, j)) = P - (prefix of [start, s)). Since the
 *   remaining walk [j+1 ...] adds the same tail to every candidate,
 *   the candidate whose carried-in value is LARGEST does best — that
 *   is s = start itself. If even start dies (P < 0), every s in the
 *   window dies too. Greedy reset = throwing away a provably-dead
 *   window; the total ≥ 0 check guarantees a live window remains.
 * =====================================================================
 */

#include <iostream>       // std::cout — benchmark output
#include <vector>         // std::vector — gas / cost arrays
#include <string>         // std::string — PASS/FAIL messages
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RSS measurement

/* =====================================================================
 * APPROACH 1 : Total-sum + single-pass candidate reset
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Find the unique start station that completes a circle.
     * Inputs  : gas  — gas[i] units gained at station i.
     *           cost — cost[i] units spent riding i → i+1.
     * Output  : int — valid start index, or -1 if none exists.
     */
    int canCompleteCircuit(const std::vector<int>& gas, const std::vector<int>& cost) {
        int total = 0; // Σ net — feasibility of the WHOLE circle
        int tank = 0;  // running fuel from the current candidate start
        int start = 0; // current best candidate

        for (int i = 0; i < static_cast<int>(gas.size()); ++i) {
            int net = gas[i] - cost[i];
            total += net;   // accumulate the global balance
            tank += net;    // accumulate the local balance

            if (tank < 0) {
                // Prefix [start..i] is negative → NO station inside it
                // can be a start (see DEEP DIVE). Reset the window.
                start = i + 1;
                tank = 0;   // new candidate begins with an empty tank
            }
        }
        // Total must cover the whole trip; the candidate is then exact.
        return total >= 0 ? start : -1;
    }
};

/* =====================================================================
 * APPROACH 2 : Brute force — simulate every candidate (O(n²))
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Find the unique start station that completes a circle.
     * Inputs  : gas  — gas[i] units gained at station i.
     *           cost — cost[i] units spent riding i → i+1.
     * Output  : int — valid start index, or -1 if none exists.
     */
    int canCompleteCircuit(const std::vector<int>& gas, const std::vector<int>& cost) {
        int n = static_cast<int>(gas.size());

        // Try every station as the start — the naive quadratic scan.
        for (int start = 0; start < n; ++start) {
            int tank = 0;
            bool ok = true;

            // Simulate n consecutive stops around the circle.
            for (int step = 0; step < n; ++step) {
                int i = (start + step) % n; // wrap around modulo n
                tank += gas[i] - cost[i];
                if (tank < 0) { ok = false; break; } // died mid-trip
            }
            if (ok) return start; // this start survived all n stops
        }
        return -1; // no station can complete the circle
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, time + peak RAM
 * ===================================================================== */
int main() {
    // Official examples + impossible circle + single-station edge.
    const std::vector<std::vector<int> > gas_tests = {
        { 1, 2, 3, 4, 5 },   // → 3
        { 2, 3, 4 },         // → -1
        { 5 },               // → 0
        { 1, 2, 3, 4, 5, 6 } // → 3
    };
    const std::vector<std::vector<int> > cost_tests = {
        { 3, 4, 5, 1, 2 },   // → 3
        { 3, 4, 3 },         // → -1
        { 4 },               // → 0
        { 6, 5, 4, 3, 2, 1 } // → 3 (unique start per problem guarantee)
    };
    const std::vector<int> expected = { 3, -1, 0, 3 };

    auto run_all = [&](int which, int (*solve)(const std::vector<int>&, const std::vector<int>&)) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto t0 = std::chrono::high_resolution_clock::now();

        bool ok = true;
        for (int t = 0; t < static_cast<int>(gas_tests.size()); ++t) {
            if (solve(gas_tests[t], cost_tests[t]) != expected[t]) ok = false;
        }

        auto t1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);
        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1000.0;
        long mem_kb = after.ru_maxrss - before.ru_maxrss; // delta, KB

        std::cout << "Approach " << which
                  << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " µs  peak-ram-delta = " << mem_kb << " KB\n";
        return ok;
    };

    bool a1 = run_all(1, [](const std::vector<int>& g, const std::vector<int>& c) { return Solution_1().canCompleteCircuit(g, c); });
    bool a2 = run_all(2, [](const std::vector<int>& g, const std::vector<int>& c) { return Solution_2().canCompleteCircuit(g, c); });
    std::cout << (a1 && a2 ? "PASS : both approaches find the correct start station."
                           : "FAIL : at least one approach is wrong.") << "\n";
    return 0;
}
