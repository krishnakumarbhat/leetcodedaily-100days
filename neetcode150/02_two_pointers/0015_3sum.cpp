/*
 * =====================================================================
 * LeetCode 15 : 3Sum                                              (Medium)
 * https://leetcode.com/problems/3sum/
 * Category   : Two Pointers
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer array nums, return ALL unique triplets [a,b,c]
 *   with a + b + c = 0. "Unique" means no duplicate triplet: (1,-1,0)
 *   and (-1,0,1) are the same answer. n can reach 3000 → O(n³) is
 *   way too slow.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Fix one element a = nums[i]. The problem collapses to the 2-sum
 *   question "find b + c = -a" on the remaining slice — and 2-sum on
 *   a SORTED array is solved in O(n) with two pointers. Sorting also
 *   manufactures uniqueness for free: equal values become adjacent,
 *   so skipping consecutive duplicates kills mirrored triplets.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sort + two pointers (BEST, O(n²))
 *   Sort nums. For each pivot i (skipping duplicate pivots):
 *     • target = -nums[i]; l = i+1, r = n-1.
 *     • Sum nums[l] + nums[r]: < target → ++l (need bigger), > target
 *       → --r (need smaller), == target → record, then skip duplicates
 *       on BOTH sides before moving on.
 *     • nums[i] > 0 → early exit: three positives can never sum to 0.
 *   Time  Complexity : O(n²)  — n pivots × O(n) two-pointer walk.
 *   Space Complexity : O(1)   extra (sort is in-place; output aside).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Hash map with dedupe set (O(n²) time, O(n) space)
 *   Same pivot loop, but the inner 2-sum uses a hash map of
 *   value → index: for each j, look up -(nums[i]+nums[j]). Insert
 *   triplets into a Set<string> ("a,b,c" joined) to kill duplicates.
 *   Time  Complexity : O(n²)  — n pivots × O(n) hash lookups.
 *   Space Complexity : O(n)   — the per-pivot hash table + dedupe set.
 * ---------------------------------------------------------------------
 * DEEP DIVE — how sorting kills duplicate triplets
 *   With sorted input, any triplet can be emitted in sorted order
 *   (a ≤ b ≤ c). Two different (i,j,k) index triples produce the same
 *   sorted VALUE triple only when the same values repeat — and the
 *   skip-duplicates rule jumps PAST those repeats, so the exact same
 *   value triple can never be recorded twice. Python's set-of-tuples
 *   achieves the same by hashing the sorted tuple; the hash table
 *   underneath (dict = open addressing, linear probing) is exactly:
 *       h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
 *   while C++ unordered_set chains colliding keys per bucket.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing PASS/FAIL + benchmarks
#include <vector>        // std::vector — the array + result triplets
#include <string>        // std::string — dedupe keys for approach 2
#include <unordered_set> // std::unordered_set — chained-bucket dedupe
#include <algorithm>     // std::sort — the O(n log n) preprocessing
#include <chrono>        // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Sort + two pointers
 * ===================================================================== */
class Solution_SortTwoPointers {
public:
    /*
     * Purpose : Return all unique value-triplets summing to zero.
     * Inputs  : nums — array of integers to search inside.
     * Output  : vector<vector<int>> — sorted triplets, no duplicates.
     */
    std::vector<std::vector<int>> threeSum(std::vector<int>& nums) {
        std::vector<std::vector<int>> result;
        int n = static_cast<int>(nums.size());
        if (n < 3) {
            return result;
        }

        // Sorting is the ONE preprocessing step that buys both the
        // two-pointer walk AND the duplicate elimination.
        std::sort(nums.begin(), nums.end());

        for (int i = 0; i < n - 2; ++i) {
            // The array is sorted: if the smallest remaining element is
            // already positive, no later triplet can ever sum to zero.
            if (nums[i] > 0) {
                break;
            }
            // Skip duplicate pivots — the same 'a' gives the same triplets.
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }

            // Classic sorted 2-sum on the slice right of i, target = -a.
            int target = -nums[i];
            int l = i + 1;
            int r = n - 1;
            while (l < r) {
                int sum = nums[l] + nums[r];
                if (sum < target) {
                    ++l;                 // pair too small → need a bigger b
                } else if (sum > target) {
                    --r;                 // pair too big → need a smaller c
                } else {
                    // b + c == -a → record the triplet in sorted order.
                    result.push_back({nums[i], nums[l], nums[r]});
                    // Skip duplicate b AND duplicate c — the pair of
                    // indices may change, but the VALUE triple would be
                    // identical, so it must not be recorded again.
                    while (l < r && nums[l] == nums[l + 1]) {
                        ++l;
                    }
                    while (l < r && nums[r] == nums[r - 1]) {
                        --r;
                    }
                    ++l;
                    --r;
                }
            }
        }
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : Pivot + hash map 2-sum with a dedupe set
 * ===================================================================== */
class Solution_HashMapDedupe {
public:
    /*
     * Purpose : Return all unique value-triplets summing to zero.
     * Inputs  : nums — array of integers to search inside.
     * Output  : vector<vector<int>> — sorted triplets, no duplicates.
     */
    std::vector<std::vector<int>> threeSum(std::vector<int>& nums) {
        std::vector<std::vector<int>> result;
        int n = static_cast<int>(nums.size());
        if (n < 3) {
            return result;
        }

        // Sort for ONLY one reason: the dedupe key "a,b,c" must be
        // canonical, so every triplet is serialized in sorted order.
        std::sort(nums.begin(), nums.end());

        // Dedupe set of canonical keys — separate chaining under the hood.
        std::unordered_set<std::string> seen;

        for (int i = 0; i < n - 2; ++i) {
            if (nums[i] > 0) {
                break;
            }
            // seen-value map for the inner 2-sum: value -> its index.
            std::unordered_set<int> partner;

            for (int j = i + 1; j < n; ++j) {
                // The complement that would complete 0 with nums[i]+nums[j].
                int need = -(nums[i] + nums[j]);
                if (partner.count(need)) {
                    // Canonical sorted triple (nums[i] ≤ need ≤ nums[j]
                    // because we scan j left→right) → unique key.
                    std::string key = std::to_string(nums[i]) + "," +
                                      std::to_string(need) + "," +
                                      std::to_string(nums[j]);
                    if (seen.insert(key).second) {
                        result.push_back({nums[i], need, nums[j]});
                    }
                }
                partner.insert(nums[j]);
            }
        }
        return result;
    }
};

/* =====================================================================
 * BENCHMARK — verify both solutions on real test cases + time/RAM
 * ===================================================================== */
int main() {
    // Case 1: official example — two unique triplets.
    // Case 2: only zeros — exactly ONE triplet, not three.
    // Case 3: no triplet sums to zero (all distinct, small).
    struct TestCase { std::vector<int> nums; size_t expectedCount; };
    std::vector<TestCase> tests = {
        {{-1, 0, 1, 2, -1, -4}, 2},
        {{0, 0, 0, 0}, 1},
        {{1, 2, 3, 4, 5}, 0}
    };

    // Aggregate time + peak-RAM across all cases, per approach.
    long time_us[2] = {0, 0};
    long peak_kb[2] = {0, 0};
    bool allPass = true;

    for (size_t t = 0; t < tests.size(); ++t) {
        struct rusage before, after;
        std::vector<int> copy1 = tests[t].nums;
        std::vector<int> copy2 = tests[t].nums;

        // --- Approach 1: time + peak memory (ru_maxrss is KB on Linux) ---
        getrusage(RUSAGE_SELF, &before);
        auto s1 = std::chrono::steady_clock::now();
        auto r1 = Solution_SortTwoPointers().threeSum(copy1);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        time_us[0] += std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000;
        peak_kb[0] = std::max(peak_kb[0], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        // --- Approach 2: same instrumentation ---
        getrusage(RUSAGE_SELF, &before);
        auto s2 = std::chrono::steady_clock::now();
        auto r2 = Solution_HashMapDedupe().threeSum(copy2);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        time_us[1] += std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000;
        peak_kb[1] = std::max(peak_kb[1], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        // Verify: count matches AND every triplet really sums to zero.
        bool ok = (r1.size() == tests[t].expectedCount) && (r2.size() == tests[t].expectedCount);
        for (const auto& trip : r1) {
            ok = ok && (trip[0] + trip[1] + trip[2] == 0);
        }
        for (const auto& trip : r2) {
            ok = ok && (trip[0] + trip[1] + trip[2] == 0);
        }
        allPass = allPass && ok;
        std::cout << "Test " << (t + 1) << ": sort2Ptr=" << r1.size()
                  << " hashMap=" << r2.size()
                  << " expected=" << tests[t].expectedCount
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "---\n"
              << "Approach 1 (sort + two pointers) : " << time_us[0] << " µs total, peak " << peak_kb[0] << " KB\n"
              << "Approach 2 (pivot + hash map)    : " << time_us[1] << " µs total, peak " << peak_kb[1] << " KB\n"
              << (allPass ? "PASS : all cases" : "FAIL : at least one case") << "\n";
    return allPass ? 0 : 1;
}