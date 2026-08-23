/*
 * =====================================================================
 * LeetCode 1 : Two Sum                                             (Easy)
 * https://leetcode.com/problems/two-sum/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of integers `nums` and an integer `target`, return
 *   the indices of the two numbers that add up to `target`.
 *   Exactly ONE valid answer exists. You may not use the same element
 *   twice.
 * ---------------------------------------------------------------------
 * INTUITION
 *   For every number `num` we only ever care about ONE thing:
 *   "have I already seen its partner `target - num` earlier?"
 *   A hash map turns that question from an O(n) scan ("which index
 *   holds my partner?") into an O(1) lookup ("did I store it?").
 * ---------------------------------------------------------------------
 * APPROACH 1 — One-pass hash map (BEST)
 *   Walk the array once. Before inserting `num`, check whether its
 *   complement `target - num` is already in the map. If yes → done.
 *   If no → store `num -> index` for future elements to find.
 *   Time  Complexity : O(n)  — every element visited exactly once,
 *                        every hash-map op is O(1) average.
 *   Space Complexity : O(n)  — the map stores at most n entries.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort + two pointers (no hash map)
 *   Copy (value, originalIndex) pairs and sort. Place `l` at the
 *   smallest value and `r` at the largest. Sum them:
 *     • sum == target → found (read original indices).
 *     • sum  < target → move `l` right (need a bigger partner).
 *     • sum  > target → move `r` left  (need a smaller partner).
 *   Time  Complexity : O(n log n) — dominated by the sort.
 *   Space Complexity : O(n)       — the sorted copy of pairs.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — which hash map and WHY
 *   C++ : std::unordered_map = separate chaining (bucket of linked
 *         list of colliding keys). O(1) average per op. std::map is
 *         a red-black BST with O(log n) ops — only better if you
 *         need ordered iteration / range queries (not needed here).
 *   Python : dict = open addressing with linear probing:
 *         h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
 *         Collisions walk to the next free slot; all data lives in
 *         ONE contiguous array → excellent cache locality, very
 *         low memory overhead. Perfect for this problem.
 * =====================================================================
 */

#include <vector>        // std::vector — dynamic array for nums/answers
#include <unordered_map> // std::unordered_map — hash table, O(1) ops
#include <algorithm>     // std::sort — used by approach 2
#include <utility>       // std::pair — (value, index) bundles in approach 2
#include <chrono>        // std::chrono — high-resolution timing for benchmark
#include <iostream>      // std::cout — printing benchmark results
#include <sys/resource.h>// getrusage — peak RAM measurement for benchmark

using namespace std;     // allows writing vector instead of std::vector

/* =====================================================================
 * APPROACH 1 : One-pass hash map
 * ===================================================================== */
class Solution_OnePassHashmap {
public:
    /*
     * Purpose : Return the two indices whose values sum to `target`.
     * Inputs  : nums   — array of integers to search inside.
     *           target — the sum we must form with two distinct elements.
     * Output  : vector<int> of size 2 with the answer indices.
     */
    vector<int> twoSum(const vector<int>& nums, int target) {
        // seen : value -> index  (hash table with O(1) insert + lookup)
        unordered_map<int, int> seen;

        // Walk every element exactly once — this is the single O(n) pass.
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {

            // complement = the partner that would complete the sum.
            int need = target - nums[i];

            // Check the table BEFORE inserting: the partner must come
            // from an EARLIER index, so we never reuse the same element.
            auto it = seen.find(need);
            if (it != seen.end()) {

                // found → answer = (partner's stored index, current index)
                return {it->second, i};
            }

            // Partner not seen yet → remember this value for the future.
            seen[nums[i]] = i;
        }

        // Problem guarantees an answer, but the compiler needs a return.
        return {};
    }
};

/* =====================================================================
 * APPROACH 2 : Sort + two pointers (no hash map at all)
 * ===================================================================== */
class Solution_SortTwoPointers {
public:
    /*
     * Purpose : Return the two indices whose values sum to `target`.
     * Inputs  : nums   — array of integers to search inside.
     *           target — the sum we must form with two distinct elements.
     * Output  : vector<int> of size 2 with the answer indices.
     */
    vector<int> twoSum(const vector<int>& nums, int target) {
        // Bundle every value with its ORIGINAL index — sorting would
        // otherwise destroy the indices we are asked to return.
        vector<pair<int, int>> pairs;
        pairs.reserve(nums.size());
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            pairs.emplace_back(nums[i], i);
        }

        // Sort by value so that values are laid out ascending in memory.
        // This is the O(n log n) step that costs us the best time bound.
        sort(pairs.begin(), pairs.end());

        // Two pointers: l hunts from the small end, r from the big end.
        int l = 0;
        int r = static_cast<int>(pairs.size()) - 1;

        // The pointers converge, so we inspect O(n) pairs total.
        while (l < r) {

            // Current sum of the two pointed-to values.
            int sum = pairs[l].first + pairs[r].first;

            if (sum == target) {
                // Exact match → hand back the original indices.
                return {pairs[l].second, pairs[r].second};
            }
            if (sum < target) {
                // Sum too small → the only way to grow it is to move the
                // left pointer toward bigger values.
                ++l;
            } else {
                // Sum too big → shrink it by pulling the right pointer
                // toward smaller values.
                --r;
            }
        }

        // Unreachable per problem statement; keeps the compiler quiet.
        return {};
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Fixed sample used by the official examples, plus extra elements
    // so the benchmark is not trivially fast.
    vector<int> nums = {2, 7, 11, 15, 3, 6, 1, 4, 9, 8, 5, 10};
    int target = 9; // answer: indices {0, 1} → 2 + 7 = 9

    // --- Approach 1 timing ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = chrono::high_resolution_clock::now();
    vector<int> r1 = Solution_OnePassHashmap().twoSum(nums, target);
    auto end_1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    // Convert nanoseconds to microseconds for human-friendly output.
    double us_1 = chrono::duration_cast<chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    // ru_maxrss is cumulative peak → the delta is what THIS run consumed.
    long mem_1 = (after_1.ru_maxrss - before_1.ru_maxrss) / 1024; // KB -> MB

    // --- Approach 2 timing ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = chrono::high_resolution_clock::now();
    vector<int> r2 = Solution_SortTwoPointers().twoSum(nums, target);
    auto end_2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    double us_2 = chrono::duration_cast<chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = (after_2.ru_maxrss - before_2.ru_maxrss) / 1024;

    // Print both results and confirm they agree with each other.
    cout << "Approach 1 (one-pass hash map) : [" << r1[0] << "," << r1[1]
         << "]  time = " << us_1 << " µs  peak-ram-delta = " << mem_1 << " MB\n";
    cout << "Approach 2 (sort + two pointers): [" << r2[0] << "," << r2[1]
         << "]  time = " << us_2 << " µs  peak-ram-delta = " << mem_2 << " MB\n";

    // Sanity check: each answer must (a) use distinct indices and
    // (b) actually sum to the target — the real acceptance criteria.
    auto valid = [&](const vector<int>& r) {
        return r.size() == 2 &&
               r[0] != r[1] &&
               nums[r[0]] + nums[r[1]] == target;
    };
    bool ok = valid(r1) && valid(r2);
    cout << (ok ? "PASS : both approaches return valid pairs summing to target."
                : "FAIL : at least one answer is wrong.") << "\n";

    return 0;
}