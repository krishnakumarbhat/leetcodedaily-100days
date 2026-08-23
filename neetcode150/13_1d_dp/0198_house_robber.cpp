/*
 * =====================================================================
 * LeetCode 198 : House Robber                                     (Medium)
 * https://leetcode.com/problems/house-robber/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Houses on a street hold cash nums[i] each. Adjacent houses share
 *   an alarm → you may NOT rob two neighbours. Maximise total loot.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Walk the street left→right. At house i the optimal plan is either
 *   "skip i" (best loot from houses 0..i-1) or "rob i" (cash[i] plus
 *   the best loot from houses 0..i-2 — house i-1 is now forbidden).
 *   The winner at i is the answer for every later house → optimal
 *   substructure with overlapping subproblems.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bottom-up with rolling variables (BEST)
 *   dp[i] = max loot from houses 0..i.
 *   Recurrence : dp[i] = max(dp[i-1], nums[i] + dp[i-2])
 *                dp[0] = nums[0], dp[1] = max(nums[0], nums[1])
 *   State space : i ∈ [0, n) → n states on array dp[n]; cell i reads
 *                only i-1 and i-2 → collapse the table into two
 *                rolling variables (prev2, prev1) → O(1) space.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down memoized recursion
 *   f(i) = max loot from houses 0..i — same recurrence, solved on
 *   demand and cached in memo[i].
 *   Trade-off : reads the street right-to-left, natural to derive;
 *               recursion depth n + memo lookup per state.
 *   Time  Complexity : O(n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why "skip" and "rob" capture every feasible plan
 *   Any valid selection over houses 0..i either excludes house i
 *   (then it IS a valid selection over 0..i-1) or includes it (then
 *   houses i-1 is excluded, leaving a selection over 0..i-2) — the two
 *   branches are exhaustive AND disjoint, so max() over them is exact.
 *   This is weighted interval scheduling on consecutive intervals —
 *   the same recurrence drives meeting-room allocation and task
 *   scheduling with 1-slot cool-down.
 *   State-space math: n states, O(1) combine each → O(n). The
 *   backward-only reads (i-1, i-2) again justify rolling variables:
 *   dp[i-3] and older are never consulted again.
 *   Real life : job scheduling with exclusion constraints, resource
 *   harvesting, and cellular network interference avoidance.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <sys/resource.h>
#include <algorithm>

/* =====================================================================
 * APPROACH 1 : bottom-up with two rolling variables
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Maximise loot without robbing adjacent houses.
     * Inputs  : nums — cash in each house.
     * Output  : int — maximum total loot.
     */
    int rob(const std::vector<int>& nums) {
        if (nums.empty()) {
            return 0;                      // empty street → nothing to take
        }
        if (nums.size() == 1) {
            return nums[0];                // single house → take it
        }
        // Rolling window: prev2 = dp[i-2], prev1 = dp[i-1].
        int prev2 = nums[0];
        int prev1 = std::max(nums[0], nums[1]);
        for (std::size_t i = 2; i < nums.size(); ++i) {
            // skip i  vs  rob i + best loot from houses 0..i-2.
            const int cur = std::max(prev1, nums[i] + prev2);
            prev2 = prev1;                 // slide the window right
            prev1 = cur;
        }
        return prev1;                      // dp[n-1]
    }
};

/* =====================================================================
 * APPROACH 2 : top-down memoized recursion
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Maximise loot without robbing adjacent houses (memoized).
     * Inputs  : nums — cash in each house.
     * Output  : int — maximum total loot.
     */
    int rob(const std::vector<int>& nums) {
        houses = nums;
        // memo[i] = -1 → range 0..i not solved yet.
        memo.assign(houses.size(), -1);
        return f(static_cast<int>(houses.size()) - 1);
    }

private:
    std::vector<int> houses;
    std::vector<int> memo;

    /*
     * Purpose : Recursive range solver with caching (top-down DP).
     * Inputs  : i — right end of the house range 0..i.
     * Output  : int — max loot from houses 0..i.
     */
    int f(int i) {
        if (i < 0) {
            return 0;              // no houses left → no loot
        }
        if (memo[i] != -1) {
            return memo[i];        // overlapping subproblem → reuse
        }
        // skip i  vs  rob i + best from 0..i-2 (i-1 is forbidden).
        return memo[i] = std::max(f(i - 1), houses[i] + f(i - 2));
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (nums, expected loot). Both solutions must match.
    struct Test { std::vector<int> nums; int expected; };
    const std::vector<Test> tests = {
        {{1, 2, 3, 1}, 4},      // rob 1 + 3
        {{2, 7, 9, 3, 1}, 12},  // rob 2 + 9 + 1
        {{2, 1, 1, 2}, 4}       // rob 2 + 2 (ends — not adjacent)
    };

    double total_us_1 = 0.0, total_us_2 = 0.0;
    long total_kb_1 = 0, total_kb_2 = 0;
    bool allPass = true;

    for (const Test& t : tests) {
        // --- Approach 1: time via steady_clock, RAM via getrusage ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().rob(t.nums);
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
        const int r2 = Solution_2().rob(t.nums);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        const double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        const long kb2 = after2.ru_maxrss - before2.ru_maxrss;
        total_us_2 += us2;
        total_kb_2 += kb2;

        const bool ok = (r1 == t.expected) && (r2 == t.expected);
        allPass = allPass && ok;

        std::cout << "A1=" << r1 << "  A2=" << r2
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