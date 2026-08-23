/*
 * =====================================================================
 * LeetCode 0004 : Median of Two Sorted Arrays                        (Hard)
 * https://leetcode.com/problems/median-of-two-sorted-arrays/
 * Category   : Binary Search
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two sorted arrays `nums1` and `nums2` of sizes m and n,
 *   return the median of the two merged arrays. Must run in
 *   O(log(m + n)) — this is the constraint that forces binary search.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Median = the value that splits the combined data so the LEFT half
 *   and RIGHT half hold the same number of elements. Instead of
 *   merging (O(m+n)), we ask: "where does the cut go in the smaller
 *   array?" — then the cut position in the other array is FORCED by
 *   the half-count equation. Each probe on the smaller array either
 *   validates the cut or discards half of the remaining positions.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Merge, then pick the middle (baseline, O(m+n))
 *   Walk both arrays with two pointers, always appending the smaller
 *   head — exactly like the merge step of merge sort. When the merged
 *   length hits the middle, read the median:
 *     • odd total   → the middle element.
 *     • even total  → average of the two middle elements.
 *   Correct and simple; too slow for the O(log(m+n)) requirement but
 *   a perfect ground-truth referee.
 *   Time  Complexity : O(m+n)   Space Complexity : O(m+n)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Binary search on the partition (BEST, O(log min(m,n)))
 *   Let A be the SMALLER array (keeps the probe count minimal). The
 *   median cut is: i elements from A's left, j = (m+n+1)/2 - i from
 *   B's left. Probe i with binary search; the cut is valid when
 *   A[i-1] <= B[j] AND B[j-1] <= A[i] (every left element ≤ every
 *   right element). If A[i-1] > B[j], i is too big → search left;
 *   else i is too small → search right. The loop moves i until the
 *   cut balances; the median is then read off the four boundary
 *   elements A[i-1], A[i], B[j-1], B[j].
 *   The equation i + j = (m+n+1)/2 is THE invariant: it forces the
 *   halves to hold ⌈(m+n)/2⌉ elements so the median boundary is exact.
 *   Time  Complexity : O(log(min(m, n)))   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why i + j = (m+n+1)/2 and where the +1 comes from
 *   The cut divides combined data into left (i + j elements) and
 *   right (m+n-i-j). For the median we need i + j = ⌈(m+n)/2⌉.
 *   (m+n+1)/2 is exactly ⌈(m+n)/2⌉ in integer arithmetic — the +1
 *   makes ODD totals put the extra element on the left, so the median
 *   is max(left side) and the even case reads the average of the two
 *   middle boundaries. i and j are COUNTS of elements on the left
 *   (while A[i] and B[j] are VALUES, 0-based) — so j is derived, not
 *   probed: j = (m+n+1)/2 - i falls out of the count equation.
 *   When i = 0 or i = m (cut at the edge), the missing neighbor is
 *   treated as ∓∞ so comparisons behave. This problem is the hardest
 *   BS variant in the 150 — mastering the invariant here makes 153 /
 *   875 / 981 feel like the same idea with easier math.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing results
#include <vector>       // std::vector — the two sorted input arrays
#include <string>       // std::string — PASS/FAIL verdicts
#include <unordered_map>// (included per section convention; unused here)
#include <map>          // (included per section convention; unused here)
#include <algorithm>    // std::max/std::min — boundary-element pick
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Merge with two pointers, then read the middle
 * ===================================================================== */
class Solution_Merge {
public:
    /*
     * Purpose : Return the median of two sorted arrays by merging.
     * Inputs  : nums1, nums2 — sorted vectors of ints.
     * Output  : double median of the combined data.
     */
    double findMedianSortedArrays(const std::vector<int>& nums1,
                                  const std::vector<int>& nums2) {
        // Two-pointer merge into one sorted array — O(m+n) memory.
        std::vector<int> merged;
        merged.reserve(nums1.size() + nums2.size());
        size_t i = 0, j = 0;

        // Always append the smaller of the two current heads.
        while (i < nums1.size() && j < nums2.size()) {
            if (nums1[i] <= nums2[j]) {
                merged.push_back(nums1[i++]);   // take from nums1.
            } else {
                merged.push_back(nums2[j++]);   // take from nums2.
            }
        }
        // Drain whichever array still has leftovers (sorted by itself).
        while (i < nums1.size()) {
            merged.push_back(nums1[i++]);
        }
        while (j < nums2.size()) {
            merged.push_back(nums2[j++]);
        }

        // Median: middle element (odd) or mean of two middles (even).
        size_t n = merged.size();
        if (n % 2 == 1) {
            return static_cast<double>(merged[n / 2]);
        }
        return (merged[n / 2 - 1] + merged[n / 2]) / 2.0;
    }
};

/* =====================================================================
 * APPROACH 2 : Binary search the partition in the SMALLER array
 * ===================================================================== */
class Solution_BS_Partition {
public:
    /*
     * Purpose : Return the median of two sorted arrays in O(log min).
     * Inputs  : nums1, nums2 — sorted vectors of ints.
     * Output  : double median of the combined data.
     */
    double findMedianSortedArrays(const std::vector<int>& nums1,
                                  const std::vector<int>& nums2) {
        // A = smaller array → binary search domain of size min(m, n).
        const std::vector<int>& A =
            (nums1.size() <= nums2.size()) ? nums1 : nums2;
        const std::vector<int>& B =
            (nums1.size() <= nums2.size()) ? nums2 : nums1;

        int total = static_cast<int>(A.size() + B.size());
        // THE invariant: the left half must hold ⌈total/2⌉ elements.
        // (total+1)/2 is that ceiling in integer arithmetic — the +1
        // pushes the extra middle element LEFT for odd totals.
        int leftCount = (total + 1) / 2;

        // i = number of A-elements on the left of the cut. Its window
        // is [0, A.size()] because the cut can sit at either edge.
        int lo = 0;
        int hi = static_cast<int>(A.size());

        while (lo <= hi) {
            int i = lo + (hi - lo) / 2;      // probe the cut in A.
            // j is FORCED by the invariant: i + j = leftCount, so the
            // two left halves together always hold ⌈total/2⌉ elements.
            int j = leftCount - i;

            // Boundary values with ∓∞ sentinels for edge cuts.
            // A[i-1] = rightmost element of A's left part (i==0 → -inf)
            // B[j-1] = rightmost element of B's left part (j==0 → -inf)
            double aLeft  = (i >= 1) ? A[i - 1] : -1e18;
            double aRight = (i < static_cast<int>(A.size())) ? A[i] : 1e18;
            double bLeft  = (j >= 1) ? B[j - 1] : -1e18;
            double bRight = (j < static_cast<int>(B.size())) ? B[j] : 1e18;

            if (aLeft <= bRight && bLeft <= aRight) {
                // Cut is BALANCED: every left ≤ every right.
                if (total % 2 == 1) {
                    return std::max(aLeft, bLeft);   // odd → median is max of left.
                }
                return (std::max(aLeft, bLeft) + std::min(aRight, bRight)) / 2.0;
            }
            if (aLeft > bRight) {
                hi = i - 1;                  // too many A-elements on the left.
            } else {
                lo = i + 1;                  // too few — pull more from A.
            }
        }
        return 0.0;                          // unreachable with valid input.
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, print time + peak RAM
 * ===================================================================== */
int main() {
    // Test cases: odd total, even total, and a single-element edge.
    std::vector<std::pair<std::vector<int>, std::vector<int>>> tests = {
        { {1, 3}, {2} },                          // merged [1,2,3] → 2.0
        { {1, 2}, {3, 4} },                       // merged [1,2,3,4] → 2.5
        { {0, 0}, {0, 0} },                       // merged [0,0,0,0] → 0.0
        { {1, 3, 5, 7}, {2, 4, 6, 8, 10} }        // merged odd → 5.0
    };

    for (size_t t = 0; t < tests.size(); ++t) {
        const std::vector<int>& n1 = tests[t].first;
        const std::vector<int>& n2 = tests[t].second;

        // --- Approach 1 timing + peak-RAM delta ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto start1 = std::chrono::high_resolution_clock::now();
        double r1 = Solution_Merge().findMedianSortedArrays(n1, n2);
        auto end1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        long kb1 = after1.ru_maxrss - before1.ru_maxrss; // ru_maxrss is KB on Linux

        // --- Approach 2 timing + peak-RAM delta ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto start2 = std::chrono::high_resolution_clock::now();
        double r2 = Solution_BS_Partition().findMedianSortedArrays(n1, n2);
        auto end2 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        long kb2 = after2.ru_maxrss - before2.ru_maxrss;

        // --- Verdict: brute-force referee computes the true median ---
        std::vector<int> merged = n1;
        merged.insert(merged.end(), n2.begin(), n2.end());
        std::sort(merged.begin(), merged.end());
        double expect;
        if (merged.size() % 2 == 1) {
            expect = static_cast<double>(merged[merged.size() / 2]);
        } else {
            expect = (merged[merged.size() / 2 - 1] + merged[merged.size() / 2]) / 2.0;
        }
        bool ok = (r1 == expect) && (r2 == expect);

        std::cout << "Test " << (t + 1) << ": |A|=" << n1.size() << " |B|="
                  << n2.size() << " | A1 merge = " << r1 << " (" << us1
                  << " us, +" << kb1 << " KB) | A2 BS-partition = " << r2
                  << " (" << us2 << " us, +" << kb2 << " KB) | expect "
                  << expect << " | " << (ok ? "PASS" : "FAIL") << "\n";
    }

    return 0;
}