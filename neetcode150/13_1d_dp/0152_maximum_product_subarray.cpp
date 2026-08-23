/*
 * =====================================================================
 * LeetCode 152 : Maximum Product Subarray                         (Medium)
 * https://leetcode.com/problems/maximum-product-subarray/
 * Category   : 1-D dynamic programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Contiguous subarray with the LARGEST product. Negatives and zeros
 *   make this harder than the max-sum version.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A negative number flips the sign of every product ending at i:
 *   the running MINIMUM can become the maximum. So track BOTH the
 *   largest and smallest product of subarrays ending at each position.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Kadane-with-min (best)
 *   maxEnd = max(a, maxEnd*a, minEnd*a); minEnd = min(...same three);
 *   answer = max(answer, maxEnd) per step.
 * APPROACH 2 · Two-pass prefix/suffix products
 *   The optimal subarray never needs to cross BOTH a zero and a
 *   negative... scan products left→right and right→left, taking max;
 *   reset at zeros. Simpler to reason about, same O(n).
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why Kadane-with-min is correct
 *   The classic "drop the prefix if negative" fails: [-2, 3, -4] → the
 *   full array wins (24) despite a negative prefix. Keeping minEnd
 *   preserves the option "multiply the worst prefix by this negative",
 *   which is exactly the case where prefix-dropping loses. At zeros
 *   both extremal products reset naturally via a*0 = 0.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n).
 * MEMORY COMPLEXITY: O(1).
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int maxProduct(std::vector<int>& nums) {
        int best = nums[0], maxEnd = nums[0], minEnd = nums[0];
        for (size_t i = 1; i < nums.size(); ++i) {
            int a = nums[i];
            if (a < 0) std::swap(maxEnd, minEnd);   // sign flip swaps roles
            maxEnd = std::max(a, maxEnd * a);
            minEnd = std::min(a, minEnd * a);
            best = std::max(best, maxEnd);
        }
        return best;
    }
};

class Solution_2 {
public:
    int maxProduct(std::vector<int>& nums) {
        int best = nums[0];
        int cur = 1;
        for (int x : nums) {                        // left-to-right products
            cur *= x;
            best = std::max(best, cur);
            if (x == 0) cur = 1;
        }
        cur = 1;
        for (size_t i = nums.size(); i-- > 0;) {    // right-to-left products
            cur *= nums[i];
            best = std::max(best, cur);
            if (nums[i] == 0) cur = 1;
        }
        return best;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<int> nums; int want; };
    const Case cases[] = {
        {{2, 3, -2, 4}, 6},
        {{-2, 0, -1}, 0},
        {{-2, 3, -4}, 24},
        {{0}, 0}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        std::vector<int> v1 = c.nums, v2 = c.nums;
        int r1 = Solution_1().maxProduct(v1);
        int r2 = Solution_2().maxProduct(v2);
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "→ A1=" << r1 << " A2=" << r2 << " (want " << c.want
                  << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
