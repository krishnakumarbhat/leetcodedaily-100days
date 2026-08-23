/*
 * =====================================================================
 * LeetCode 46  : Permutations                                        (Medium)
 * https://leetcode.com/problems/permutations/
 * Category   : Backtracking
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Return ALL permutations of a distinct-integer array (n! results).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Build permutations slot by slot: at each level pick an unused
 *   element — the set of choices shrinks by one each step. A swap
 *   trick avoids an extra "used[]" array.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Swap-based DFS (best)
 *   dfs(pos): if pos == n, record. Else for j in pos..n-1: swap(pos,j),
 *   recurse(pos+1), swap back. The array itself carries the state.
 * APPROACH 2 · Used[] + fresh copy
 *   Classic: keep a used[] bitmap; append unused values to a running
 *   permutation; backtrack by popping and un-marking.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Swap vs used[] — same tree, different state encoding
 *   The swap version permutes IN PLACE: after fixing position pos, the
 *   "used" elements live left of pos — encoded by position, no extra
 *   memory. Each full permutation costs n swaps to unwind. The used[]
 *   version copies n elements per leaf (O(n) extra per permutation)
 *   but reads more naturally. Both enumerate exactly n! leaves; total
 *   work O(n · n!) because every leaf must be materialized.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n · n!).
 * MEMORY COMPLEXITY: O(n) — recursion depth (output not counted).
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::vector<std::vector<int>> out_;
    std::vector<int>* a_;
    int n_;
    void dfs(int pos) {
        if (pos == n_) { out_.push_back(*a_); return; }
        for (int j = pos; j < n_; ++j) {
            std::swap((*a_)[pos], (*a_)[j]);
            dfs(pos + 1);
            std::swap((*a_)[pos], (*a_)[j]);          // backtrack
        }
    }
public:
    std::vector<std::vector<int>> permute(std::vector<int>& nums) {
        a_ = &nums;
        n_ = static_cast<int>(nums.size());
        dfs(0);
        return out_;
    }
};

class Solution_2 {
    std::vector<std::vector<int>> out_;
    std::vector<int> cur_;
    std::vector<int>* a_;
    std::vector<bool> used_;
    void dfs() {
        if (cur_.size() == a_->size()) { out_.push_back(cur_); return; }
        for (size_t i = 0; i < a_->size(); ++i) {
            if (used_[i]) continue;
            used_[i] = true;
            cur_.push_back((*a_)[i]);
            dfs();
            cur_.pop_back();                          // backtrack
            used_[i] = false;
        }
    }
public:
    std::vector<std::vector<int>> permute(std::vector<int>& nums) {
        a_ = &nums;
        used_.assign(nums.size(), false);
        dfs();
        return out_;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    std::vector<int> nums = {1, 2, 3};
    const long mem0 = memKb();
    auto t0 = nowUs();
    auto r1 = Solution_1().permute(nums);
    nums = {1, 2, 3};
    auto r2 = Solution_2().permute(nums);
    auto t1 = nowUs();
    std::cout << "A1 size=" << r1.size() << " A2 size=" << r2.size()
              << " (want 6) " << (r1.size() == 6 && r2.size() == 6 ? "PASS" : "FAIL")
              << " | time: " << (t1 - t0) << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
