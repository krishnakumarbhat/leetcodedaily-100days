/*
 * LeetCode 1: Two Sum
 * Link: https://leetcode.com/problems/two-sum/
 * Difficulty: Easy
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Iterate through each element in the array. For each element, iterate through
// the remaining elements to check if their sum equals the target.
// Time: O(n^2)  Space: O(1)
class Solution_v1 {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++)
            for (int j = i + 1; j < nums.size(); j++)
                if (nums[i] + nums[j] == target)
                    return {i, j};
        return {};
    }
};

// ============= Variation 2: Two-pass Hash Map =============
// Algorithm: First pass: map each element to its index.
// Second pass: for each element, check if 'target - element' exists in map.
// Time: O(n)  Space: O(n)
class Solution_v2 {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> mp;
        for (int i = 0; i < nums.size(); i++)
            mp[nums[i]] = i;
        for (int i = 0; i < nums.size(); i++) {
            int comp = target - nums[i];
            if (mp.count(comp) && mp[comp] != i)
                return {i, mp[comp]};
        }
        return {};
    }
};

// ============= Variation 3: One-pass Hash Map =============
// Algorithm: Store seen elements in a hash map as we iterate. 
// If target - current element exists in map, we found the pair immediately.
// Time: O(n)  Space: O(n)
class Solution_v3 {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> mp;
        for (int i = 0; i < nums.size(); i++) {
            int comp = target - nums[i];
            if (mp.count(comp))
                return {mp[comp], i};
            mp[nums[i]] = i;
        }
        return {};
    }
};

// ============= Variation 4: Sort + Two Pointers =============
// Algorithm: Store values with original indices and sort. Use left pointer at start
// and right pointer at end. Increment left if sum is too small, decrement right if too large.
// Time: O(n log n)  Space: O(n)
class Solution_v4 {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<pair<int, int>> sorted_nums;
        for (int i = 0; i < nums.size(); i++) {
            sorted_nums.push_back({nums[i], i});
        }
        sort(sorted_nums.begin(), sorted_nums.end());
        int l = 0, r = sorted_nums.size() - 1;
        while (l < r) {
            int current_sum = sorted_nums[l].first + sorted_nums[r].first;
            if (current_sum == target) {
                return {sorted_nums[l].second, sorted_nums[r].second};
            } else if (current_sum < target) {
                l++;
            } else {
                r--;
            }
        }
        return {};
    }
};

int main() {
    vector<int> nums = {2, 7, 11, 15, 1, 3, 5, 8, 4, 6};
    int target = 9;

    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v1().twoSum(data, target);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Brute Force): result=[" << res[0] << "," << res[1] << "], time = " << us << " µs" << endl;
    }
    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v2().twoSum(data, target);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Two-pass HashMap): result=[" << res[0] << "," << res[1] << "], time = " << us << " µs" << endl;
    }
    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v3().twoSum(data, target);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var3 (One-pass HashMap): result=[" << res[0] << "," << res[1] << "], time = " << us << " µs" << endl;
    }
    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v4().twoSum(data, target);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var4 (Sort + Two Pointers): result=[" << res[0] << "," << res[1] << "], time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 0.414 µs
// var2 mem = N/A and time = 6.86 µs
// var3 mem = N/A and time = 0.653 µs
// var4 mem = N/A and time = 1.254 µs
