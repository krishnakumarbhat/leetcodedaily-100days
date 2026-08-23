/*
 * =====================================================================
 * LeetCode 300 : Longest Increasing Subsequence                    (Medium)
 * https://leetcode.com/problems/longest-increasing-subsequence/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer array `nums`, return the length of the LONGEST
 *   strictly-increasing SUBSEQUENCE (elements keep order, may skip).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Look at each element as the END of a subsequence. The longest
 *   increasing subsequence ending AT nums[i] appends nums[i] to the
 *   best sequence ending at some EARLIER nums[j] < nums[i]:
 *       dp[i] = 1 + max(dp[j] for j < i and nums[j] < nums[i])
 *   Overlapping subproblems: dp[j] is reused by every later i with
 *   nums[i] > nums[j]. Greedy alternative: a sorted `tails` array
 *   where tails[k] = smallest possible last element of a length-k+1
 *   increasing subsequence.
 * ---------------------------------------------------------------------
 * APPROACH 1 — O(n²) DP (BEST when n ≤ 2000)
 *   dp[i] = length of the LIS ending at index i.
 *   Recurrence : dp[i] = 1 + max( dp[j] ) over j < i, nums[j] < nums[i]
 *                base: dp[i] = 1 (the element alone).
 *   State space : i ∈ [0, n) → n states on array dp[n]; cell i scans
 *                EVERY earlier cell j → full table required (each cell
 *                has a different set of smaller predecessors).
 *   Time  Complexity : O(n²)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Patience sorting + binary search (BEST for big n)
 *   tails stays sorted; for each num find the FIRST slot where
 *   tails[slot] >= num (lower bound) and replace it. slots beyond the
 *   current length only grow when num is a new record tail.
 *   Time  Complexity : O(n log n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why tails[] is sorted and why lower_bound is exact
 *   Invariant: tails[k] is the SMALLEST tail achievable for a length
 *   k+1 subsequence. Because each slot is replaced only by smaller
 *   values, tails stays strictly increasing — so binary search applies.
 *   lower_bound(tails, num) finds the first slot that is not smaller:
 *     • found → replacing tails[slot] with the smaller num can only
 *       help future extensions (never hurts — slot's length class
 *       exists with an equal-or-better tail);
 *     • not found → num is larger than every tail → it EXTENDS the
 *       longest sequence, appending a new slot.
 *   Time math: n numbers × O(log n) search = O(n log n) vs O(n²)
 *   comparisons of the DP table — the table's O(n²) work is replaced
 *   by the sorted-array trick. Real life : patience sorting is the
 *   optimal Solitaire strategy; LIS powers LCS, diff tools, and
 *   dependency-chain analysis.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <sys/resource.h>
#include <algorithm>

/* =====================================================================
 * APPROACH 1 : O(n²) classic DP
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Length of the longest strictly increasing subsequence.
     * Inputs  : nums — integer array.
     * Output  : int — LIS length.
     */
    int lengthOfLIS(const std::vector<int>& nums) {
        const int n = static_cast<int>(nums.size());
        // dp[i] = LIS length ending at i; every element alone is 1.
        std::vector<int> dp(n, 1);
        int best = 1;
        for (int i = 1; i < n; ++i) {
            // Scan all earlier ends; extend the best one that is smaller.
            for (int j = 0; j < i; ++j) {
                if (nums[j] < nums[i]) {
                    dp[i] = std::max(dp[i], dp[j] + 1);
                }
            }
            best = std::max(best, dp[i]);
        }
        return best;
    }
};

/* =====================================================================
 * APPROACH 2 : patience sorting with binary search (O(n log n))
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Length of the longest strictly increasing subsequence.
     * Inputs  : nums — integer array.
     * Output  : int — LIS length.
     */
    int lengthOfLIS(const std::vector<int>& nums) {
        // tails[k] = smallest possible tail of a length-(k+1) LIS.
        std::vector<int> tails;
        for (const int num : nums) {
            // lower_bound: first index with tails[idx] >= num.
            const auto it = std::lower_bound(tails.begin(), tails.end(), num);
            if (it == tails.end()) {
                tails.push_back(num);  // num is a record tail → extends LIS
            } else {
                *it = num;             // improve slot it - tails.begin()
            }
        }
        return static_cast<int>(tails.size());
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (nums, expected LIS). Both solutions must match.
    struct Test { std::vector<int> nums; int expected; };
    const std::vector<Test> tests = {
        {{10, 9, 2, 5, 3, 7, 101, 18}, 4},  // [2,3,7,101]
        {{0, 1, 0, 3, 2, 3}, 4},            // [0,1,2,3]
        {{7, 7, 7, 7}, 1}                   // strictly → ties do not chain
    };

    double total_us_1 = 0.0, total_us_2 = 0.0;
    long total_kb_1 = 0, total_kb_2 = 0;
    bool allPass = true;

    for (const Test& t : tests) {
        // --- Approach 1: time via steady_clock, RAM via getrusage ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().lengthOfLIS(t.nums);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        // ru_maxrss delta = peak RAM consumed by THIS run (KB on Linux).
        const double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        const long kb1 = after1.ru_maxrss - before1.ru_maxrss;
        total_us_1 += us1;
        total_kb_1 += kb1;

        // --- Approach 2 ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().lengthOfLIS(t.nums);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        const double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        const long kb2 = after2.ru_maxrss - before2.ru_maxrss;
        total_us_2 += us2;
        total_kb_2 += kb2;

        const bool ok = (r1 == t.expected) && (r2 == t.expected);
        allPass = allPass && ok;

        std::cout << "A1=" << r1 << "  A2=" << r2
                  << "  expected=" << t.expected
                  << (ok ? "  PASS" : "  FAIL")
                  << "  A1 " << us1 << "µs/" << kb1 << "KB  A2 " << us2
                  << "µs/" << kb2 << "KB\n";
    }

    std::cout << "Totals: A1 " << total_us_1 << "µs/" << total_kb_1
              << "KB | A2 " << total_us_2 << "µs/" << total_kb_2 << "KB\n";
    std::cout << (allPass
                  ? "PASS : both approaches match every expected output."
                  : "FAIL : at least one answer is wrong.")
              << "\n";
    return allPass ? 0 : 1;
}