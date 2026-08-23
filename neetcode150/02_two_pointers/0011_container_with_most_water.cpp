/*
 * =====================================================================
 * LeetCode 11 : Container With Most Water                           (Medium)
 * https://leetcode.com/problems/container-with-most-water/
 * Category   : Two Pointers
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array `height` where height[i] is the vertical wall at
 *   index i, find two walls that together with the x-axis enclose the
 *   LARGEST rectangle of water. Water cannot overflow the shorter wall:
 *       area(l, r) = min(height[l], height[r]) * (r - l)
 * ---------------------------------------------------------------------
 * INTUITION
 *   The area is a product of TWO factors: the width (r - l) and the
 *   limiting height min(h[l], h[r]). At every step we must sacrifice
 *   the factor that costs us the least — move the SHORTER wall inward.
 *   The shorter wall caps the area, so keeping it guarantees we never
 *   improve; moving it is the only move that CAN improve the next area.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Brute force (baseline, O(n²))
 *   Try EVERY pair of walls (i, j), compute the enclosed area with the
 *   formula above, and remember the maximum. Correct but wasteful:
 *   n² pairs, most of which are dominated by a taller wall somewhere.
 *   Time  Complexity : O(n²) — nested loops enumerate n(n-1)/2 pairs.
 *   Space Complexity : O(1) — only a running maximum is stored.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Two pointers (BEST, O(n))
 *   Start l = 0, r = n-1 (maximal width). Compute the area. Then move
 *   ONLY the shorter of the two walls inward:
 *     • If h[l] <= h[r], advancing l can only make area grow (the
 *       limiting height might rise) — advancing r can never beat this.
 *     • Else advance r.
 *   Both pointers meet after exactly n-1 moves → O(n) total areas.
 *   Time  Complexity : O(n)  — each wall is moved at most once.
 *   Space Complexity : O(1) — two indices + one maximum.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why moving the SHORTER wall is provably safe
 *   Fix l and r. If h[l] <= h[r], the best possible container that
 *   still uses l as its LEFT wall has height at most h[l] and width at
 *   most (r - l) — so it cannot beat the current area. Every r' < r
 *   yields area = min(h[l], h[r']) * (r' - l) <= h[l] * (r - l).
 *   Hence l can be discarded forever: this is the monotonicity argument
 *   that turns the O(n²) search into a single O(n) sweep. Each step
 *   we shrink the "candidate rectangle" of wall pairs by one column,
 *   and the answer is the maximum over the n-1 rectangles we measure.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing PASS/FAIL + benchmarks
#include <vector>        // std::vector — holds the wall heights
#include <algorithm>     // std::max — tracking the best area
#include <chrono>        // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Brute force — every pair of walls
 * ===================================================================== */
class Solution_BruteForce {
public:
    /*
     * Purpose : Return the max water area over ALL pairs of walls.
     * Inputs  : height — wall heights; height[i] is wall i.
     * Output  : int — the largest area min(h[i],h[j]) * (j-i).
     */
    int maxArea(const std::vector<int>& height) {
        int best = 0;
        // Enumerate every ordered pair (l, r) with r strictly right of l.
        for (int l = 0; l < static_cast<int>(height.size()); ++l) {
            for (int r = l + 1; r < static_cast<int>(height.size()); ++r) {
                // The shorter wall decides how high the water can rise.
                int area = std::min(height[l], height[r]) * (r - l);
                best = std::max(best, area);
            }
        }
        return best;
    }
};

/* =====================================================================
 * APPROACH 2 : Two pointers — shrink from the outside in (BEST)
 * ===================================================================== */
class Solution_TwoPointers {
public:
    /*
     * Purpose : Return the max water area using the O(n) two-pointer sweep.
     * Inputs  : height — wall heights; height[i] is wall i.
     * Output  : int — the largest area min(h[i],h[j]) * (j-i).
     */
    int maxArea(const std::vector<int>& height) {
        int l = 0;
        int r = static_cast<int>(height.size()) - 1;
        int best = 0;

        // The pointers converge; each iteration discards one candidate
        // wall, so at most n-1 areas are ever measured.
        while (l < r) {
            // Current width is the widest remaining; the short wall caps it.
            int area = std::min(height[l], height[r]) * (r - l);
            best = std::max(best, area);

            if (height[l] < height[r]) {
                // Left wall is the bottleneck: the right wall caps the
                // water, so ANY right-side partner with this left wall
                // fits ≤ h[l]*(r-l) — l is provably useless now, drop it.
                ++l;
            } else {
                // Right wall is the bottleneck (or tie) — drop it instead.
                // A tie is symmetric: moving either side cannot lose the
                // optimum since the equal wall still caps future areas.
                --r;
            }
        }
        return best;
    }
};

/* =====================================================================
 * BENCHMARK — verify both solutions on real test cases + time/RAM
 * ===================================================================== */
int main() {
    // Case 1: official example → 49. Case 2: monotonic rise → walls keep
    // growing, the answer is the pair (0, n-1). Case 3: short walls in the
    // middle — the two-pointer must jump over the middle plateau.
    struct TestCase { std::vector<int> height; int expected; };
    std::vector<TestCase> tests = {
        {{1, 8, 6, 2, 5, 4, 8, 3, 7}, 49},
        {{1, 2, 3, 4, 5, 6, 7, 8}, 16},
        {{4, 3, 1, 1, 1, 3, 4}, 24}
    };

    // Aggregate time + peak-RAM across all cases, per approach.
    // ru_maxrss reports in KILOBYTES on Linux; keep a long to match it.
    long time_us[2] = {0, 0};
    long peak_kb[2] = {0, 0};
    bool allPass = true;

    for (size_t t = 0; t < tests.size(); ++t) {
        struct rusage before, after;
        int r1, r2;

        // --- Approach 1: time + peak memory (ru_maxrss is KB on Linux) ---
        getrusage(RUSAGE_SELF, &before);
        auto s1 = std::chrono::steady_clock::now();
        r1 = Solution_BruteForce().maxArea(tests[t].height);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        // Steady clock never jumps (unlike wall clock); ns diff → µs.
        long us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000;
        time_us[0] += us1;
        peak_kb[0] = std::max(peak_kb[0], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        // --- Approach 2: same instrumentation ---
        getrusage(RUSAGE_SELF, &before);
        auto s2 = std::chrono::steady_clock::now();
        r2 = Solution_TwoPointers().maxArea(tests[t].height);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        long us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000;
        time_us[1] += us2;
        peak_kb[1] = std::max(peak_kb[1], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        // Verify BOTH approaches against the independently-computed answer.
        bool ok = (r1 == tests[t].expected) && (r2 == tests[t].expected);
        allPass = allPass && ok;
        std::cout << "Test " << (t + 1) << ": brute=" << r1 << " twoPtr=" << r2
                  << " expected=" << tests[t].expected
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "---\n"
              << "Approach 1 (brute force)  : " << time_us[0] << " µs total, peak " << peak_kb[0] << " KB\n"
              << "Approach 2 (two pointers) : " << time_us[1] << " µs total, peak " << peak_kb[1] << " KB\n"
              << (allPass ? "PASS : all cases" : "FAIL : at least one case") << "\n";
    return allPass ? 0 : 1;
}
