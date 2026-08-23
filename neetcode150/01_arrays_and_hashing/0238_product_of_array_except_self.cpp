/*
 * =====================================================================
 * LeetCode 238 : Product of Array Except Self                   (Medium)
 * https://leetcode.com/problems/product-of-array-except-self/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Return an array answer where answer[i] = product of ALL elements
 *   of nums EXCEPT nums[i]. MUST run in O(n) WITHOUT using division.
 * ---------------------------------------------------------------------
 * INTUITION
 *   answer[i] = (product of everything LEFT of i) × (product of
 *   everything RIGHT of i). Compute "prefix products" left-to-right,
 *   then multiply by "suffix products" right-to-left — both in the
 *   SAME output array, so extra memory stays O(1).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Prefix × suffix in the output array (BEST)
 *   Pass 1: answer[i] = product of nums[0..i-1] (prefix).
 *   Pass 2: multiply answer[i] by product of nums[i+1..n-1] while
 *           tracking the running suffix product in one variable.
 *   Time  Complexity : O(n)   Space Complexity : O(1) extra
 *   (the output array does not count as extra space).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Divide-by-self (CONTRAST — why it is illegal here)
 *   total = product of all; answer[i] = total / nums[i].
 *   Time  Complexity : O(n)   Space Complexity : O(1).
 *   FAILS on two counts: (1) the problem explicitly forbids division;
 *   (2) any ZERO in nums crashes it (division by zero) or corrupts
 *   every other answer (one zero makes only ITS slot wrong, two zeros
 *   make everything zero). Shown only to explain why we avoid it.
 * =====================================================================
 */

#include <vector>          // std::vector — input + output containers
#include <chrono>          // timing for the benchmark
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : Prefix × suffix without division — O(n) / O(1)
 * ===================================================================== */
class Solution_PrefixSuffix {
public:
    /*
     * Purpose : Compute product of all elements except each one.
     * Inputs  : nums — the input array.
     * Output  : vector where answer[i] = product of nums except nums[i].
     */
    vector<int> productExceptSelf(const vector<int>& nums) {

        // The answer array doubles as working memory → O(1) extra.
        vector<int> answer(nums.size());

        // ---- Pass 1 : prefix products ----
        // answer[i] = product of everything to the LEFT of i.
        answer[0] = 1;  // nothing is left of index 0 → neutral product 1
        for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
            // carry the product: left-of-i = left-of-(i-1) × nums[i-1].
            answer[i] = answer[i - 1] * nums[i - 1];
        }

        // ---- Pass 2 : fold in suffix products ----
        // suffix = product of everything to the RIGHT of the current i.
        int suffix = 1;  // nothing is right of the last index
        for (int i = static_cast<int>(nums.size()) - 1; i >= 0; --i) {
            // prefix(left of i) × suffix(right of i) = answer for i.
            answer[i] *= suffix;
            // move left one step: the suffix grows with nums[i].
            suffix *= nums[i];
        }
        return answer;
    }
};

/* =====================================================================
 * APPROACH 2 : Divide-by-self — shown ONLY as a contrast
 * ===================================================================== */
class Solution_DivideBySelf {
public:
    /*
     * Purpose : Contrast implementation using division (invalid here).
     * Inputs  : nums — the input array.
     * Output  : vector where answer[i] = product of nums except nums[i].
     * NOTE    : This is NOT an accepted solution — the problem forbids
     *           division, and zeros break it mathematically.
     */
    vector<int> productExceptSelf(const vector<int>& nums) {

        // total : product of every element.
        long long total = 1;
        for (int num : nums) {
            total *= num;
        }

        // Each slot = total / itself — division is the forbidden tool.
        vector<int> answer(nums.size());
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            answer[i] = static_cast<int>(total / nums[i]);  // CRASHES on nums[i]==0
        }
        return answer;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // Official example (2*3*4=24, 1*3*4=12, 1*2*4=8, 1*2*3=6).
    vector<int> nums = {1, 2, 3, 4};

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    auto r1 = Solution_PrefixSuffix().productExceptSelf(nums);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    cout << "Approach 1 (prefix × suffix) : [";
    for (size_t i = 0; i < r1.size(); ++i) cout << (i ? "," : "") << r1[i];
    cout << "]  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";

    // Ground truth computed independently with the definition.
    vector<int> expected(nums.size(), 1);
    for (int i = 0; i < static_cast<int>(nums.size()); ++i)
        for (int j = 0; j < static_cast<int>(nums.size()); ++j)
            if (i != j) expected[i] *= nums[j];

    cout << ((r1 == expected) ? "PASS : prefix×suffix matches the definition."
                              : "FAIL : wrong answer.")
         << "\n";
    return 0;
}