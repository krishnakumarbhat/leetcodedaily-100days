/*
 * =====================================================================
 * LeetCode 215 : Kth Largest Element in an Array                    (Medium)
 * https://leetcode.com/problems/kth-largest-element-in-an-array/
 * Category   : Heap / Priority queue
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer array nums and an integer k, return the k-th
 *   largest element (1-indexed) without sorting the whole array.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Sorting gives O(n log n) but we only need ONE element. A min-heap
 *   of size k keeps the k LARGEST values seen so far — its top is the
 *   k-th largest. Alternatively quickselect partitions in O(n) average.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Min-heap of size k (best)
 *   Push every value; whenever the heap exceeds k, pop the smallest.
 *   After the sweep the heap holds the k largest values, top = answer.
 * APPROACH 2 · std::nth_element (quickselect in libstdc++)
 *   nth_element puts the n-k-th smallest exactly where it belongs.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why a MIN-heap and not a max-heap?
 *   Heap of size k: a max-heap can only answer "largest 1"; popping
 *   its root discards the largest and keeps... the wrong side. The
 *   min-heap keeps the SMALLEST of the k best — exactly the k-th
 *   largest. In C++ std::priority_queue is a max-heap by default, so
 *   we use std::greater<int> to flip it. Every push is O(log k);
 *   total O(n log k) — faster than O(n log n) sort when k < n.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n log k) — n pushes, each O(log k).
 * MEMORY COMPLEXITY: O(k)         — the heap holds at most k values.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <queue>
#include <functional>    // std::greater — min-heap comparator
#include <algorithm>     // std::nth_element
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int findKthLargest(std::vector<int>& nums, int k) {
        std::priority_queue<int, std::vector<int>, std::greater<int>> heap;
        for (int x : nums) {
            heap.push(x);                     // candidate for top-k
            if (heap.size() > static_cast<size_t>(k)) heap.pop();  // drop smallest
        }
        return heap.top();                    // k-th largest = min of top-k
    }
};

class Solution_2 {
public:
    int findKthLargest(std::vector<int>& nums, int k) {
        std::nth_element(nums.begin(), nums.begin() + nums.size() - k, nums.end());
        return nums[nums.size() - k];         // element at its sorted position
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<int> nums; int k; int expect; };
    const Case cases[] = {
        {{3,2,1,5,6,4}, 2, 5},
        {{3,2,3,1,2,4,5,5,6}, 4, 4},
        {{1}, 1, 1}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        std::vector<int> a = c.nums, b = c.nums;
        int r1 = Solution_1().findKthLargest(a, c.k);
        int r2 = Solution_2().findKthLargest(b, c.k);
        bool ok = r1 == c.expect && r2 == c.expect;
        allOk = allOk && ok;
        std::cout << "k=" << c.k << " → A1=" << r1 << " A2=" << r2
                  << " (want " << c.expect << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
