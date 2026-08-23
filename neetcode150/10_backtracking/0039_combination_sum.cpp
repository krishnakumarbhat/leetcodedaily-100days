/*
 * =====================================================================
 * LeetCode 39  : Combination Sum                                    (Medium)
 * https://leetcode.com/problems/combination-sum/
 * Category   : Backtracking
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given distinct candidate integers and a target, return ALL unique
 *   combinations where candidates sum to target. Each candidate may
 *   be used UNLIMITED times.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Classic knapsack-style DFS: at each step either take the current
 *   coin again, or move past it. Because numbers may repeat, the
 *   recursion stays on the SAME index after taking.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Backtracking with repeat (best)
 *   dfs(i, remaining): if remaining == 0 record. Loop j from i: skip
 *   candidates[j] > remaining; take it (remaining -= c[j]), recurse
 *   with the SAME j (unlimited use); pop and move on.
 * APPROACH 2 · DP counts (alternative view)
 *   dp[t] = list of combinations reaching sum t; append candidate to
 *   every dp[t - c]. Same result, more memory.
 * ---------------------------------------------------------------------
 * DEEP DIVE · The two recursion idioms for "unlimited repeats"
 *   (1) include-exclude: take (recurse same i) OR skip (recurse i+1).
 *   (2) bounded loop: for j in i..n: choose c[j], recurse(j) — the
 *   loop's "j+1" version forbids reuse; passing j (not j+1) allows it.
 *   Both terminate because target strictly decreases. Pruning
 *   (skip > remaining) converts the exponential worst case into a
 *   fast practical search on small targets.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n^(target/min)) worst case.
 * MEMORY COMPLEXITY: O(target / min_candidate) recursion depth.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::vector<std::vector<int>> out_;
    std::vector<int> cur_;
    std::vector<int>* a_;
    int target_;
    void dfs(int i, int rem) {
        if (rem == 0) { out_.push_back(cur_); return; }
        for (size_t j = i; j < a_->size(); ++j) {
            if ((*a_)[j] > rem) continue;             // prune
            cur_.push_back((*a_)[j]);
            dfs(j, rem - (*a_)[j]);                   // same j: unlimited use
            cur_.pop_back();                          // backtrack
        }
    }
public:
    std::vector<std::vector<int>> combinationSum(std::vector<int>& candidates, int target) {
        a_ = &candidates;
        target_ = target;
        dfs(0, target);
        return out_;
    }
};

class Solution_2 {
    // DP-style: dp[sum] = list of sorted combos reaching `sum`.
public:
    std::vector<std::vector<int>> combinationSum(std::vector<int>& candidates, int target) {
        std::vector<std::vector<std::vector<int>>> dp(target + 1);
        dp[0] = {{}};
        for (size_t i = 0; i < candidates.size(); ++i) {
            int c = candidates[i];
            for (int t = c; t <= target; ++t) {
                for (auto& combo : dp[t - c]) {
                    auto next = combo;
                    next.push_back(c);
                    dp[t].push_back(next);
                }
            }
        }
        return dp[target];
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<int> c; int t; int want; };
    const Case cases[] = {
        {{2, 3, 6, 7}, 7, 2},         // [[2,2,3],[7]]
        {{2, 3, 5}, 8, 3},            // [[2,2,2,2],[2,3,3],[3,5]]
        {{2}, 1, 0}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        std::vector<int> v = c.c;
        int r1 = static_cast<int>(Solution_1().combinationSum(v, c.t).size());
        v = c.c;
        int r2 = static_cast<int>(Solution_2().combinationSum(v, c.t).size());
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "target=" << c.t << " → A1=" << r1 << " A2=" << r2
                  << " (want " << c.want << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
