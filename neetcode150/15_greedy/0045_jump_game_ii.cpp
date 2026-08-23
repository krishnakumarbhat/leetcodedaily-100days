/*
 * =====================================================================
 * LeetCode 45 : Jump Game II                                        (Medium)
 * https://leetcode.com/problems/jump-game-ii/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Start at index 0 of `nums`; from i you can jump at most nums[i]
 *   steps forward. Return the MINIMUM number of jumps to reach the
 *   last index. It is guaranteed the end is reachable.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Think in LAYERS (BFS on the implicit jump graph). Layer k = all
 *   positions reachable with exactly ≤ k jumps. The frontier of layer
 *   k is an interval [l, r]; one more jump from ANY cell inside it
 *   covers at most max(i + nums[i]) over the interval — the greedy
 *   jump is the one that maximizes that single value. Taking the
 *   furthest option per layer is optimal because the next layer's
 *   frontier is exactly (r, maxReach]: a shorter jump only lands
 *   inside [l, r] again (no progress) or covers less ground (worse
 *   frontier) — exchange argument.
 * ---------------------------------------------------------------------
 * APPROACH 1 — BFS-layered greedy (BEST, O(1) space)
 *     curEnd = right edge of the CURRENT layer; far = furthest any
 *     cell in this layer can reach. When i reaches curEnd the layer
 *     is exhausted → one jump consumed, curEnd = far.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 *   WHY correctness: layer k is an interval. Minimal jumps = number
 *   of layers until the interval contains the end — greedy maximizes
 *   each layer's right edge, so it minimizes the layer count.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Reverse greedy O(n²) (pick leftmost reachable)
 *   Work from the end backwards: repeatedly find the LEFTMOST index
 *   that can jump to the current target (greedy-leftmost is correct
 *   because landing further left can only leave more options open).
 *   Time  Complexity : O(n²)   Space Complexity : O(1)
 *   Correct but quadratic: the leftmost-reachable search re-scans the
 *   array once per jump. Forward BFS-layered does the same counting
 *   in a single sweep.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why per-layer furthest is the right greed
 *   Exchange argument: in layer k, every cell c in [l, r] is ≤ r, and
 *   its reach c + nums[c] ≤ maxReach (the greedy pick). So the greedy
 *   next-layer frontier [r, maxReach] CONTAINS the frontier any other
 *   choice would produce → any path the rival continues from, we can
 *   continue from too. Greedy layer count ≤ rival layer count, and
 *   since both are valid (≥ optimal), greedy is optimal. This is the
 *   same interval-frontier monotonicity as Jump Game I, upgraded to
 *   COUNTING layers.
 * =====================================================================
 */

#include <iostream>       // std::cout — benchmark output
#include <vector>         // std::vector — input array
#include <string>         // std::string — PASS/FAIL messages
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RSS measurement

/* =====================================================================
 * APPROACH 1 : BFS-layered greedy (furthest reach per layer)
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the minimum number of jumps to reach the end.
     * Inputs  : nums — vector of ints, nums[i] = max forward jump.
     * Output  : int — minimal jump count (end guaranteed reachable).
     */
    int jump(const std::vector<int>& nums) {
        int jumps = 0;  // layers consumed so far
        int curEnd = 0; // right edge of the CURRENT jump layer
        int far = 0;    // furthest cell the current layer can reach

        // We never need to process the last cell: being there means
        // we are already done (its jump value is irrelevant).
        for (int i = 0; i < static_cast<int>(nums.size()) - 1; ++i) {
            if (i + nums[i] > far) far = i + nums[i]; // widen next frontier

            if (i == curEnd) {
                ++jumps;      // current layer exhausted → must take a jump
                curEnd = far; // its frontier becomes the next layer
            }
        }
        return jumps;
    }
};

/* =====================================================================
 * APPROACH 2 : Reverse greedy — hop backwards to leftmost reachable
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the minimum number of jumps to reach the end.
     * Inputs  : nums — vector of ints, nums[i] = max forward jump.
     * Output  : int — minimal jump count (end guaranteed reachable).
     */
    int jump(const std::vector<int>& nums) {
        int jumps = 0;
        int pos = static_cast<int>(nums.size()) - 1; // target to reach

        // Each iteration places `pos` one jump closer to index 0.
        while (pos > 0) {
            // Leftmost index that can jump ONTO pos. Landing leftmost
            // is safest: it leaves the most future options open.
            for (int i = 0; i < pos; ++i) {
                if (i + nums[i] >= pos) {
                    pos = i;    // new target = the takeoff cell
                    ++jumps;
                    break;      // restart search from the new position
                }
            }
        }
        return jumps;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, time + peak RAM
 * ===================================================================== */
int main() {
    // Official examples + a pathological all-ones array (n-1 jumps).
    const std::vector<std::vector<int> > tests = {
        { 2, 3, 1, 1, 4 }, // → 2  (0→1→4)
        { 2, 3, 0, 1, 4 }, // → 2  (0→1→4)
        { 1, 1, 1, 1 },    // → 3  (walk one step each time)
        { 0 },             // → 0  (already at the end)
        { 1, 2, 3 }        // → 2  (0→1→2; direct 0→2 impossible, jump=1)
    };
    const std::vector<int> expected = { 2, 2, 3, 0, 2 };

    auto run_all = [&](int which, int (*solve)(const std::vector<int>&)) {
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

    bool a1 = run_all(1, [](const std::vector<int>& v) { return Solution_1().jump(v); });
    bool a2 = run_all(2, [](const std::vector<int>& v) { return Solution_2().jump(v); });
    std::cout << (a1 && a2 ? "PASS : both approaches return the minimal jump count."
                           : "FAIL : at least one approach is wrong.") << "\n";
    return 0;
}
