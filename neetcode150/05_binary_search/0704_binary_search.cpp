/*
 * =====================================================================
 * LeetCode 704 : Binary Search                                       (Easy)
 * https://leetcode.com/problems/binary-search/
 * Category   : Binary Search
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a SORTED array of integers `nums` and an integer `target`,
 *   return the index of `target`, or -1 if it is not present.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The array is sorted, so every comparison with `nums[mid]` lets us
 *   DISCARD half of the remaining candidates. Each probe halves the
 *   search space → we find the answer in log2(n) probes instead of n.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Classic lo <= hi loop (find ANY hit)
 *   Maintain the invariant: `target` (if present) lives in [lo, hi].
 *   Each iteration probes mid = lo + (hi-lo)/2:
 *     • nums[mid] == target → found, return mid immediately.
 *     • nums[mid] <  target → the left half can never hold target,
 *                             so narrow to [mid+1, hi].
 *     • nums[mid] >  target → narrow to [lo, mid-1].
 *   The loop exits with lo > hi — the moment the window inverts, the
 *   element cannot exist. `<=` matters: with a single-element window
 *   [k, k] we still need one probe to test nums[k].
 *   Time  Complexity : O(log n)  — log2(n) probes, each O(1).
 *   Space Complexity : O(1)      — only three index variables.
 * ---------------------------------------------------------------------
 * APPROACH 2 — lo < hi loop (find the LOWER BOUND, then verify)
 *   Variant taught by the "first true predicate" school. The invariant
 *   here is: everything in [lo, hi) has NOT yet been confirmed false.
 *   Instead of returning on a hit, the loop SHRINKS toward the first
 *   index whose value >= target:
 *     • nums[mid] >= target → mid could be the answer, keep it: hi = mid.
 *     • nums[mid] <  target → mid is too small: lo = mid + 1.
 *   After the loop lo == hi == the first index with nums[lo] >= target.
 *   One final check decides "exact hit" vs "absent". This variant is
 *   the one that generalizes to 0033 / 0153 / 0875 — the predicate
 *   pattern (false…false → true…true) is the real invariant of BS.
 *   Time  Complexity : O(log n)   Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — the binary search invariant and the off-by-one
 *   Both loops maintain ONE invariant: "the answer lies inside the
 *   current window". The loop condition differs because the windows
 *   shrink differently:
 *     • lo <= hi : window is INCLUSIVE; each step removes mid, so the
 *       window size decreases by ≥1 and can reach 0 → the loop must
 *       allow one final probe of a size-1 window (hence `<=`).
 *     • lo <  hi : window is HALF-OPEN [lo, hi); hi never moves past
 *       mid, so the window only ever shrinks to size ≥ 1 → the loop
 *       terminates with lo == hi and you check that single cell after.
 *   The predicate view (used by 0033, 0153, 0875, 0981): define
 *   P(x) = "answer is ≤ x". For sorted data P is monotone:
 *   false false … false TRUE TRUE … TRUE. Binary search finds the
 *   FIRST true index in O(log n) — this is exactly std::lower_bound.
 *   C++ STL internals: lower_bound returns the first element >= key
 *   (first true of P(x) = "x >= key"); upper_bound returns the first
 *   element > key. Both run O(log n) with the same halving loop.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing results
#include <vector>       // std::vector — the sorted input array
#include <string>       // std::string — PASS/FAIL verdicts
#include <unordered_map>// (included per section convention; unused here)
#include <map>          // (included per section convention; unused here)
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Classic inclusive-window binary search (lo <= hi)
 * ===================================================================== */
class Solution_ClassicLoop {
public:
    /*
     * Purpose : Return the index of `target` in sorted `nums`, else -1.
     * Inputs  : nums   — sorted vector<int> to search.
     *           target — integer value being searched for.
     * Output  : int index of target, or -1 when absent.
     */
    int search(const std::vector<int>& nums, int target) {
        // lo/hi bound the window [lo, hi] that may contain target.
        int lo = 0;
        int hi = static_cast<int>(nums.size()) - 1;

        // `<=` keeps a size-1 window [k, k] alive for its final probe.
        while (lo <= hi) {
            // mid = lo + (hi-lo)/2 avoids overflow of (lo+hi) on 32-bit.
            int mid = lo + (hi - lo) / 2;

            if (nums[mid] == target) {
                return mid;              // exact hit — done in one probe.
            }
            if (nums[mid] < target) {
                lo = mid + 1;            // discard left half entirely.
            } else {
                hi = mid - 1;            // discard right half entirely.
            }
        }

        // Window inverted (lo > hi) → every candidate eliminated.
        return -1;
    }
};

/* =====================================================================
 * APPROACH 2 : Half-open lower-bound loop (lo < hi) + final check
 * ===================================================================== */
class Solution_LowerBound {
public:
    /*
     * Purpose : Return the index of `target` in sorted `nums`, else -1.
     * Inputs  : nums   — sorted vector<int> to search.
     *           target — integer value being searched for.
     * Output  : int index of target, or -1 when absent.
     */
    int search(const std::vector<int>& nums, int target) {
        // Window is half-open [lo, hi): candidates live in here.
        int lo = 0;
        int hi = static_cast<int>(nums.size());

        // `lo < hi` + hi = mid ⇒ window never empties, no mid re-probe.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;

            if (nums[mid] >= target) {
                // mid qualifies as "first >= target" — keep it in scope.
                hi = mid;
            } else {
                // mid is strictly too small — safe to discard it.
                lo = mid + 1;
            }
        }

        // lo == hi == first index with nums[lo] >= target.
        // Only a final O(1) check tells "hit" from "absent".
        if (lo < static_cast<int>(nums.size()) && nums[lo] == target) {
            return lo;
        }
        return -1;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, print time + peak RAM
 * ===================================================================== */
int main() {
    // Test cases: hit in the middle, hit at the boundary, and a miss.
    std::vector<std::pair<std::vector<int>, int>> tests = {
        { {-1, 0, 3, 5, 9, 12}, 9 },      // hit — expect index 4
        { {-1, 0, 3, 5, 9, 12}, 2 },      // miss — expect -1
        { {5}, 5 }                        // single element — expect 0
    };

    // Run each approach over every test; accumulate timings.
    for (size_t t = 0; t < tests.size(); ++t) {
        const std::vector<int>& nums = tests[t].first;
        int target = tests[t].second;

        // --- Approach 1 timing + peak-RAM delta ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto start1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_ClassicLoop().search(nums, target);
        auto end1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        long kb1 = after1.ru_maxrss - before1.ru_maxrss; // ru_maxrss is KB on Linux

        // --- Approach 2 timing + peak-RAM delta ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto start2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_LowerBound().search(nums, target);
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

        std::cout << "Test " << (t + 1) << ": nums size " << nums.size()
                  << " target " << target
                  << " | A1 classic = " << r1 << " (" << us1 << " us, +"
                  << kb1 << " KB) | A2 lower_bound = " << r2 << " ("
                  << us2 << " us, +" << kb2 << " KB)"
                  << " | " << (ok ? "PASS" : "FAIL") << "\n";
    }

    return 0;
}