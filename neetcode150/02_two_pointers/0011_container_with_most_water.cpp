/*
 * LeetCode 11: Container With Most Water
 * Link: https://leetcode.com/problems/container-with-most-water/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Loop through every pair of left and right boundaries (i, j).
// Area is the smallest boundary height times length width (j - i). Maximize.
// Time: O(n^2)  Space: O(1)
class Solution_v1 {
public:
    int maxArea(vector<int>& height) {
        int mx = 0;
        for (int i = 0; i < height.size(); i++)
            for (int j = i+1; j < height.size(); j++)
                mx = max(mx, min(height[i], height[j]) * (j - i));
        return mx;
    }
};

// ============= Variation 2: Two Pointers =============
// Algorithm: Put one pointer on the left and one on the right. Track the max
// area formed by these lines, then step the shorter boundary inwards.
// Time: O(n)  Space: O(1)
class Solution_v2 {
public:
    int maxArea(vector<int>& height) {
        int l = 0, r = height.size() - 1, mx = 0;
        while (l < r) {
            mx = max(mx, min(height[l], height[r]) * (r - l));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return mx;
    }
};

int main() {
    vector<int> height = {1, 8, 6, 2, 5, 4, 8, 3, 7};
    {
        auto d = height;
        auto s = chrono::high_resolution_clock::now();
        int r = Solution_v1().maxArea(d);
        auto e = chrono::high_resolution_clock::now();
        cout << "var1 (Brute Force): result=" << r << ", time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    {
        auto d = height;
        auto s = chrono::high_resolution_clock::now();
        int r = Solution_v2().maxArea(d);
        auto e = chrono::high_resolution_clock::now();
        cout << "var2 (Two Pointers): result=" << r << ", time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    return 0;
}
// var1 mem = N/A and time = 0.558 µs
// var2 mem = N/A and time = 0.179 µs
