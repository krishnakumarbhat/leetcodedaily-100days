/*
 * =====================================================================
 * LeetCode 128 : Longest Consecutive Sequence                    (Medium)
 * https://leetcode.com/problems/longest-consecutive-sequence/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an unsorted array, return the length of the longest run of
 *   consecutive integers (e.g. [100,4,200,1,3,2] → 4 for 1,2,3,4).
 *   MUST run in O(n) time.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A run like 1,2,3,4 can be grown from its FIRST element only:
 *   count up while (x+1) exists. Checking "does x+1 exist" is an
 *   O(1) hash-set lookup. To avoid restarting from the middle of an
 *   existing run, only start counting at numbers whose predecessor
 *   (x-1) is NOT in the set — every number is then touched O(1)
 *   times amortized → overall O(n).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Hash set + head-of-run growth (BEST)
 *   Time  Complexity : O(n)   Space Complexity : O(n).
 *   WHY the "x-1 in set?" guard matters: without it, [1,2,3,4] would
 *   trigger counting from 1,2,3,4 → O(n²). With it, only 1 counts.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort + linear scan
 *   Time  Complexity : O(n log n)   Space Complexity : O(1).
 *   Wins when memory is tight; loses the O(n) requirement.
 * =====================================================================
 */

#include <vector>          // std::vector — input container
#include <unordered_set>   // std::unordered_set — O(1) membership tests
#include <algorithm>       // std::sort — approach 2
#include <chrono>          // timing for the benchmark
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : Hash set + head-of-run growth — O(n)
 * ===================================================================== */
class Solution_HashSet {
public:
    /*
     * Purpose : Return the longest run of consecutive integers.
     * Inputs  : nums — unsorted array of integers.
     * Output  : length of the longest consecutive sequence.
     */
    int longestConsecutive(const vector<int>& nums) {

        // Throw everything into a set: O(1) "does x exist?" later.
        unordered_set<int> seen(nums.begin(), nums.end());

        // best : longest run discovered so far.
        int best = 0;

        // Inspect every distinct number exactly once.
        for (int x : seen) {

            // Only start a run at its HEAD: x-1 must be absent.
            // This single guard keeps the whole algorithm O(n).
            if (seen.count(x - 1)) {
                continue;  // x is mid-run → some smaller head owns it
            }

            // Grow the run upward while consecutive numbers exist.
            int length = 1;
            while (seen.count(x + length)) {
                ++length;  // extend the run by one
            }

            // Keep the global maximum.
            best = max(best, length);
        }
        return best;
    }
};

/* =====================================================================
 * APPROACH 2 : Sort + linear scan — O(n log n)
 * ===================================================================== */
class Solution_SortScan {
public:
    /*
     * Purpose : Return the longest run of consecutive integers.
     * Inputs  : nums — unsorted array of integers.
     * Output  : length of the longest consecutive sequence.
     */
    int longestConsecutive(vector<int>& nums) {

        // Sorting groups each run into a contiguous stretch — O(n log n).
        sort(nums.begin(), nums.end());

        // Edge case: empty input has no run at all.
        if (nums.empty()) {
            return 0;
        }

        // cur/best : run length ending here / global maximum.
        int cur = 1;
        int best = 1;

        // Sweep the sorted array once.
        for (int i = 1; i < static_cast<int>(nums.size()); ++i) {

            // Duplicates do not extend a run — skip them silently.
            if (nums[i] == nums[i - 1]) {
                continue;
            }

            // Consecutive value → the current run grows by one.
            if (nums[i] == nums[i - 1] + 1) {
                ++cur;
            } else {
                // Gap → the run broke; start a fresh run of length 1.
                cur = 1;
            }

            // Track the global maximum after every element.
            best = max(best, cur);
        }
        return best;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // Official example (1,2,3,4 → 4).
    vector<int> nums = {100, 4, 200, 1, 3, 2};

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    int r1 = Solution_HashSet().longestConsecutive(nums);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    // --- Approach 2 (sorts its own copy) ---
    vector<int> copy = nums;
    struct rusage b2, a2;
    getrusage(RUSAGE_SELF, &b2);
    auto s2 = chrono::high_resolution_clock::now();
    int r2 = Solution_SortScan().longestConsecutive(copy);
    auto e2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a2);
    double us2 = chrono::duration_cast<chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long mem2 = (a2.ru_maxrss - b2.ru_maxrss) / 1024;

    cout << "Approach 1 (hash set, head-of-run) : " << r1
         << "  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";
    cout << "Approach 2 (sort + scan)           : " << r2
         << "  time = " << us2 << " µs  peak-ram-delta = " << mem2 << " MB\n";

    cout << ((r1 == r2) ? "PASS : both approaches agree."
                        : "FAIL : approaches disagree.")
         << "\n";
    return 0;
}