/*
 * =====================================================================
 * LeetCode 90  : Subsets II                                          (Medium)
 * https://leetcode.com/problems/subsets-ii/
 * Category   : Backtracking / duplicates handling
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Like Subsets, but nums may contain DUPLICATES. Return all unique
 *   subsets (no duplicate subsets).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Sort first, then at each recursion level skip repeated values:
 *   equal numbers produce identical subtrees, so only the FIRST copy
 *   may start new branches.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Backtracking with skip-duplicates (best)
 *   Sort nums. Standard power-set DFS; after choosing nums[i], while
 *   nums[i+1] == nums[i] skip i+1 (they'd duplicate every subset).
 * APPROACH 2 · Set of bitmask tuples (brute)
 *   Enumerate all 2^n masks, build tuples, insert into a set, dump.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why "skip after use" is correct
 *   Duplicates cause DOUBLE counting exactly when the same value is
 *   used as the FIRST element of a subset. Rule: at a decision level,
 *   take a value v at most once — loop over DISTINCT candidates
 *   {for j = i; j < n && nums[j] == v; ...}. Equivalent popular form:
 *   recurse(i, path) with "for j in i..n: choose nums[j], recurse(j+1)"
 *   plus skipping equal neighbors. Both yield exactly one subset per
 *   distinct choice sequence; total subsets shrink to 2^d (d distinct).
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(2^n) worst case (all distinct).
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
    std::vector<int>* nums_;
    void dfs(int i) {
        out_.push_back(cur_);                         // every node is a subset
        for (size_t j = i; j < nums_->size(); ++j) {
            if (j > i && (*nums_)[j] == (*nums_)[j - 1]) continue;  // skip dup
            cur_.push_back((*nums_)[j]);
            dfs(j + 1);
            cur_.pop_back();
        }
    }
public:
    std::vector<std::vector<int>> subsetsWithDup(std::vector<int>& nums) {
        std::sort(nums.begin(), nums.end());
        nums_ = &nums;
        dfs(0);
        return out_;
    }
};

class Solution_2 {
public:
    std::vector<std::vector<int>> subsetsWithDup(std::vector<int>& nums) {
        std::sort(nums.begin(), nums.end());
        std::vector<std::vector<int>> out;
        for (int mask = 0; mask < (1 << nums.size()); ++mask) {
            std::vector<int> cur;
            for (size_t j = 0; j < nums.size(); ++j)
                if (mask & (1 << j)) cur.push_back(nums[j]);
            if (std::find(out.begin(), out.end(), cur) == out.end())
                out.push_back(cur);                  // dedupe by linear scan
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
    std::vector<int> nums = {1, 2, 2};
    const long mem0 = memKb();
    auto t0 = nowUs();
    auto r1 = Solution_1().subsetsWithDup(nums);
    nums = {1, 2, 2};
    auto r2 = Solution_2().subsetsWithDup(nums);
    auto t1 = nowUs();
    std::cout << "A1 size=" << r1.size() << " A2 size=" << r2.size()
              << " (want 6: [[],[1],[1,2],[1,2,2],[2],[2,2]]) "
              << (r1.size() == 6 && r2.size() == 6 ? "PASS" : "FAIL")
              << " | time: " << (t1 - t0) << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
