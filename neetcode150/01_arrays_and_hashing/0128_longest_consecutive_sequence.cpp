/*
 * LeetCode 128: Longest Consecutive Sequence
 * Link: https://leetcode.com/problems/longest-consecutive-sequence/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Sorting =============
// Algorithm: Sort the array. Iterate and track the consecutive streak length.
// If numbers are the same, skip. If difference > 1, reset streak.
// Time: O(n log n)  Space: O(1)
class Solution_v1 {
public:
    int longestConsecutive(vector<int>& nums) {
        if (nums.empty()) return 0;
        sort(nums.begin(), nums.end());
        int longest = 1, current = 1;
        for (int i = 1; i < nums.size(); i++) {
            if (nums[i] == nums[i-1]) continue;
            if (nums[i] == nums[i-1] + 1) current++;
            else current = 1;
            longest = max(longest, current);
        }
        return longest;
    }
};

// ============= Variation 2: Hash Set =============
// Algorithm: Convert array to unordered_set. Loop through the set. Only start
// counting sequence length if `num - 1` doesn't exist (i.e. it is a sequence start).
// Time: O(n)  Space: O(n)
class Solution_v2 {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> s(nums.begin(), nums.end());
        int longest = 0;
        for (int num : s) {
            if (!s.count(num - 1)) {
                int curr = num, streak = 1;
                while (s.count(curr + 1)) { curr++; streak++; }
                longest = max(longest, streak);
            }
        }
        return longest;
    }
};

// ============= Variation 3: Union Find =============
// Algorithm: Map numbers to themselves in a parent array. Union a number with its
// `num-1` and `num+1` counterparts. Track group sizes. Largest group is the answer.
// Time: O(n α(n))  Space: O(n)
class Solution_v3 {
public:
    unordered_map<int, int> parent, sz;

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    void unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return;
        if (sz[px] < sz[py]) swap(px, py);
        parent[py] = px;
        sz[px] += sz[py];
    }

    int longestConsecutive(vector<int>& nums) {
        parent.clear(); sz.clear();
        for (int num : nums) {
            if (parent.count(num)) continue;
            parent[num] = num; sz[num] = 1;
            if (parent.count(num - 1)) unite(num, num - 1);
            if (parent.count(num + 1)) unite(num, num + 1);
        }
        int longest = 0;
        for (auto& p : sz) longest = max(longest, p.second);
        return longest;
    }
};

int main() {
    vector<int> nums = {100, 4, 200, 1, 3, 2, 5, 6, 7, 8};

    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        int res = Solution_v1().longestConsecutive(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Sorting): result=" << res << ", time = " << us << " µs" << endl;
    }
    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        int res = Solution_v2().longestConsecutive(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Hash Set): result=" << res << ", time = " << us << " µs" << endl;
    }
    {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        int res = Solution_v3().longestConsecutive(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var3 (Union Find): result=" << res << ", time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 0.81 µs
// var2 mem = N/A and time = 10.519 µs
// var3 mem = N/A and time = 4.88 µs
