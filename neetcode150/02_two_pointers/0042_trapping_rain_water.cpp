/*
 * LeetCode 42: Trapping Rain Water
 * Link: https://leetcode.com/problems/trapping-rain-water/
 * Difficulty: Hard
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Prefix Max Arrays =============
// Algorithm: Build an array tracing max heights to the left, and another tracking
// max heights to the right. Use these to find trapped water locally per bar.
// Time: O(n)  Space: O(n)
class Solution_v1 {
public:
    int trap(vector<int>& height) {
        int n = height.size();
        if (n == 0) return 0;
        vector<int> left_max(n), right_max(n);
        left_max[0] = height[0];
        for (int i = 1; i < n; i++) left_max[i] = max(left_max[i-1], height[i]);
        right_max[n-1] = height[n-1];
        for (int i = n-2; i >= 0; i--) right_max[i] = max(right_max[i+1], height[i]);
        int water = 0;
        for (int i = 0; i < n; i++) water += min(left_max[i], right_max[i]) - height[i];
        return water;
    }
};

// ============= Variation 2: Two Pointers =============
// Algorithm: Squeeze inward from l and r. Rely on the guaranteed fact that water 
// level is bound by the smaller height maximums. Saves allocating prefix arrays.
// Time: O(n)  Space: O(1)
class Solution_v2 {
public:
    int trap(vector<int>& height) {
        int l = 0, r = height.size() - 1, lmax = 0, rmax = 0, water = 0;
        while (l < r) {
            if (height[l] < height[r]) {
                lmax = max(lmax, height[l]);
                water += lmax - height[l];
                l++;
            } else {
                rmax = max(rmax, height[r]);
                water += rmax - height[r];
                r--;
            }
        }
        return water;
    }
};

// ============= Variation 3: Stack =============
// Algorithm: Loop indices putting them in a stack so long as heights decrease.
// When encountering a taller height than stack top, pop as a valley and calc volume.
// Time: O(n)  Space: O(n)
class Solution_v3 {
public:
    int trap(vector<int>& height) {
        stack<int> st;
        int water = 0;
        for (int i = 0; i < height.size(); i++) {
            while (!st.empty() && height[i] > height[st.top()]) {
                int top = st.top(); st.pop();
                if (st.empty()) break;
                int dist = i - st.top() - 1;
                int h = min(height[i], height[st.top()]) - height[top];
                water += dist * h;
            }
            st.push(i);
        }
        return water;
    }
};

int main() {
    vector<int> height = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
    {
        auto d = height; auto s = chrono::high_resolution_clock::now();
        int r = Solution_v1().trap(d);
        auto e = chrono::high_resolution_clock::now();
        cout << "var1 (Prefix Max): result=" << r << ", time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    {
        auto d = height; auto s = chrono::high_resolution_clock::now();
        int r = Solution_v2().trap(d);
        auto e = chrono::high_resolution_clock::now();
        cout << "var2 (Two Pointers): result=" << r << ", time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    {
        auto d = height; auto s = chrono::high_resolution_clock::now();
        int r = Solution_v3().trap(d);
        auto e = chrono::high_resolution_clock::now();
        cout << "var3 (Stack): result=" << r << ", time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    return 0;
}
// var1 mem = N/A and time = 3.308 µs
// var2 mem = N/A and time = 0.465 µs
// var3 mem = N/A and time = 3.662 µs
