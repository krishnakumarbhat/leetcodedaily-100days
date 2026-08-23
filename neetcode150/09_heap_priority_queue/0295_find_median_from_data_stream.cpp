/*
 * =====================================================================
 * LeetCode 295 : Find Median from Data Stream                     (Hard)
 * https://leetcode.com/problems/find-median-from-data-stream/
 * Category   : Heap / Priority queue
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design a class that supports addNum(int) in any order, and
 *   findMedian() that returns the median of ALL numbers added so far.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The median splits the data into two halves. Keep the LOWER half in
 *   a max-heap and the UPPER half in a min-heap, balanced so the two
 *   tops give the median instantly: even count → average of the two
 *   tops; odd count → the top of the larger heap.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Two heaps — max-heap + min-heap (best)
 *   1. addNum: push into max-heap (lower), then fix order: if lower's
 *      top > upper's top, swap the two tops. Rebalance size so the
 *      halves differ by at most one element.
 *   2. findMedian: size equal → average of both tops; else the top of
 *      the bigger heap.
 * APPROACH 2 · Sorted vector + binary search insert (naive)
 *   Keep the data sorted; insert with lower_bound → O(n) shift per add.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why this is the classic streaming-median trick
 *   Any algorithm that keeps the whole array sorted pays O(n) per
 *   insertion. Heaps give O(log n). The invariant "max(lower) ≤
 *   min(upper)" is preserved by pushing every new value into the lower
 *   half first, then correcting: if max(lower) > min(upper), swap the
 *   tops. Balancing after that keeps heights within 1, so the median
 *   always sits at the boundary of the two halves.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(log n) per addNum ; O(1) findMedian.
 * MEMORY COMPLEXITY: O(n) across both heaps.
 * =====================================================================
 */
#include <iostream>
#include <queue>
#include <vector>
#include <functional>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::priority_queue<int> lower_;                       // max-heap
    std::priority_queue<int, std::vector<int>, std::greater<int>> upper_; // min-heap
public:
    void addNum(int num) {
        lower_.push(num);                                  // tentatively to lower
        upper_.push(lower_.top());                         // hand the largest over
        lower_.pop();
        if (upper_.size() > lower_.size()) {               // rebalance heights
            lower_.push(upper_.top());
            upper_.pop();
        }
    }
    double findMedian() {
        if (lower_.size() > upper_.size()) return lower_.top();
        return (lower_.top() + upper_.top()) / 2.0;
    }
};

class Solution_2 {
    std::vector<int> data_;
public:
    void addNum(int num) {
        auto it = std::lower_bound(data_.begin(), data_.end(), num);
        data_.insert(it, num);                             // O(n) shift
    }
    double findMedian() {
        size_t n = data_.size();
        if (n % 2) return data_[n / 2];
        return (data_[n / 2 - 1] + data_[n / 2]) / 2.0;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Step { int val; double expect; };
    const Step steps[] = {
        {1, 1.0}, {2, 1.5}, {3, 2.0}, {4, 2.5}, {5, 3.0}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    Solution_1 s1;
    Solution_2 s2;
    bool allOk = true;
    for (const auto& st : steps) {
        s1.addNum(st.val); s2.addNum(st.val);
        double r1 = s1.findMedian(), r2 = s2.findMedian();
        bool ok = r1 == st.expect && r2 == st.expect;
        allOk = allOk && ok;
        std::cout << "after " << st.val << " → A1=" << r1 << " A2=" << r2
                  << " (want " << st.expect << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all steps" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
