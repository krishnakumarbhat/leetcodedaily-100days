/*
 * =====================================================================
 * LeetCode 347 : Top K Frequent Elements                         (Medium)
 * https://leetcode.com/problems/top-k-frequent-elements/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer array nums and an integer k, return the k most
 *   frequent elements. Answer may be in any order.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Two separate jobs: (1) count frequencies — a hash map turns this
 *   into O(n); (2) pick the k largest frequencies. Frequencies live
 *   in a small range [1..n], so a frequency-indexed BUCKET ARRAY lets
 *   us collect the top-k in O(n) without any sorting.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Counter + bucket sort (BEST)
 *   buckets[f] = list of numbers appearing exactly f times. Walk
 *   buckets from the highest frequency down, collecting until k.
 *   Time  Complexity : O(n)   — count O(n) + collect O(n).
 *   Space Complexity : O(n)   — map + buckets.
 *   WHY bucket sort beats a heap here: frequency range is bounded by
 *   n, so a counting-style sort runs in linear time; a heap pays
 *   O(log k) per push even when k ≈ n.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Counter + min-heap of size k
 *   Keep a min-heap of (freq, value). New elements evict the smallest
 *   frequency; the heap ends holding the k largest frequencies.
 *   Time  Complexity : O(n log k)   Space Complexity : O(n).
 *   Wins when k ≪ n AND data arrives streaming (no full array in RAM).
 * =====================================================================
 */

#include <vector>          // std::vector — input + buckets
#include <unordered_map>   // std::unordered_map — value → frequency
#include <queue>           // std::priority_queue — min-heap in approach 2
#include <utility>         // std::pair — (frequency, value) heap entries
#include <algorithm>       // std::sort — ordering results for the PASS check
#include <chrono>          // timing for the benchmark
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : Bucket sort on frequencies — O(n)
 * ===================================================================== */
class Solution_BucketSort {
public:
    /*
     * Purpose : Return the k most frequent elements of nums.
     * Inputs  : nums — array of integers; k — how many top elements.
     * Output  : vector with the k most frequent values.
     */
    vector<int> topKFrequent(const vector<int>& nums, int k) {

        // count : value → how many times it appears (single O(n) pass).
        unordered_map<int, int> count;
        for (int num : nums) {
            ++count[num];
        }

        // buckets[f] = values that appear exactly f times.
        // Frequency never exceeds n → bucket array size n+1 is enough.
        vector<vector<int>> buckets(nums.size() + 1);
        for (auto& kv : count) {
            buckets[kv.second].push_back(kv.first);
        }

        // Collect answers from the highest frequency downward.
        vector<int> result;
        for (int f = static_cast<int>(buckets.size()) - 1; f >= 0 && result.size() < static_cast<size_t>(k); --f) {
            // Every value in this bucket is a top-frequency candidate.
            for (int v : buckets[f]) {
                result.push_back(v);

                // Stop the moment we have k elements — O(n) total.
                if (result.size() == static_cast<size_t>(k)) {
                    break;
                }
            }
        }
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : Min-heap of size k — O(n log k)
 * ===================================================================== */
class Solution_MinHeap {
public:
    /*
     * Purpose : Return the k most frequent elements of nums.
     * Inputs  : nums — array of integers; k — how many top elements.
     * Output  : vector with the k most frequent values.
     */
    vector<int> topKFrequent(const vector<int>& nums, int k) {

        // count : value → frequency (same O(n) counting pass as before).
        unordered_map<int, int> count;
        for (int num : nums) {
            ++count[num];
        }

        // Min-heap of size k on (frequency, value): smallest freq on top.
        // C++ priority_queue is a max-heap by default → invert with greater.
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> heap;

        // Push every (freq, value); evict the smallest when over k.
        for (auto& kv : count) {
            heap.push({kv.second, kv.first});

            // Size k+1 → the least frequent of the kept ones must leave.
            if (heap.size() > static_cast<size_t>(k)) {
                heap.pop();
            }
        }

        // The heap now holds exactly the k largest frequencies.
        vector<int> result;
        while (!heap.empty()) {
            result.push_back(heap.top().second);
            heap.pop();
        }
        return result;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // Official example; include many duplicates to make counting real.
    vector<int> nums = {1, 1, 1, 2, 2, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6};
    int k = 3; // expect {4, 5, 1} in some order

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    auto r1 = Solution_BucketSort().topKFrequent(nums, k);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    // --- Approach 2 ---
    struct rusage b2, a2;
    getrusage(RUSAGE_SELF, &b2);
    auto s2 = chrono::high_resolution_clock::now();
    auto r2 = Solution_MinHeap().topKFrequent(nums, k);
    auto e2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a2);
    double us2 = chrono::duration_cast<chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long mem2 = (a2.ru_maxrss - b2.ru_maxrss) / 1024;

    cout << "Approach 1 (bucket sort)      : [";
    for (size_t i = 0; i < r1.size(); ++i) cout << (i ? "," : "") << r1[i];
    cout << "]  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";
    cout << "Approach 2 (min-heap k)       : [";
    for (size_t i = 0; i < r2.size(); ++i) cout << (i ? "," : "") << r2[i];
    cout << "]  time = " << us2 << " µs  peak-ram-delta = " << mem2 << " MB\n";

    // Both answers must contain the same elements (order is free).
    sort(r1.begin(), r1.end());
    sort(r2.begin(), r2.end());
    cout << ((r1 == r2) ? "PASS : both approaches agree."
                        : "FAIL : approaches disagree.")
         << "\n";
    return 0;
}