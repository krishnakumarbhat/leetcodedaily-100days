/*
 * =====================================================================
 * LeetCode 42 : Trapping Rain Water                                 (Hard)
 * https://leetcode.com/problems/trapping-rain-water/
 * Category   : Two Pointers
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an elevation map height[i] (bar width = 1), compute how
 *   much water it can trap after a rain. Water pools above a bar only
 *   when both a taller bar to its LEFT and a taller bar to its RIGHT
 *   exist; it cannot spill past the lower of those two.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The water sitting ON TOP of bar i is fully determined by the two
 *   "walls" that trap it:
 *       water[i] = max(0, min(maxLeft[i], maxRight[i]) - height[i])
 *   where maxLeft[i]  = tallest bar strictly in [0 .. i-1] region
 *         maxRight[i] = tallest bar strictly in [i+1 .. n-1] region
 *   Every algorithm for this problem is a way of computing those two
 *   max-arrays (or the running maxima) and summing the per-bar units.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Prefix/suffix max arrays (intuitive, O(n) space)
 *   Pass 1: leftMax[i]  = max(height[0..i])   — build left to right.
 *   Pass 2: rightMax[i] = max(height[i..n-1]) — build right to left.
 *   Pass 3: water[i] = min(leftMax[i], rightMax[i]) - height[i] ≥ 0.
 *   Sum the non-negative values. Three linear passes, dead simple.
 *   Time  Complexity : O(n)  — three passes over n bars.
 *   Space Complexity : O(n)  — two max-array copies.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Two pointers (BEST, O(1) space)
 *   Maintain l = 0, r = n-1 plus two running maxima: lMax (tallest
 *   seen on the left side) and rMax (tallest seen on the right side).
 *   Invariant: if lMax <= rMax, bar l is NOT contained by anything on
 *   the right taller than rMax, so the true min(maxLeft, maxRight)
 *   for bar l equals lMax — we can compute water[l] RIGHT NOW and
 *   advance l. Symmetric for r. Each bar is finalized exactly once.
 *   Time  Complexity : O(n)  — each bar processed once, l and r meet.
 *   Space Complexity : O(1)  — two indices + two running maxima.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the pointer trick needs NO right-array
 *   When lMax <= rMax, bar l's right constraint can never be below
 *   lMax (rMax already exceeds it), and its left constraint IS lMax —
 *   so min(maxLeft, maxRight) = lMax deterministically. The same
 *   argument inverts at r. The smaller of the two running maxima is
 *   always "finalized" — that is the invariant that compresses the
 *   two O(n) arrays of Approach 1 into two O(1) integers.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing PASS/FAIL + benchmarks
#include <vector>        // std::vector — holds the elevation map
#include <algorithm>     // std::max / std::min — running maxima, water
#include <numeric>       // std::accumulate — sanity-sum of heights
#include <chrono>        // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Prefix/suffix max arrays
 * ===================================================================== */
class Solution_PrefixSuffix {
public:
    /*
     * Purpose : Return total trapped water using left/right max arrays.
     * Inputs  : height — elevation map; height[i] is bar height at i.
     * Output  : int — total water units trapped between the bars.
     */
    int trap(const std::vector<int>& height) {
        int n = static_cast<int>(height.size());
        if (n == 0) {
            return 0;
        }

        // leftMax[i] = tallest bar at or left of i — the left wall.
        std::vector<int> leftMax(n);
        leftMax[0] = height[0];
        for (int i = 1; i < n; ++i) {
            leftMax[i] = std::max(leftMax[i - 1], height[i]);
        }

        // rightMax[i] = tallest bar at or right of i — the right wall.
        std::vector<int> rightMax(n);
        rightMax[n - 1] = height[n - 1];
        for (int i = n - 2; i >= 0; --i) {
            rightMax[i] = std::max(rightMax[i + 1], height[i]);
        }

        // Water on bar i is capped by the LOWER of its two walls.
        // max(0, ...) guards dips where the bar itself is the tallest.
        int total = 0;
        for (int i = 0; i < n; ++i) {
            total += std::max(0, std::min(leftMax[i], rightMax[i]) - height[i]);
        }
        return total;
    }
};

/* =====================================================================
 * APPROACH 2 : Two pointers with running maxima (BEST)
 * ===================================================================== */
class Solution_TwoPointers {
public:
    /*
     * Purpose : Return total trapped water in O(1) extra space.
     * Inputs  : height — elevation map; height[i] is bar height at i.
     * Output  : int — total water units trapped between the bars.
     */
    int trap(const std::vector<int>& height) {
        int n = static_cast<int>(height.size());
        if (n == 0) {
            return 0;
        }

        int l = 0, r = n - 1;
        int lMax = 0, rMax = 0;
        int total = 0;

        // Invariant: the pointer whose RUNNING MAX is smaller gets its
        // bar finalized — its true cap is known without any right array.
        while (l < r) {
            if (height[l] < height[r]) {
                // Right side is strictly taller → the LEFT bar is the
                // binding side. If lMax already ≥ height[l], water pools;
                // otherwise lMax rises (bar l becomes a wall itself).
                if (height[l] >= lMax) {
                    lMax = height[l];
                } else {
                    total += lMax - height[l];
                }
                ++l;
            } else {
                // Symmetric: right bar is binding → finalize bar r.
                if (height[r] >= rMax) {
                    rMax = height[r];
                } else {
                    total += rMax - height[r];
                }
                --r;
            }
        }
        return total;
    }
};

/* =====================================================================
 * BENCHMARK — verify both solutions on real test cases + time/RAM
 * ===================================================================== */
int main() {
    // Case 1: official example → 6. Case 2: bowl with walls at edges.
    // Case 3: monotonic rise/fall → ZERO water (no basin anywhere).
    struct TestCase { std::vector<int> height; int expected; };
    std::vector<TestCase> tests = {
        {{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}, 6},
        {{4, 2, 0, 3, 2, 5}, 9},
        {{1, 2, 3, 4, 3, 2, 1}, 0}
    };

    // Aggregate time + peak-RAM across all cases, per approach.
    long time_us[2] = {0, 0};
    long peak_kb[2] = {0, 0};
    bool allPass = true;

    for (size_t t = 0; t < tests.size(); ++t) {
        struct rusage before, after;
        int r1, r2;

        // --- Approach 1: time + peak memory (ru_maxrss is KB on Linux) ---
        getrusage(RUSAGE_SELF, &before);
        auto s1 = std::chrono::steady_clock::now();
        r1 = Solution_PrefixSuffix().trap(tests[t].height);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        time_us[0] += std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000;
        peak_kb[0] = std::max(peak_kb[0], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        // --- Approach 2: same instrumentation ---
        getrusage(RUSAGE_SELF, &before);
        auto s2 = std::chrono::steady_clock::now();
        r2 = Solution_TwoPointers().trap(tests[t].height);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        time_us[1] += std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000;
        peak_kb[1] = std::max(peak_kb[1], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        bool ok = (r1 == tests[t].expected) && (r2 == tests[t].expected);
        allPass = allPass && ok;
        std::cout << "Test " << (t + 1) << ": prefixSuffix=" << r1 << " twoPtr=" << r2
                  << " expected=" << tests[t].expected
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "---\n"
              << "Approach 1 (prefix/suffix max) : " << time_us[0] << " µs total, peak " << peak_kb[0] << " KB\n"
              << "Approach 2 (two pointers)      : " << time_us[1] << " µs total, peak " << peak_kb[1] << " KB\n"
              << (allPass ? "PASS : all cases" : "FAIL : at least one case") << "\n";
    return allPass ? 0 : 1;
}
