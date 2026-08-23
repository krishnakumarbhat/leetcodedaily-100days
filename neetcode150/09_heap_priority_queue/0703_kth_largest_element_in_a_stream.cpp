/*
 * =====================================================================
 * LeetCode 703 : Kth Largest Element in a Stream                   (Easy)
 * https://leetcode.com/problems/kth-largest-element-in-a-stream/
 * Category   : Heap / Priority queue
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design a class that keeps adding integers to a stream and answers
 *   "what is the k-th largest element so far?" after each addition.
 * ---------------------------------------------------------------------
 * INTUITION
 *   We never need the full sorted stream — only the boundary of the
 *   top-k. A min-heap of size k maintains exactly that boundary: the
 *   top IS the k-th largest, and any new value smaller than it is
 *   irrelevant forever (it can never enter the top-k).
 * ---------------------------------------------------------------------
 * APPROACH 1 · Min-heap of size k (best)
 *   Constructor: heapify the first k elements. add(): push the value;
 *   if the heap grows past k, pop the smallest; return heap.top().
 * APPROACH 2 · Rebuild / sort-per-call (naive)
 *   Keep a plain vector; sort descending and take index k-1 on every
 *   add() — O(n log n) per query, shown for contrast.
 * ---------------------------------------------------------------------
 * DEEP DIVE · The invariant that makes it O(log k)
 *   Invariant: heap always contains the k largest values seen.
 *   - New value ≤ top → smaller than everything in the heap → cannot
 *     be in the top-k → skip (no work!).
 *   - New value > top → push it (O(log k)) and eject the old top.
 *   Total per add: O(log k). If the stream is huge and k small, this
 *   is dramatically cheaper than any full-sort approach.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(log k) per add() ; O(k) construction.
 * MEMORY COMPLEXITY: O(k) heap storage.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <queue>
#include <functional>    // std::greater
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::priority_queue<int, std::vector<int>, std::greater<int>> heap_;
    int k_;
public:
    explicit Solution_1(int k, std::vector<int>& nums) : k_(k) {
        for (int x : nums) add(x);            // reuse the same add() path
    }
    int add(int val) {
        heap_.push(val);
        if (heap_.size() > static_cast<size_t>(k_)) heap_.pop();  // eject smallest
        return heap_.top();                   // k-th largest = top of top-k
    }
};

class Solution_2 {
    std::vector<int> data_;
    int k_;
public:
    explicit Solution_2(int k, std::vector<int>& nums) : k_(k), data_(nums) {}
    int add(int val) {
        data_.push_back(val);
        std::sort(data_.begin(), data_.end(), std::greater<int>());  // desc
        return data_[k_ - 1];                 // k-th largest directly
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    std::vector<int> init = {4, 5, 8, 2};
    struct Case { int val; int expect; };
    const Case cases[] = {{3, 4}, {5, 5}, {10, 5}, {9, 8}, {4, 8}};
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    {
        std::vector<int> i1 = init, i2 = init;
        Solution_1 s1(3, i1);
        Solution_2 s2(3, i2);
        for (const auto& c : cases) {
            int r1 = s1.add(c.val);
            int r2 = s2.add(c.val);
            bool ok = r1 == c.expect && r2 == c.expect;
            allOk = allOk && ok;
            std::cout << "add(" << c.val << ") → A1=" << r1 << " A2=" << r2
                      << " (want " << c.expect << ") " << (ok ? "PASS" : "FAIL") << "\n";
        }
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all adds" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
