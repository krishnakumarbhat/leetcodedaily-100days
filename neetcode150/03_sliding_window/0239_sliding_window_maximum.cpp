/*
 * =====================================================================
 * LeetCode 239 : Sliding Window Maximum                         (Hard)
 * https://leetcode.com/problems/sliding-window-maximum/
 * Category   : Sliding Window
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given `nums` and window size `k`, return an array holding the
 *   maximum of EVERY contiguous window of length k. Windows start
 *   at index 0, 1, ..., n−k.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A max-heap gives the max in O(log n) per op; a monotonic deque
 *   gives it in O(1) amortized. The deque keeps candidate maxima
 *   with TWO invariants: (1) indices strictly increasing along the
 *   deque, (2) values strictly DECREASING. The front is therefore
 *   the window's maximum, and anything smaller than the newcomer
 *   can never become a maximum again → safe to discard forever.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Monotonic deque (BEST)
 *   For each i: pop front while it falls outside the window, pop
 *   back while values ≤ nums[i] (they are dominated), push i, and
 *   once the window is full record nums[front].
 *   Time  Complexity : O(n)  — each index pushed/popped once
 *   Space Complexity : O(k)  — deque never holds > k indices
 * ---------------------------------------------------------------------
 * APPROACH 2 — Max-heap with lazy deletion
 *   Push (−value, index) pairs (max-heap via negation). The root is
 *   the global max; before reading it, lazily pop roots that have
 *   slid out of the window (index ≤ i − k). Stale roots are removed
 *   only when they reach the top → O(log n) per push + popped work.
 *   Time  Complexity : O(n log n) — each push/pop is O(log n)
 *   Space Complexity : O(n)      — heap accumulates stale entries
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — deque vs heap
 *   std::deque (C++): a sequence of fixed-size blocks, O(1) push/pop
 *   on BOTH ends — this is exactly what the monotonic queue needs.
 *   Python collections.deque: doubly-linked blocks, same O(1) ends.
 *   std::priority_queue: a heap — the root is always the max, but
 *   removal of ARBITRARY (stale) elements costs O(k) → hence lazy
 *   deletion, deferring cleanup until the stale root actually blocks
 *   the answer. The monotonic-deque trick removes the waste: each
 *   element is compared to its back neighbours and discarded exactly
 *   once, which is what turns O(n log n) into O(n).
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — nums and the answer
#include <deque>          // std::deque — monotonic queue of indices
#include <queue>          // std::priority_queue — lazy-deletion heap
#include <utility>        // std::pair — (value, index) heap entries
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement (KB)

/* =====================================================================
 * APPROACH 1 : Monotonic deque of indices (O(n))
 * ===================================================================== */
class Solution_MonotonicDeque {
public:
    /*
     * Purpose : Return the maximum of every length-k window of `nums`.
     * Inputs  : nums — the array to slide over.
     *           k    — window size (1 ≤ k ≤ n).
     * Output  : std::vector<int> of size n−k+1 with window maxima.
     */
    std::vector<int> maxSlidingWindow(const std::vector<int>& nums, int k) {
        // dq : INDICES, front→back = increasing index, decreasing value.
        // Front is always the current window's maximum.
        std::deque<int> dq;
        std::vector<int> result;
        result.reserve(nums.size() - k + 1);

        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            // Invariant 1: drop indices that slid out of the window.
            // Window is [i−k+1 .. i], so front must satisfy ≥ i−k+1.
            while (!dq.empty() && dq.front() < i - k + 1) {
                dq.pop_front();
            }
            // Invariant 2: while the back value is ≤ nums[i], that
            // back index is dominated — nums[i] is newer AND bigger,
            // so it will outlive it as the window's max. Pop forever.
            while (!dq.empty() && nums[dq.back()] <= nums[i]) {
                dq.pop_back();
            }
            // nums[i] enters as the new (potential) maximum tail.
            dq.push_back(i);
            // Window complete? Then the front is its maximum.
            if (i >= k - 1) {
                result.push_back(nums[dq.front()]);
            }
        }
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : Max-heap with lazy deletion (O(n log n))
 * ===================================================================== */
class Solution_MaxHeapLazy {
public:
    /*
     * Purpose : Return the maximum of every length-k window of `nums`.
     * Inputs  : nums — the array to slide over.
     *           k    — window size (1 ≤ k ≤ n).
     * Output  : std::vector<int> of size n−k+1 with window maxima.
     */
    std::vector<int> maxSlidingWindow(const std::vector<int>& nums, int k) {
        // heap : max-heap of (−value, index). Negation emulates a
        // max-heap with the default (min-)priority_queue comparator.
        std::priority_queue<std::pair<int, int>> heap;
        std::vector<int> result;
        result.reserve(nums.size() - k + 1);

        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            // Every newcomer enters the heap; it may be the answer.
            heap.push({nums[i], i});

            // Window [i−k+1 .. i] is complete → record its maximum.
            if (i >= k - 1) {
                // Lazy deletion: the root might be a stale index that
                // already slid out of the window — evict until the
                // root is one we can still legally use.
                while (!heap.empty() && heap.top().second <= i - k) {
                    heap.pop();
                }
                // Root = largest value among live indices in-window.
                result.push_back(heap.top().first);
            }
        }
        return result;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests + a longer series,
 * compare time and peak RAM, print PASS/FAIL per case.
 * ===================================================================== */
int main() {
    const std::vector<std::pair<std::vector<int>, int>> tests = {
        {{1, 3, -1, -3, 5, 3, 6, 7}, 3},  // official: [3,3,5,5,6,7]
        {{1}, 1},                          // single element, k=1
        {{9, 8, 7, 6}, 2}                  // decreasing series: [9,8,7]
    };
    // Expected answers for the three tests above.
    const std::vector<std::vector<int>> expected = {
        {3, 3, 5, 5, 6, 7}, {1}, {9, 8, 7}
    };

    bool allPass = true;
    for (size_t t = 0; t < tests.size(); ++t) {
        const auto r1 = Solution_MonotonicDeque().maxSlidingWindow(tests[t].first, tests[t].second);
        const auto r2 = Solution_MaxHeapLazy().maxSlidingWindow(tests[t].first, tests[t].second);
        const bool ok = r1 == expected[t] && r2 == expected[t];
        allPass = allPass && ok;
        std::cout << (ok ? "PASS " : "FAIL ") << "test#" << t + 1 << " k=" << tests[t].second << "  deque=[";
        for (size_t i = 0; i < r1.size(); ++i) {
            std::cout << r1[i] << (i + 1 < r1.size() ? "," : "");
        }
        std::cout << "]  heap=[";
        for (size_t i = 0; i < r2.size(); ++i) {
            std::cout << r2[i] << (i + 1 < r2.size() ? "," : "");
        }
        std::cout << "]\n";
    }

    // Longer zig-zag series so both data structures do real work.
    std::vector<int> bench;
    for (int i = 0; i < 20000; ++i) {
        bench.push_back((i * 37) % 1000);
    }

    // --- Approach 1 timing ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    const auto b1 = Solution_MonotonicDeque().maxSlidingWindow(bench, 100);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    const double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    const long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss; // KB on Linux

    // --- Approach 2 timing ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    const auto b2 = Solution_MaxHeapLazy().maxSlidingWindow(bench, 100);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    const double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    const long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (monotonic deque) : size=" << b1.size()
              << "  time=" << us_1 << " µs  peak-ram-delta=" << mem_1 << " KB\n";
    std::cout << "Approach 2 (max heap + lazy) : size=" << b2.size()
              << "  time=" << us_2 << " µs  peak-ram-delta=" << mem_2 << " KB\n";

    // Both approaches must produce identical maxima on the big series.
    allPass = allPass && (b1 == b2);
    std::cout << (allPass ? "PASS : all test cases and benchmark agree."
                          : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}