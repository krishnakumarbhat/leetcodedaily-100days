/*
 * LeetCode 217: Contains Duplicate
 * Link: https://leetcode.com/problems/contains-duplicate/
 * Difficulty: Easy
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Two nested loops comparing every element to every other element.
// Time: O(n^2)  Space: O(1)
class Solution_v1 {
public:
    bool containsDuplicate(vector<int>& nums) {
        for (int i = 0; i < nums.size(); i++)
            for (int j = i + 1; j < nums.size(); j++)
                if (nums[i] == nums[j]) return true;
        return false;
    }
};

// ============= Variation 2: Sorting =============
// Algorithm: Sort the input array. Duplicates will end up adjacent.
// Scan checking if adjacent elements are equal.
// Time: O(n log n)  Space: O(1)
class Solution_v2 {
public:
    bool containsDuplicate(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        for (int i = 1; i < nums.size(); i++)
            if (nums[i] == nums[i - 1]) return true;
        return false;
    }
};

// ============= Variation 3: Hash Set =============
// Algorithm: Maintain an unordered_set. Add elements to the set as we iterate.
// If an element is already in the set, a duplicate is found.
// Time: O(n)  Space: O(n)
class Solution_v3 {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.count(num)) return true;
            seen.insert(num);
        }
        return false;
    }
};

int main() {
    vector<int> test_data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 1};

    // Variation 1
    {
        vector<int> data = test_data;
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v1().containsDuplicate(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Brute Force): result=" << res << ", time = " << us << " µs" << endl;
    }
    // Variation 2
    {
        vector<int> data = test_data;
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v2().containsDuplicate(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Sorting): result=" << res << ", time = " << us << " µs" << endl;
    }
    // Variation 3
    {
        vector<int> data = test_data;
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v3().containsDuplicate(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var3 (Hash Set): result=" << res << ", time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 0.251 µs
// var2 mem = N/A and time = 0.327 µs
// var3 mem = N/A and time = 6.404 µs
