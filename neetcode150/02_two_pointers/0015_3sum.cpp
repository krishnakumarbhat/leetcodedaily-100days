/*
 * LeetCode 15: 3Sum
 * Link: https://leetcode.com/problems/3sum/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Iterate through every triplet pair (i, j, k) to see if they add to 0. 
// Use an std::set to record result vectors which inherently ignores duplicates.
// Time: O(n^3)  Space: O(n)
class Solution_v1 {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        set<vector<int>> res;
        for (int i = 0; i < (int)nums.size(); i++)
            for (int j = i+1; j < (int)nums.size(); j++)
                for (int k = j+1; k < (int)nums.size(); k++)
                    if (nums[i]+nums[j]+nums[k]==0) res.insert({nums[i],nums[j],nums[k]});
        return vector<vector<int>>(res.begin(), res.end());
    }
};

// ============= Variation 2: Two Pointers =============
// Algorithm: Sort array first. Loop through to fix one number. Use two pointers 
// starting at i+1 and n-1 moving inwards to find a zero sum target.
// Time: O(n^2)  Space: O(1)
class Solution_v2 {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> result;
        for (int i = 0; i < (int)nums.size()-2; i++) {
            if (i > 0 && nums[i]==nums[i-1]) continue;
            int l = i+1, r = nums.size()-1;
            while (l < r) {
                int s = nums[i]+nums[l]+nums[r];
                if (s == 0) {
                    result.push_back({nums[i],nums[l],nums[r]});
                    while (l<r && nums[l]==nums[l+1]) l++;
                    while (l<r && nums[r]==nums[r-1]) r--;
                    l++; r--;
                } else if (s < 0) l++;
                else r--;
            }
        }
        return result;
    }
};

int main() {
    vector<int> nums = {-1, 0, 1, 2, -1, -4, 3, -2, 5, -3};
    {
        auto d = nums;
        auto s = chrono::high_resolution_clock::now();
        auto r = Solution_v1().threeSum(d);
        auto e = chrono::high_resolution_clock::now();
        cout << "var1 (Brute Force): triplets=" << r.size() << ", time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    {
        auto d = nums;
        auto s = chrono::high_resolution_clock::now();
        auto r = Solution_v2().threeSum(d);
        auto e = chrono::high_resolution_clock::now();
        cout << "var2 (Two Pointers): triplets=" << r.size() << ", time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    return 0;
}
// var1 mem = N/A and time = 11.887 µs
// var2 mem = N/A and time = 2.739 µs
