/*
 * =====================================================================
 * LeetCode 40  : Combination Sum II                                 (Medium)
 * https://leetcode.com/problems/combination-sum-ii/
 * Category   : Backtracking / duplicates
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Like Combination Sum but each candidate may be used AT MOST ONCE,
 *   and the input may contain duplicates. Return unique combos.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Sort + the Subsets-II skip rule: at a recursion level, use each
 *   DISTINCT value only once (first copy only), and never reuse an
 *   element twice (move index by 1 after choosing).
 * ---------------------------------------------------------------------
 * APPROACH 1 · Sorted DFS, skip-dups, j+1 (best)
 *   for j in i..n: if j > i && c[j] == c[j-1] continue; if c[j] > rem
 *   break (sorted!); take, recurse(j+1), backtrack.
 * APPROACH 2 · Frequency-map DFS
 *   Group values by count; branch per distinct value with 0..count
 *   copies — needs a count array but reads nicely.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Sort makes both rules trivial
 *   (1) "each element once" is just the j+1 jump; (2) "unique combos"
 *   is the skip-equal-neighbor prune — possible because sorting
 *   collects equal values adjacently. Note the BREAK vs CONTINUE
 *   distinction vs Combination Sum I: with sorted candidates, once
 *   c[j] > rem every later c is also too big, so break prunes harder.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(2^n) worst case.
 * MEMORY COMPLEXITY: O(n) recursion depth.
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
    void dfs(int i, int rem) {
        if (rem == 0) { out_.push_back(cur_); return; }
        for (size_t j = i; j < a_->size(); ++j) {
            if ((*a_)[j] > rem) break;                 // sorted → prune hard
            if (j > i && (*a_)[j] == (*a_)[j - 1]) continue;  // skip dup
            cur_.push_back((*a_)[j]);
            dfs(j + 1, rem - (*a_)[j]);                // j+1: use each once
            cur_.pop_back();
        }
    }
public:
    std::vector<std::vector<int>> combinationSum2(std::vector<int>& candidates, int target) {
        std::sort(candidates.begin(), candidates.end());
        a_ = &candidates;
        dfs(0, target);
        return out_;
    }
};

class Solution_2 {
    std::vector<std::vector<int>> out_;
    std::vector<int> cur_;
    std::vector<int>* a_;
    void dfs(int i, int rem) {
        if (rem == 0) { out_.push_back(cur_); return; }
        if (i >= static_cast<int>(a_->size()) || (*a_)[i] > rem) return;
        for (int take = i; take < static_cast<int>(a_->size()); ++take) {
            if (take > i && (*a_)[take] == (*a_)[take - 1]) continue;
            cur_.push_back((*a_)[take]);
            dfs(take + 1, rem - (*a_)[take]);
            cur_.pop_back();
        }
    }
public:
    std::vector<std::vector<int>> combinationSum2(std::vector<int>& candidates, int target) {
        std::sort(candidates.begin(), candidates.end());
        a_ = &candidates;
        dfs(0, target);
        return out_;
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
        {{10, 1, 2, 7, 6, 1, 5}, 8, 4},    // [[1,1,6],[1,2,5],[1,7],[2,6]]
        {{2, 5, 2, 1, 2}, 5, 2},           // [[1,2,2],[5]]
        {{1, 1, 1, 1}, 2, 1}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        std::vector<int> v = c.c;
        int r1 = static_cast<int>(Solution_1().combinationSum2(v, c.t).size());
        v = c.c;
        int r2 = static_cast<int>(Solution_2().combinationSum2(v, c.t).size());
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
