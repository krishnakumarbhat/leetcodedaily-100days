/*
 * LeetCode 347: Top K Frequent Elements
 * Link: https://leetcode.com/problems/top-k-frequent-elements/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Sorting =============
// Algorithm: Hash map to count occurrences. Store (freq, value) in a vector.
// Sort the vector in descending order. Return the top k values.
// Time: O(n log n)  Space: O(n)
class Solution_v1 {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        for (int n : nums) count[n]++;
        vector<pair<int, int>> freq;
        for (auto& p : count) freq.push_back({p.second, p.first});
        sort(freq.rbegin(), freq.rend());
        vector<int> result;
        for (int i = 0; i < k; i++) result.push_back(freq[i].second);
        return result;
    }
};

// ============= Variation 2: Min Heap =============
// Algorithm: Count occurrences. Push pair(freq, val) into a min-priority queue.
// When size > k, pop the smallest frequency. The remaining k are the largest.
// Time: O(n log k)  Space: O(n)
class Solution_v2 {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        for (int n : nums) count[n]++;
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
        for (auto& p : count) {
            pq.push({p.second, p.first});
            if (pq.size() > k) pq.pop();
        }
        vector<int> result;
        while (!pq.empty()) { result.push_back(pq.top().second); pq.pop(); }
        return result;
    }
};

// ============= Variation 3: Bucket Sort =============
// Algorithm: Count frequencies. Use a 2D array (buckets) where the index is the 
// frequency and the value is a list of elements. Iterate backwards from n.
// Time: O(n)  Space: O(n)
class Solution_v3 {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        for (int n : nums) count[n]++;
        vector<vector<int>> buckets(nums.size() + 1);
        for (auto& p : count) buckets[p.second].push_back(p.first);
        vector<int> result;
        for (int i = buckets.size() - 1; i >= 0 && result.size() < k; i--)
            for (int n : buckets[i]) {
                result.push_back(n);
                if (result.size() == k) return result;
            }
        return result;
    }
};

int main() {
    vector<int> nums = {1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 5};
    int k = 2;

    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v1().topKFrequent(data, k);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Sorting): time = " << us << " µs" << endl;
    }
    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v2().topKFrequent(data, k);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Min Heap): time = " << us << " µs" << endl;
    }
    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v3().topKFrequent(data, k);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var3 (Bucket Sort): time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 8.592 µs
// var2 mem = N/A and time = 2.329 µs
// var3 mem = N/A and time = 2.492 µs
