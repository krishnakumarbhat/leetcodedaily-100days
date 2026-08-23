/*
 * =====================================================================
 * LeetCode 213 : House Robber II                                  (Medium)
 * https://leetcode.com/problems/house-robber-ii/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Same as 0198, but the houses form a CIRCLE: house 0 and house n-1
 *   are adjacent, so robbing both is forbidden.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The ONLY new constraint is the pair (0, n-1). A feasible plan can
 *   never contain both houses, so the optimum is the better of:
 *       • rob houses 0..n-2 (exclude the last)   → linear problem
 *       • rob houses 1..n-1 (exclude the first)  → linear problem
 *   Both cases are the plain 0198 recurrence on a LINE → decompose the
 *   circle into two lines and reuse the linear solver.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Two linear passes with rolling variables (BEST)
 *   ans = max( robLine(nums[0..n-2]), robLine(nums[1..n-1]) )
 *   robLine = the 0198 recurrence dp[i] = max(dp[i-1], nums[i]+dp[i-2])
 *             collapsed to two rolling variables.
 *   State space : two independent 1D runs, each O(n) states, O(1)
 *                 rolling space per run.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Two passes with FULL dp tables (contrast)
 *   Identical split, but each run materialises the full dp[] array so
 *   the recurrence→array mapping is visible cell by cell.
 *   Trade-off : same O(n) time, O(n) space — shows WHY rolling
 *               variables exist: dp[i] only reads i-1 and i-2, so the
 *               table is over-allocated once those slides are seen.
 *   Time  Complexity : O(n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the split is exact (not an approximation)
 *   Any optimal plan is a set of houses with no adjacency. If it does
 *   not use house n-1 it is a valid plan on 0..n-2 → captured by case
 *   A. If it does not use house 0 it is valid on 1..n-1 → case B.
 *   Every plan misses at least ONE of the two neighbours (n-1 or 0)
 *   because the plan can contain neither... except when it contains
 *   neither, in which case it is contained in BOTH cases. So
 *   max(caseA, caseB) covers every feasible plan exactly.
 *   State-space math: 2 × O(n) states, O(1) combine → O(n) total.
 *   Real life : ring topologies (token rings, round-robin scheduling
 *   on circular corridors), any 0198 variant with wraparound edges.
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
 * APPROACH 1 : split the circle into two lines, rolling variables
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Maximise loot on a CIRCLE of houses (0 adjacent to n-1).
     * Inputs  : nums — cash in each house.
     * Output  : int — maximum total loot.
     */
    int rob(const std::vector<int>& nums) {
        const int n = static_cast<int>(nums.size());
        if (n == 1) {
            return nums[0];  // a single house: no circle to worry about
        }
        // Case A: houses 0..n-2 (last excluded) — first is allowed.
        // Case B: houses 1..n-1 (first excluded) — last is allowed.
        return std::max(robLine(nums, 0, n - 1), robLine(nums, 1, n));
    }

private:
    /*
     * Purpose : Linear 0198 solver on nums[start, end) with rolling vars.
     * Inputs  : nums  — cash in each house.
     *           start — first index of the line.
     *           end   — one past the last index of the line.
     * Output  : int — max loot on that line.
     */
    static int robLine(const std::vector<int>& nums, int start, int end) {
        int prev2 = 0;  // dp[i-2]
        int prev1 = 0;  // dp[i-1]
        for (int i = start; i < end; ++i) {
            // cur = max(skip i, rob i + loot from i-2).
            const int cur = std::max(prev1, nums[i] + prev2);
            prev2 = prev1;  // slide the window right
            prev1 = cur;
        }
        return prev1;  // dp[end-1]
    }
};

/* =====================================================================
 * APPROACH 2 : same split, but with explicit full dp tables
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Maximise loot on a CIRCLE (full-table variant).
     * Inputs  : nums — cash in each house.
     * Output  : int — maximum total loot.
     */
    int rob(const std::vector<int>& nums) {
        const int n = static_cast<int>(nums.size());
        if (n == 1) {
            return nums[0];
        }
        // Materialise full dp tables — O(n) space per case.
        return std::max(robTable(nums, 0, n - 1), robTable(nums, 1, n));
    }

private:
    /*
     * Purpose : Linear solver that stores the whole dp array.
     * Inputs  : nums  — cash in each house.
     *           start — first index of the line.
     *           end   — one past the last index of the line.
     * Output  : int — max loot on that line.
     */
    static int robTable(const std::vector<int>& nums, int start, int end) {
        const int len = end - start;
        if (len <= 0) {
            return 0;
        }
        std::vector<int> dp(len, 0);
        dp[0] = nums[start];
        if (len > 1) {
            dp[1] = std::max(nums[start], nums[start + 1]);
        }
        for (int i = 2; i < len; ++i) {
            dp[i] = std::max(dp[i - 1], nums[start + i] + dp[i - 2]);
        }
        return dp[len - 1];
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (nums, expected loot). Both solutions must match.
    struct Test { std::vector<int> nums; int expected; };
    const std::vector<Test> tests = {
        {{2, 3, 2}, 3},     // rob first or last — middle alarms both neighbours
        {{1, 2, 3, 1}, 4},  // rob 1 + 3
        {{1}, 1}            // single house
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