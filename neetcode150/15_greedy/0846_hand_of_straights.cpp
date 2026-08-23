/*
 * =====================================================================
 * LeetCode 846 : Hand of Straights                                  (Medium)
 * https://leetcode.com/problems/hand-of-straights/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Can the cards be rearranged into `groupSize`-long runs of
 *   CONSECUTIVE values? Each card used exactly once.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Greedy from the smallest remaining card: it MUST start a run (no
 *   smaller card can precede it). Consume it and the next
 *   groupSize-1 consecutive values; repeat. A multiset makes "smallest
 *   remaining" an O(log n) operation.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Sorted map (TreeMap) — best
 *   1. Count cards. While cards remain: take the smallest value v,
 *      and for k in v..v+groupSize-1 decrement; a missing/empty value
 *      kills the arrangement.
 * APPROACH 2 · Sort + greedy pointer scan
 *   Sort the array; walk runs in-place, skipping already-used cards.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why "smallest first" is forced, not a choice
 *   The smallest remaining card x cannot be the middle or end of a
 *   run (no x-1 exists among remaining cards — it was consumed by an
 *   earlier run or never existed). It must be the FIRST card of a
 *   run, and that run is fully determined: x..x+groupSize-1. So every
 *   greedy choice is forced — no branching, hence correctness is
 *   immediate and the algorithm is optimal by construction.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n log n) — n inserts + n removals.
 * MEMORY COMPLEXITY: O(n).
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    bool isNStraightHand(std::vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize) return false;
        std::map<int, int> cnt;
        for (int c : hand) ++cnt[c];
        while (!cnt.empty()) {
            int first = cnt.begin()->first;             // smallest remaining
            for (int k = 0; k < groupSize; ++k) {
                int v = first + k;
                auto it = cnt.find(v);
                if (it == cnt.end()) return false;      // run can't close
                if (--it->second == 0) cnt.erase(it);
            }
        }
        return true;
    }
};

class Solution_2 {
public:
    bool isNStraightHand(std::vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize) return false;
        std::sort(hand.begin(), hand.end());
        std::vector<bool> used(hand.size(), false);
        for (size_t i = 0; i < hand.size(); ++i) {
            if (used[i]) continue;
            int prev = hand[i], placed = 1;
            used[i] = true;
            for (size_t j = i + 1; j < hand.size() && placed < groupSize; ++j)
                if (!used[j] && hand[j] == prev + 1) {  // next consecutive
                    used[j] = true;
                    prev = hand[j];
                    ++placed;
                }
            if (placed < groupSize) return false;
        }
        return true;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<int> hand; int g; bool want; };
    const Case cases[] = {
        {{1, 2, 3, 6, 2, 3, 4, 7, 8}, 3, true},
        {{1, 2, 3, 4, 5}, 4, false},
        {{1, 2, 3, 4, 5, 6}, 2, true},
        {{8, 10, 12}, 3, false}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        auto h1 = c.hand, h2 = c.hand;
        bool r1 = Solution_1().isNStraightHand(h1, c.g);
        bool r2 = Solution_2().isNStraightHand(h2, c.g);
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "→ A1=" << (r1 ? "T" : "F") << " A2=" << (r2 ? "T" : "F")
                  << " (want " << (c.want ? "T" : "F") << ") "
                  << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
