/*
 * =====================================================================
 * LeetCode 0033 : Search in Rotated Sorted Array                   (Medium)
 * https://leetcode.com/problems/search-in-rotated-sorted-array/
 * Category   : Binary Search
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A sorted array is rotated at an unknown pivot (e.g. [0,1,2,4,5,6,7]
 *   becomes [4,5,6,7,0,1,2]). Given the rotated array and a `target`,
 *   return its index or -1. All values are UNIQUE. Must run in O(log n).
 * ---------------------------------------------------------------------
 * INTUITION
 *   After one rotation the array is two ascending runs glued together.
 *   In ANY window [lo, hi] at least ONE side of mid is still fully
 *   sorted — that sorted side is a normal binary-search sub-problem.
 *   Decide which side the target belongs to; if the sorted side cannot
 *   contain it, the answer must be in the other half. Halving still
 *   works, so O(log n) survives the rotation.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Direct BS: find the sorted half, decide, discard
 *   Invariant: target, if present, is in [lo, hi]. Per iteration:
 *     1. mid = lo + (hi-lo)/2; hit → return.
 *     2. If nums[lo] <= nums[mid], the LEFT half is sorted:
 *          target inside [nums[lo], nums[mid]) → hi = mid-1.
 *          otherwise → lo = mid+1.
 *     3. Else the RIGHT half is sorted:
 *          target inside (nums[mid], nums[hi]] → lo = mid+1.
 *          otherwise → hi = mid-1.
 *   The `<=` in step 2 is the classic off-by-one: with a 2-element
 *   window [x, y], mid == lo and the left half [x] IS sorted — we must
 *   test it, not assume the right half is the sorted one.
 *   Time  Complexity : O(log n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Find the pivot, then plain BS in the right segment
 *   The pivot is the minimum element — the only place the array drops.
 *   Locate it with the 0153 trick: while nums[mid] > nums[hi] the
 *   pivot is to the right (lo = mid+1), else hi = mid. After the loop
 *   lo IS the pivot. The array is two sorted segments; compare target
 *   with nums[0] to pick the segment, then run plain 704-style BS
 *   inside it.
 *   Time  Complexity : O(log n) pivot + O(log n) search = O(log n)
 *   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * DEEP DIVE — the predicate invariant in a rotated world
 *   Plain BS works because P(x) = "x < target" is monotone. Rotation
 *   BREAKS that monotonicity at the pivot, so Approach 1 repairs it
 *   locally: each iteration restores a monotone predicate on the
 *   sorted half and narrows exactly like 0704. Approach 2 repairs it
 *   globally: find the pivot (the single transition of the circular
 *   predicate "nums[i] > nums[i+1]"), rotate the index space back to
 *   normal, then 0704 applies unchanged.
 *   This "find where the predicate flips, then search the restored
 *   domain" pattern is the same one used in 0153 (minimum) and 0875
 *   (minimum feasible speed).
 * =====================================================================
 */

#include <iostream>     // std::cout — printing results
#include <vector>       // std::vector — the rotated input array
#include <string>       // std::string — PASS/FAIL verdicts
#include <unordered_map>// (included per section convention; unused here)
#include <map>          // (included per section convention; unused here)
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Direct binary search on the sorted half
 * ===================================================================== */
class Solution_SortedHalf {
public:
    /*
     * Purpose : Return the index of `target` in a rotated sorted array.
     * Inputs  : nums   — rotated sorted vector<int> (unique values).
     *           target — integer value being searched for.
     * Output  : int index of target, or -1 when absent.
     */
    int search(const std::vector<int>& nums, int target) {
        // Invariant: target, if present, lies inside [lo, hi].
        int lo = 0;
        int hi = static_cast<int>(nums.size()) - 1;

        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;      // overflow-safe midpoint.

            if (nums[mid] == target) {
                return mid;                    // probe hit — done.
            }

            if (nums[lo] <= nums[mid]) {
                // LEFT half [lo..mid] is sorted (the <= handles the
                // 2-element window where mid == lo).
                if (nums[lo] <= target && target < nums[mid]) {
                    hi = mid - 1;              // target lives in sorted left.
                } else {
                    lo = mid + 1;              // not there → right half.
                }
            } else {
                // RIGHT half [mid..hi] is sorted.
                if (nums[mid] < target && target <= nums[hi]) {
                    lo = mid + 1;              // target lives in sorted right.
                } else {
                    hi = mid - 1;              // not there → left half.
                }
            }
        }

        return -1;                             // window inverted → absent.
    }
};

/* =====================================================================
 * APPROACH 2 : Find pivot (0153 trick), then plain BS in one segment
 * ===================================================================== */
class Solution_PivotThenSearch {
public:
    /*
     * Purpose : Return the index of `target` in a rotated sorted array.
     * Inputs  : nums   — rotated sorted vector<int> (unique values).
     *           target — integer value being searched for.
     * Output  : int index of target, or -1 when absent.
     */
    int search(const std::vector<int>& nums, int target) {
        int n = static_cast<int>(nums.size());

        // --- Phase 1: locate the pivot (the minimum element) ---
        // Predicate "nums[mid] > nums[n-1]" is true on the left run,
        // false on the right run → shrink toward the single transition.
        int lo = 0;
        int hi = n - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) {
                lo = mid + 1;                  // pivot is to the right.
            } else {
                hi = mid;                      // mid may BE the pivot.
            }
        }
        int pivot = lo;                        // index of the minimum.

        // --- Phase 2: pick the segment, then plain binary search ---
        // Segments are [0, pivot) and [pivot, n). target must belong
        // to exactly one of them; compare against nums[0] to choose.
        lo = (target >= nums[0]) ? 0 : pivot;
        hi = (target >= nums[0]) ? (pivot - 1) : (n - 1);

        while (lo <= hi) {                     // ordinary 0704 loop.
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }

        return -1;                             // absent from both segments.
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, print time + peak RAM
 * ===================================================================== */
int main() {
    // Test cases: target in the left run, in the right run, and absent.
    std::vector<std::pair<std::vector<int>, int>> tests = {
        { {4, 5, 6, 7, 0, 1, 2}, 0 },          // expect index 4
        { {4, 5, 6, 7, 0, 1, 2}, 6 },          // expect index 2
        { {4, 5, 6, 7, 0, 1, 2}, 3 }           // absent — expect -1
    };

    for (size_t t = 0; t < tests.size(); ++t) {
        const std::vector<int>& nums = tests[t].first;
        int target = tests[t].second;

        // --- Approach 1 timing + peak-RAM delta ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto start1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_SortedHalf().search(nums, target);
        auto end1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        long kb1 = after1.ru_maxrss - before1.ru_maxrss; // ru_maxrss is KB on Linux

        // --- Approach 2 timing + peak-RAM delta ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto start2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_PivotThenSearch().search(nums, target);
        auto end2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        long kb2 = after2.ru_maxrss - before2.ru_maxrss;

        // --- Verdict: answers must agree AND match ground truth ---
        int expect = -1;
        for (size_t i = 0; i < nums.size(); ++i) {
            if (nums[i] == target) { expect = static_cast<int>(i); break; }
        }
        bool ok = (r1 == expect) && (r2 == expect);

        std::cout << "Test " << (t + 1) << ": target " << target
                  << " | A1 sorted-half = " << r1 << " (" << us1 << " us, +"
                  << kb1 << " KB) | A2 pivot+BS = " << r2 << " (" << us2
                  << " us, +" << kb2 << " KB) | " << (ok ? "PASS" : "FAIL")
                  << "\n";
    }

    return 0;
}