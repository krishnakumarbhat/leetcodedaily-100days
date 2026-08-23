/*
 * =====================================================================
 * LeetCode 0153 : Find Minimum in Rotated Sorted Array              (Medium)
 * https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
 * Category   : Binary Search
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A sorted array is rotated at an unknown pivot (e.g. [0,1,2,4,5,6,7]
 *   becomes [4,5,6,7,0,1,2]). All values are UNIQUE. Find the minimum
 *   element in O(log n).
 * ---------------------------------------------------------------------
 * INTUITION
 *   The minimum is the PIVOT — the only element smaller than the one
 *   before it, i.e. the drop point. In the rotated world, "is
 *   nums[mid] <= nums[n-1]?" is a monotone predicate: FALSE on the
 *   left run, TRUE on the right run. Binary search finds the first
 *   TRUE index — which IS the minimum. Halve the window O(log n) times.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Binary search: compare mid against the RIGHT edge
 *   Invariant: the minimum is inside [lo, hi]. Per iteration:
 *     • nums[mid] > nums[hi] → the drop is strictly to the right of
 *       mid (left run still descending past mid) → lo = mid + 1.
 *     • nums[mid] <= nums[hi] → mid lies on the right run; the
 *       minimum is at mid or to its left → hi = mid.
 *   Loop is `lo < hi` because hi = mid keeps the window size >= 1;
 *   after the loop lo == hi == the pivot.
 *   Time  Complexity : O(log n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort, then take the first (cheating contrast)
 *   std::sort the copy and read the front. Correct, trivial, and
 *   O(n log n) — a reminder of WHY the binary-search version matters:
 *   at n = 1e6 the BS does ~20 probes; sorting touches millions.
 *   Time  Complexity : O(n log n)   Space Complexity : O(n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — the false→true predicate that makes this work
 *   Define P(k) = "nums[k] <= nums[n-1]" over the whole array. On the
 *   left run values are all BIGGER than nums[n-1] → P is false; on the
 *   right run values are <= nums[n-1] → P is true. P is monotone:
 *   false false … false TRUE TRUE … TRUE, and the FIRST true index is
 *   exactly the minimum. This is the binary-search invariant from
 *   0704 in disguise: every iteration keeps [lo, hi] around the
 *   false→true boundary, exactly like std::lower_bound finds the
 *   first element >= key. The same predicate trick powers 0033
 *   (pivot + segment search) and 0875 (feasible eating speed).
 * =====================================================================
 */

#include <iostream>     // std::cout — printing results
#include <vector>       // std::vector — the rotated input array
#include <string>       // std::string — PASS/FAIL verdicts
#include <unordered_map>// (included per section convention; unused here)
#include <map>          // (included per section convention; unused here)
#include <algorithm>    // std::sort — approach 2
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Binary search on the "mid vs right edge" predicate
 * ===================================================================== */
class Solution_BinarySearch {
public:
    /*
     * Purpose : Return the minimum of a rotated sorted array.
     * Inputs  : nums — rotated sorted vector<int> with unique values.
     * Output  : int minimum element (the pivot).
     */
    int findMin(const std::vector<int>& nums) {
        // Invariant: the minimum lives inside [lo, hi].
        int lo = 0;
        int hi = static_cast<int>(nums.size()) - 1;

        // `lo < hi` (not <=): hi = mid keeps the window from emptying;
        // the loop terminates with lo == hi == pivot.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;      // overflow-safe midpoint.

            if (nums[mid] > nums[hi]) {
                // mid sits on the LEFT run (bigger than the right
                // edge) → the drop must be strictly to the right.
                lo = mid + 1;
            } else {
                // mid sits on the RIGHT run → the minimum is mid or
                // to its left; keep mid in scope (hi = mid).
                hi = mid;
            }
        }

        return nums[lo];                       // lo == hi == pivot index.
    }
};

/* =====================================================================
 * APPROACH 2 : Sort a copy and take the first element (contrast)
 * ===================================================================== */
class Solution_SortFirst {
public:
    /*
     * Purpose : Return the minimum of a rotated sorted array.
     * Inputs  : nums — rotated sorted vector<int> with unique values.
     * Output  : int minimum element.
     */
    int findMin(const std::vector<int>& nums) {
        // Sorting destroys the rotation information entirely.
        std::vector<int> copy = nums;
        std::sort(copy.begin(), copy.end());

        // The minimum of a sorted array is its first element.
        return copy.front();
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, print time + peak RAM
 * ===================================================================== */
int main() {
    // Test cases: classic rotation, full-circle (unrotated), 1 element.
    std::vector<std::vector<int>> tests = {
        {4, 5, 6, 7, 0, 1, 2},          // expect 0 at index 4
        {11, 13, 15, 17},               // expect 11 (no rotation)
        {3}                             // single element — expect 3
    };

    for (size_t t = 0; t < tests.size(); ++t) {
        const std::vector<int>& nums = tests[t];

        // --- Approach 1 timing + peak-RAM delta ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto start1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_BinarySearch().findMin(nums);
        auto end1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        long kb1 = after1.ru_maxrss - before1.ru_maxrss; // ru_maxrss is KB on Linux

        // --- Approach 2 timing + peak-RAM delta ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto start2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_SortFirst().findMin(nums);
        auto end2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        long kb2 = after2.ru_maxrss - before2.ru_maxrss;

        // --- Verdict: min over a linear scan is the ground truth ---
        int expect = nums[0];
        for (size_t i = 1; i < nums.size(); ++i) {
            if (nums[i] < expect) { expect = nums[i]; }
        }
        bool ok = (r1 == expect) && (r2 == expect);

        std::cout << "Test " << (t + 1) << ": size " << nums.size()
                  << " | A1 binary search = " << r1 << " (" << us1
                  << " us, +" << kb1 << " KB) | A2 sort-first = " << r2
                  << " (" << us2 << " us, +" << kb2 << " KB) | expect "
                  << expect << " | " << (ok ? "PASS" : "FAIL") << "\n";
    }

    return 0;
}