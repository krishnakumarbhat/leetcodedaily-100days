/*
 * =====================================================================
 * LeetCode 1046 : Last Stone Weight                                (Easy)
 * https://leetcode.com/problems/last-stone-weight/
 * Category   : Heap / Priority queue
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Smash the two heaviest stones each round: equal weights destroy
 *   both; unequal weights keep the difference. Repeat until 0 or 1
 *   stone remains; return the survivor (or 0).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every round needs the TWO LARGEST elements and produces a new
 *   element. A max-heap gives O(log n) extraction and insertion —
 *   much faster than re-sorting the vector each round.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Max-heap simulation (best)
 *   Push all weights into a max-heap. While ≥ 2 stones: pop the two
 *   biggest, smash, push the remainder if any.
 * APPROACH 2 · Repeated sort (naive)
 *   Sort descending, take the two first elements, re-insert — O(n²)
 *   overall. Shown as the baseline.
 * ---------------------------------------------------------------------
 * DEEP DIVE · What a heap actually saves
 *   n rounds × O(n) re-sort = O(n²). With a heap every operation is
 *   O(log n) → O(n log n) total. The heap stores the weights in a
 *   complete binary tree inside ONE contiguous array (children of
 *   index i at 2i, 2i+1) — so it also has great cache locality.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n log n) — n pushes + n/2 smashes.
 * MEMORY COMPLEXITY: O(n) heap storage.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>     // std::sort, std::greater
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int lastStoneWeight(std::vector<int>& stones) {
        std::priority_queue<int> heap(stones.begin(), stones.end());  // max-heap
        while (heap.size() > 1) {
            int a = heap.top(); heap.pop();   // heaviest
            int b = heap.top(); heap.pop();   // second heaviest
            if (a != b) heap.push(a - b);     // survivor of the smash
        }
        return heap.empty() ? 0 : heap.top(); // 0 if everything destroyed
    }
};

class Solution_2 {
public:
    int lastStoneWeight(std::vector<int>& stones) {
        while (stones.size() > 1) {
            std::sort(stones.begin(), stones.end(), std::greater<int>());
            int a = stones[0], b = stones[1];
            stones.erase(stones.begin(), stones.begin() + 2);
            if (a != b) stones.push_back(a - b);
        }
        return stones.empty() ? 0 : stones[0];
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<int> stones; int expect; };
    const Case cases[] = {
        {{2,7,4,1,8,1}, 1},
        {{1}, 1},
        {{1,1}, 0}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        std::vector<int> a = c.stones, b = c.stones;
        int r1 = Solution_1().lastStoneWeight(a);
        int r2 = Solution_2().lastStoneWeight(b);
        bool ok = r1 == c.expect && r2 == c.expect;
        allOk = allOk && ok;
        std::cout << "→ A1=" << r1 << " A2=" << r2 << " (want " << c.expect
                  << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
