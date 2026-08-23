/*
 * =====================================================================
 * LeetCode 217 : Contains Duplicate                              (Easy)
 * https://leetcode.com/problems/contains-duplicate/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Return true if any value appears at least twice in the array,
 *   false if every element is distinct.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Seen it before?" is literally the job of a hash set: O(1)
 *   insert + O(1) membership test. Scan once, remember everything,
 *   and the first repeat answers the question.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Hash set (BEST)
 *   For each number: already in the set → duplicate found → return
 *   true. Otherwise insert it. If the loop ends, everything was new.
 *   Time  Complexity : O(n)   — one pass, O(1) ops.
 *   Space Complexity : O(n)   — the set holds every element.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort + adjacent scan
 *   Sort the array (duplicates become neighbours), then compare each
 *   element with its next neighbour.
 *   Time  Complexity : O(n log n) — the sort dominates.
 *   Space Complexity : O(1)       — in-place sort (sorting is allowed
 *                                   here: we do not need original order).
 * ---------------------------------------------------------------------
 * DEEP DIVE — set vs map vs sorted array
 *   Python `set` = dict with no values (same linear-probing table).
 *   C++  `unordered_set` = separate chaining, O(1) average; use
 *   `std::set` (red-black tree, O(log n)) ONLY if you also need
 *   ordered iteration. If memory is critical and n is small, the
 *   sort-based approach uses zero extra memory.
 * =====================================================================
 */

#include <vector>         // std::vector — the input container
#include <unordered_set>  // std::unordered_set — O(1) membership tests
#include <algorithm>      // std::sort — used by approach 2
#include <chrono>         // timing for the benchmark
#include <iostream>       // std::cout — benchmark output
#include <sys/resource.h> // getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : Hash set — remember everything you have seen
 * ===================================================================== */
class Solution_HashSet {
public:
    /*
     * Purpose : Detect whether any value repeats inside `nums`.
     * Inputs  : nums — array of integers to inspect.
     * Output  : true if a duplicate exists, false otherwise.
     */
    bool containsDuplicate(const vector<int>& nums) {
        // seen : every distinct value we have walked past so far.
        unordered_set<int> seen;

        // Walk every element exactly once.
        for (int num : nums) {

            // If this value is already stored → second occurrence → true.
            if (seen.count(num) > 0) {
                return true;
            }

            // First occurrence → remember it for the future.
            seen.insert(num);
        }

        // Loop finished with no repeats → every element was distinct.
        return false;
    }
};

/* =====================================================================
 * APPROACH 2 : Sort + adjacent scan — zero extra memory
 * ===================================================================== */
class Solution_SortAdjacent {
public:
    /*
     * Purpose : Detect whether any value repeats inside `nums`.
     * Inputs  : nums — array of integers to inspect (will be sorted).
     * Output  : true if a duplicate exists, false otherwise.
     */
    bool containsDuplicate(vector<int>& nums) {

        // Sorting groups equal values side by side — the O(n log n) step.
        sort(nums.begin(), nums.end());

        // Walk the sorted array comparing each element with its neighbour.
        for (int i = 1; i < static_cast<int>(nums.size()); ++i) {

            // Two equal neighbours = a duplicate exists.
            if (nums[i] == nums[i - 1]) {
                return true;
            }
        }

        // No equal neighbours anywhere → all distinct.
        return false;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // Sample with duplicates sprinkled in.
    vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 3};

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    bool r1 = Solution_HashSet().containsDuplicate(nums);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    // --- Approach 2 (needs its own copy; it sorts in place) ---
    vector<int> copy = nums;
    struct rusage b2, a2;
    getrusage(RUSAGE_SELF, &b2);
    auto s2 = chrono::high_resolution_clock::now();
    bool r2 = Solution_SortAdjacent().containsDuplicate(copy);
    auto e2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a2);
    double us2 = chrono::duration_cast<chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long mem2 = (a2.ru_maxrss - b2.ru_maxrss) / 1024;

    cout << "Approach 1 (hash set)          : " << (r1 ? "true" : "false")
         << "  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";
    cout << "Approach 2 (sort + adjacent)   : " << (r2 ? "true" : "false")
         << "  time = " << us2 << " µs  peak-ram-delta = " << mem2 << " MB\n";

    cout << ((r1 == r2) ? "PASS : both approaches agree."
                        : "FAIL : approaches disagree.")
         << "\n";
    return 0;
}