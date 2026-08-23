/*
 * =====================================================================
 * LeetCode 84 : Largest Rectangle in Histogram                       (Hard)
 * https://leetcode.com/problems/largest-rectangle-in-histogram/
 * Category   : Stack (monotonic)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given `heights` (bar heights of a histogram, width 1 each), return
 *   the area of the largest rectangle that can be drawn inside the
 *   histogram — every rectangle must sit on the baseline and may span
 *   several consecutive bars, bounded by the shortest bar inside it.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every maximal rectangle is "anchored" by one bar h: it extends
 *   left and right exactly until it meets a bar SHORTER than h (the
 *   first bars outside the rectangle). If we knew, for every bar, the
 *   index of the nearest shorter bar on each side, the answer would be
 *   max over i of  heights[i] * (right_bound[i] − left_bound[i] − 1).
 *   A MONOTONIC STACK finds both bounds in one pass: while heights are
 *   ascending we cannot know the right bound; the moment a shorter bar
 *   appears, every taller bar above it gets its right bound resolved.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Monotonic increasing stack (BEST)
 *   Invariant: stack indices hold STRICTLY INCREASING heights. For
 *   each new bar h: pop every index whose height is > h. Each popped
 *   bar p has h as its first-shorter bar to the RIGHT; the new stack
 *   top is the first-shorter bar to its LEFT → width is resolved,
 *   area computed once, never again. A sentinel 0 at the end forces
 *   every bar to be popped exactly once.
 *   Time  Complexity : O(n)  — each index pushed and popped once.
 *   Space Complexity : O(n)  — the stack itself.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Brute force (contrast)
 *   For every pair (i, j) of bars, the best rectangle spanning them
 *   has height min(heights[i..j]); take the max over all pairs.
 *   Correct but quadratic — every pair inspected, no structure used.
 *   Time  Complexity : O(n²)  Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — the monotonic stack invariant
 *   A monotonic stack keeps its elements in sorted order — ascending
 *   here. It is the canonical tool for "nearest smaller/greater
 *   neighbour" problems (0084, 0739, 0853 all use it). The invariant
 *   is re-established on every push: pop WHILE the top violates order,
 *   then push. Each element pays O(1) amortized (one push, one pop),
 *   so the whole sweep is linear — this is the pattern's power.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing test + benchmark output
#include <vector>       // std::vector — the heights array
#include <stack>        // std::stack — the monotonic stack of indices
#include <algorithm>    // std::max — area tracking
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Monotonic increasing stack
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Largest rectangle area under the histogram.
     * Inputs  : heights — bar heights, each bar has width 1.
     * Output  : the maximum area of any axis-aligned rectangle.
     */
    int largestRectangleArea(const std::vector<int>& heights) {
        std::stack<int> st;      // indices; heights[st] strictly increasing
        int best = 0;

        // Sentinel height 0 appended: strictly shorter than every bar,
        // so it resolves (pops) every remaining rectangle at the end.
        std::vector<int> h = heights;
        h.push_back(0);

        for (int i = 0; i < static_cast<int>(h.size()); ++i) {

            // While the new bar is SHORTER than the stack-top bar, the
            // top bar's rectangle is complete: h[i] is its first
            // shorter neighbour on the right.
            while (!st.empty() && h[st.top()] > h[i]) {

                // height of the rectangle = the popped bar itself.
                int height = h[st.top()];
                st.pop();

                // width: right bound = i, left bound = new stack top
                // (empty stack → the bar stretched to index 0).
                int width = st.empty() ? i : i - st.top() - 1;

                // Candidate area; keep the global maximum.
                best = std::max(best, height * width);
            }

            // Invariant restored → this bar's own bound is unresolved,
            // so it enters the stack to be resolved by a future bar.
            st.push(i);
        }

        return best;
    }
};

/* =====================================================================
 * APPROACH 2 : Brute force over all pairs (contrast)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Largest rectangle area under the histogram.
     * Inputs  : heights — bar heights, each bar has width 1.
     * Output  : the maximum area of any axis-aligned rectangle.
     */
    int largestRectangleArea(const std::vector<int>& heights) {
        int n = static_cast<int>(heights.size());
        int best = 0;

        // Every rectangle is determined by its left edge i and right
        // edge j; its height is the minimum bar in between.
        for (int i = 0; i < n; ++i) {
            int min_h = heights[i];

            // Extend the right edge: width grows, height can only fall.
            for (int j = i; j < n; ++j) {
                min_h = std::min(min_h, heights[j]);  // shrink bound
                best = std::max(best, min_h * (j - i + 1));
            }
        }

        return best;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // --- Correctness tests (2-3 cases per solution) ---
    struct Test { std::vector<int> h; int expect; };
    Test tests[] = {
        {{2, 1, 5, 6, 2, 3}, 10},   // official example → 10
        {{2, 4},             4},    // two bars, tallest alone wins
        {{2, 1, 2},          3},    // valley forces width-2 rectangle
        {{},                 0},    // empty histogram
        {{5},                5}     // single bar
    };

    bool all_ok = true;
    for (const Test& t : tests) {
        int r1 = Solution_1().largestRectangleArea(t.h);
        int r2 = Solution_2().largestRectangleArea(t.h);
        if (r1 != t.expect || r2 != t.expect) all_ok = false;
        std::cout << (r1 == t.expect && r2 == t.expect ? "PASS" : "FAIL")
                  << " : histogram size " << t.h.size()
                  << "  monotonic=" << r1 << "  brute=" << r2
                  << "  expect=" << t.expect << "\n";
    }

    // --- Benchmark: worst-case monotonic ramp forces max pops ---
    // Values 30000..1 keep every product ≤ 2.25e8 < INT_MAX.
    std::vector<int> big;
    for (int i = 0; i < 30000; ++i) big.push_back(30000 - i);

    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    int r1 = Solution_1().largestRectangleArea(big);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB delta

    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    int r2 = Solution_2().largestRectangleArea(big);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (monotonic stack) : " << r1
              << "  time = " << us_1 << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (brute force)     : " << r2
              << "  time = " << us_2 << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (all_ok ? "PASS : all tests" : "FAIL : a test was wrong")
              << "\n";
    return all_ok ? 0 : 1;
}
