/*
 * =====================================================================
 * LeetCode 1899 : Merge Triplets to Form Target Triplet             (Medium)
 * https://leetcode.com/problems/merge-triplets-to-form-target-triplet/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Merge (component-wise MAX) any subset of triplets; can the result
 *   equal the target triplet exactly?
 * ---------------------------------------------------------------------
 * INTUITION
 *   A triplet is USEFUL only if no component exceeds the target (a
 *   component > target can never be reduced). Merging all useful
 *   triplets is optimal: max is monotone, and the union of maxima
 *   only helps.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Greedy filter + merge (best)
 *   1. Keep triplets with all three components ≤ target.
 *   2. Merge them; the running max equals target component-wise iff
 *      a solution exists.
 * APPROACH 2 · Coordinate tracking (equivalent, in-place)
 *   Track (a,b,c) as the best-so-far coordinate-wise maximum of the
 *   admissible triplets — identical math, less memory.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why "merge all useful" is optimal
 *   max(a,b) ≥ a and ≥ b: merging never destroys components. So if
 *   ANY subset can reach the target, the FULL set of admissible
 *   triplets reaches it too (it dominates every candidate subset
 *   coordinate-wise). Conversely, a triplet that exceeds the target
 *   in some coordinate poisons every merge containing it — it must be
 *   excluded entirely. This dichotomy (useful ⇔ admissible) makes the
 *   greedy trivially optimal: there is literally nothing to choose.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n) — single pass.
 * MEMORY COMPLEXITY: O(1) (A2) / O(n) (A1 storing the filter).
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    bool mergeTriplets(std::vector<std::vector<int>>& ts, std::vector<int>& target) {
        std::vector<std::vector<int>> ok;
        for (auto& t : ts)
            if (t[0] <= target[0] && t[1] <= target[1] && t[2] <= target[2])
                ok.push_back(t);
        std::vector<int> acc(3, 0);
        for (auto& t : ok)
            for (int i = 0; i < 3; ++i) acc[i] = std::max(acc[i], t[i]);
        return acc == target;
    }
};

class Solution_2 {
public:
    bool mergeTriplets(std::vector<std::vector<int>>& ts, std::vector<int>& target) {
        int a = 0, b = 0, c = 0;
        for (auto& t : ts)
            if (t[0] <= target[0] && t[1] <= target[1] && t[2] <= target[2]) {
                a = std::max(a, t[0]);
                b = std::max(b, t[1]);
                c = std::max(c, t[2]);
            }
        return a == target[0] && b == target[1] && c == target[2];
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<std::vector<int>> ts; std::vector<int> t; bool want; };
    const Case cases[] = {
        {{{2, 5, 3}, {1, 8, 4}, {1, 7, 5}}, {2, 7, 5}, true},
        {{{2, 3, 4}, {1, 2, 5}, {3, 2, 2}}, {2, 3, 5}, true},
        {{{1, 1, 1}}, {1, 1, 2}, false},
        {{{3, 5, 3}}, {3, 5, 3}, true}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        auto ts1 = c.ts, ts2 = c.ts;
        auto t1v = c.t, t2v = c.t;
        bool r1 = Solution_1().mergeTriplets(ts1, t1v);
        bool r2 = Solution_2().mergeTriplets(ts2, t2v);
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
