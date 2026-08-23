/*
 * =====================================================================
 * LeetCode 55 : Jump Game                                           (Medium)
 * https://leetcode.com/problems/jump-game/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   You start at index 0 of `nums`. From index i you can jump at most
 *   nums[i] steps FORWARD. Return true if you can reach the last
 *   index.
 * ---------------------------------------------------------------------
 * INTUITION
 *   We never need to know WHICH jumps to take — only how far we can
 *   get. Track a single scalar: the furthest reachable index. When
 *   the sweep pointer passes the reach, the array is not reachable.
 *   Greedy because a larger reach strictly dominates a smaller one:
 *   every target that a worse path reaches, our best path reaches too
 *   (exchange argument — swap in our reach for theirs at every step).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Greedy furthest-reach (BEST, O(1) space)
 *     reach = max(reach, i + nums[i])
 *     if i > reach → index i is unreachable → return false.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 *   WHY it is correct: reachable[i] is decided by the max over all
 *   j < i of (j + nums[j] >= i). The single number `reach` encodes
 *   exactly that max — it is a sufficient statistic. No DP table
 *   needed because "reachable" is monotone: positions ≤ reach are
 *   ALL reachable, so boundary checking is enough.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Dynamic programming O(n²) (shows why greedy wins)
 *   reachable[0] = true; for every reachable i, mark all of
 *   (i, i+nums[i]] as reachable.
 *   Time  Complexity : O(n²)   Space Complexity : O(n)
 *   Correct but wasteful: it re-derives the same frontier again and
 *   again. Greedy compresses the whole reachable frontier into ONE
 *   integer — the DP table's information is redundant because the
 *   frontier is a single interval [0, reach].
 * ---------------------------------------------------------------------
 * DEEP DIVE — why "furthest reach" greedy cannot fail
 *   Exchange argument: let O be an optimal (winning) path reaching
 *   the end, and let G be our greedy path. Claim: after k moves, the
 *   greedy position is ≥ the optimal position for EVERY k. Induction:
 *   greedy position g_k ≥ o_k, and our jump can reach g_k + nums[g_k]
 *   ≥ o_k + nums[o_k] ≥ o_{k+1}. So greedily we are always at least as
 *   far as any rival — hence we can always imitate and beat O. This
 *   monotone-domination structure is the signature of a safe greedy.
 * =====================================================================
 */

#include <iostream>       // std::cout — benchmark output
#include <vector>         // std::vector — input array
#include <string>         // std::string — PASS/FAIL messages
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RSS measurement

/* =====================================================================
 * APPROACH 1 : Greedy furthest-reach
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether the last index is reachable.
     * Inputs  : nums — vector of integers, nums[i] = max forward jump.
     * Output  : bool — true if index n-1 is reachable from index 0.
     */
    bool canJump(const std::vector<int>& nums) {
        // Invariant: `reach` = furthest index reachable so far.
        int reach = 0;

        // Sweep left to right; each index either extends the frontier
        // or is discovered unreachable (sweep pointer overtakes it).
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            if (i > reach) return false;       // cannot even land on i
            if (i + nums[i] > reach) {
                reach = i + nums[i];           // frontier grows rightwards
            }
            if (reach >= static_cast<int>(nums.size()) - 1) {
                return true;                   // last index covered — done
            }
        }
        return true;
    }
};

/* =====================================================================
 * APPROACH 2 : DP with a reachable[] frontier (O(n²), for contrast)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether the last index is reachable.
     * Inputs  : nums — vector of integers, nums[i] = max forward jump.
     * Output  : bool — true if index n-1 is reachable from index 0.
     */
    bool canJump(const std::vector<int>& nums) {
        // reachable[i] = "index i can be reached". Re-derives the same
        // interval frontier as the greedy, but stores n booleans.
        std::vector<bool> reachable(nums.size(), false);
        reachable[0] = true; // start cell is trivially reachable

        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            if (!reachable[i]) continue;       // dead cell — no propagation

            // Stamp every landing cell this jump offers as reachable.
            int limit = i + nums[i];
            if (limit >= static_cast<int>(nums.size())) limit = nums.size() - 1;
            for (int j = i + 1; j <= limit; ++j) {
                reachable[j] = true;
            }
        }
        return reachable.back();
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, time + peak RAM
 * ===================================================================== */
int main() {
    // Official examples + a tricky zero-gap case.
    const std::vector<std::vector<int> > tests = {
        { 2, 3, 1, 1, 4 },        // → true  (2→3→4)
        { 3, 2, 1, 0, 4 },        // → false (stuck at index 3)
        { 2, 0, 0 },              // → true  (2 lands exactly on the end)
        { 0, 1 }                  // → false (never leave index 0)
    };
    const std::vector<bool> expected = { true, false, true, false };

    auto run_all = [&](int which, bool (*solve)(const std::vector<int>&)) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto t0 = std::chrono::high_resolution_clock::now();

        bool ok = true;
        for (int t = 0; t < static_cast<int>(tests.size()); ++t) {
            if (solve(tests[t]) != expected[t]) ok = false;
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

    bool a1 = run_all(1, [](const std::vector<int>& v) { return Solution_1().canJump(v); });
    bool a2 = run_all(2, [](const std::vector<int>& v) { return Solution_2().canJump(v); });
    std::cout << (a1 && a2 ? "PASS : both approaches agree on every test case."
                           : "FAIL : at least one approach is wrong.") << "\n";
    return 0;
}
