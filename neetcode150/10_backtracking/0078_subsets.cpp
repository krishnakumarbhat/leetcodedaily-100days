/*
 * =====================================================================
 * LeetCode 78  : Subsets                                             (Medium)
 * https://leetcode.com/problems/subsets/
 * Category   : Backtracking / bit manipulation
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Return ALL possible subsets (the power set) of a distinct-int
 *   array. Order of subsets does not matter.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every element is either IN a subset or OUT — the power set is the
 *   set of all 2^n binary choices. Two mechanical views: DFS that
 *   branches on "include/exclude", or counting from 0..2^n-1 where
 *   the bits of the counter select elements.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Backtracking include/exclude (best)
 *   DFS over index i: first recurse WITHOUT nums[i], then WITH.
 *   Every leaf of the recursion is one subset.
 * APPROACH 2 · Bitmask enumeration
 *   For mask in 0..(1<<n)-1, push nums[j] iff bit j of mask is set.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Where backtracking actually backtracks
 *   We append nums[i] to a shared vector, recurse, then pop — the
 *   pop IS the backtrack: it restores the state so the sibling branch
 *   starts from the same prefix. Total nodes = 2^(n+1) - 1; each leaf
 *   is materialized once, so time = O(n · 2^n) to also copy each set.
 *   Python builds a fresh list per recursion instead of mutating.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n · 2^n) — copy each of the 2^n subsets.
 * MEMORY COMPLEXITY: O(n) recursion depth (+ output storage).
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::vector<std::vector<int>> out_;
    std::vector<int> cur_;
    std::vector<int>* nums_;
    void dfs(int i) {
        if (i == static_cast<int>(nums_->size())) { out_.push_back(cur_); return; }
        dfs(i + 1);               // exclude nums[i]
        cur_.push_back((*nums_)[i]);
        dfs(i + 1);               // include nums[i]
        cur_.pop_back();          // THE backtrack
    }
public:
    std::vector<std::vector<int>> subsets(std::vector<int>& nums) {
        nums_ = &nums;
        dfs(0);
        return out_;
    }
};

class Solution_2 {
public:
    std::vector<std::vector<int>> subsets(std::vector<int>& nums) {
        std::vector<std::vector<int>> out;
        for (int mask = 0; mask < (1 << nums.size()); ++mask) {
            std::vector<int> cur;
            for (size_t j = 0; j < nums.size(); ++j)
                if (mask & (1 << j)) cur.push_back(nums[j]);
            out.push_back(cur);
        }
        return out;
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
    auto r1 = Solution_1().subsets(nums);
    auto r2 = Solution_2().subsets(nums);
    auto t1 = nowUs();
    std::cout << "A1 size=" << r1.size() << " A2 size=" << r2.size()
              << " (want 8) " << (r1.size() == 8 && r2.size() == 8 ? "PASS" : "FAIL")
              << " | time: " << (t1 - t0) << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
