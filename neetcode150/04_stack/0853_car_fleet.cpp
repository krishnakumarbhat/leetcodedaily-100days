/*
 * =====================================================================
 * LeetCode 853 : Car Fleet                                        (Medium)
 * https://leetcode.com/problems/car-fleet/
 * Category   : Stack (monotonic)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   n cars drive to a target mile. Each car starts at `position[i]`
 *   with `speed[i]` (mph), all moving toward the target. A car NEVER
 *   passes another: if a faster car catches a slower one AHEAD, it
 *   slows down and they merge into one FLEET (the fleet keeps the
 *   speed of the slowest leader). Count the number of fleets that
 *   arrive at the target.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A car at position p reaches the target at time (target − p)/speed.
 *   Sort cars by position from the target backwards (nearest first).
 *   The nearest car is its own fleet. Each car BEHIND merges iff its
 *   arrival time ≤ the time of the fleet in front of it (it would
 *   catch up before the target). So we walk backwards and keep only
 *   the arrival times that are STRICTLY GREATER than the last kept
 *   one — every kept time = one new fleet. A stack stores them.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sort + stack of arrival times (BEST)
 *   Sort (position, speed) pairs by position DESCENDING (nearest to
 *   target first). Maintain a stack of arrival times that is
 *   STRICTLY INCREASING bottom→top. Push t only if t is greater than
 *   the current top — otherwise the car merges into the fleet ahead.
 *   Answer = stack size.
 *   Time  Complexity : O(n log n)  — dominated by the sort.
 *   Space Complexity : O(n)  — the pairs + the stack.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort + running maximum (no stack)
 *   Same sort and walk, but the "stack" shrinks to one variable: the
 *   arrival time of the slowest leader so far (the fleet's time).
 *   Count a new fleet every time a car's time exceeds it.
 *   Time  Complexity : O(n log n)  Space Complexity : O(1) extra.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — same monotonic invariant again
 *   The stack of times is MONOTONIC (strictly increasing): pushing a
 *   smaller/equal time would be pointless because that car merges.
 *   This is the same "keep only what beats the running extreme"
 *   pattern as 0084 and 0739 — sorted order turns a geometric chase
 *   into a linear walk. Float time is exact enough here; the problem
 *   tolerates tiny errors because merges are decided by comparison.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing test + benchmark output
#include <vector>       // std::vector — positions, speeds
#include <stack>        // std::stack — the monotonic stack of times
#include <utility>      // std::pair — (position, speed) bundles
#include <algorithm>    // std::sort — order cars by position
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Sort + stack of arrival times
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Count fleets arriving at the target.
     * Inputs  : target — mile marker all cars drive toward.
     *           position — starting mile of each car.
     *           speed — mph of each car (position[i] pairs with speed[i]).
     * Output  : number of distinct fleets that reach the target.
     */
    int carFleet(int target, const std::vector<int>& position,
                 const std::vector<int>& speed) {
        int n = static_cast<int>(position.size());

        // Pair each car, sorted by position DESCENDING — nearest to
        // the target first (that is the direction fleets form).
        std::vector<std::pair<int, int>> cars;
        for (int i = 0; i < n; ++i) cars.emplace_back(position[i], speed[i]);
        std::sort(cars.begin(), cars.end(),
                  [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
                      return a.first > b.first;   // descending position
                  });

        // times : arrival times of fleet leaders so far. Values are
        // STRICTLY INCREASING bottom→top (invariant of the walk).
        std::stack<double> times;

        for (const std::pair<int, int>& c : cars) {

            // Hours to drive (target − position) miles at `speed` mph.
            double t = static_cast<double>(target - c.first) / c.second;

            // If this car's arrival time EXCEEDS the fleet in front,
            // it never catches up → it starts its OWN fleet.
            if (times.empty() || t > times.top()) {
                times.push(t);
            }
            // Else t ≤ leader time → this car merges: no new fleet,
            // the leader's (slower) time already represents it.
        }

        // Every stack entry is one fleet leader → count = fleets.
        return static_cast<int>(times.size());
    }
};

/* =====================================================================
 * APPROACH 2 : Sort + running maximum (stack replaced by 1 variable)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Count fleets arriving at the target.
     * Inputs  : target — mile marker all cars drive toward.
     *           position — starting mile of each car.
     *           speed — mph of each car (position[i] pairs with speed[i]).
     * Output  : number of distinct fleets that reach the target.
     */
    int carFleet(int target, const std::vector<int>& position,
                 const std::vector<int>& speed) {
        int n = static_cast<int>(position.size());

        // Same descending sort as approach 1.
        std::vector<std::pair<int, int>> cars;
        for (int i = 0; i < n; ++i) cars.emplace_back(position[i], speed[i]);
        std::sort(cars.begin(), cars.end(),
                  [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
                      return a.first > b.first;
                  });

        // Only the SLOWEST leader time matters for merging decisions —
        // that single value replaces the whole stack.
        double slowest = 0.0;
        int fleets = 0;

        for (const std::pair<int, int>& c : cars) {
            double t = static_cast<double>(target - c.first) / c.second;

            // New fleet only when this car cannot catch the current
            // leader; then IT becomes the new (slower) leader.
            if (t > slowest) {
                ++fleets;
                slowest = t;
            }
        }

        return fleets;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // --- Correctness tests (2-3 cases per solution) ---
    struct Test { int target; std::vector<int> pos; std::vector<int> spd; int expect; };
    Test tests[] = {
        // Official example 1 → 3 fleets.
        {12, {10, 8, 0, 5, 3}, {2, 4, 1, 1, 3}, 3},
        // Single car → 1 fleet.
        {10, {3}, {3}, 1},
        // All merge into one fleet (10,7) → (8,2) catches up.
        {100, {0, 2, 4}, {4, 2, 1}, 1},
        // Official example 3: all arrive separately → 2 fleets.
        {100, {0, 2, 4}, {4, 2, 3}, 2}
    };

    bool all_ok = true;
    for (const Test& t : tests) {
        int r1 = Solution_1().carFleet(t.target, t.pos, t.spd);
        int r2 = Solution_2().carFleet(t.target, t.pos, t.spd);
        if (r1 != t.expect || r2 != t.expect) all_ok = false;
        std::cout << (r1 == t.expect && r2 == t.expect ? "PASS" : "FAIL")
                  << " : target=" << t.target << " n=" << t.pos.size()
                  << "  stack=" << r1 << "  maxvar=" << r2
                  << "  expect=" << t.expect << "\n";
    }

    // --- Benchmark: 50k random cars ---
    const int N = 50000;
    const int TARGET = 1000000;
    std::vector<int> pos(N), spd(N);
    for (int i = 0; i < N; ++i) {
        pos[i] = (i * 7919) % TARGET;
        // 64-bit multiply avoids signed overflow (UB) at i ≈ 20k.
        spd[i] = 1 + static_cast<int>((i * 104729LL) % 100);
    }

    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    int r1 = Solution_1().carFleet(TARGET, pos, spd);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB delta

    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    int r2 = Solution_2().carFleet(TARGET, pos, spd);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (sort + stack)    : " << r1
              << " fleets  time = " << us_1 << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (sort + max var)  : " << r2
              << " fleets  time = " << us_2 << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (all_ok ? "PASS : all tests" : "FAIL : a test was wrong")
              << "\n";
    return all_ok ? 0 : 1;
}
