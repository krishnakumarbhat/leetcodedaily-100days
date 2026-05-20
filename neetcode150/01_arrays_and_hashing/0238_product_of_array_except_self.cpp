/*
 * LeetCode 238: Product of Array Except Self
 * Link: https://leetcode.com/problems/product-of-array-except-self/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Nested iterations. For every index, loop through everyone else and
// multiply accumulating into the answer. Avoid multiplying by self.
// Time: O(n^2)  Space: O(n)
class Solution_v1 {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, 1);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (i != j) result[i] *= nums[j];
        return result;
    }
};

// ============= Variation 2: Prefix & Suffix Arrays =============
// Algorithm: Build an array of products matching all elements to the left.
// Build another for all elements right. Multiply left[i] and right[i].
// Time: O(n)  Space: O(n)
class Solution_v2 {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> prefix(n, 1), suffix(n, 1), result(n);
        for (int i = 1; i < n; i++) prefix[i] = prefix[i-1] * nums[i-1];
        for (int i = n-2; i >= 0; i--) suffix[i] = suffix[i+1] * nums[i+1];
        for (int i = 0; i < n; i++) result[i] = prefix[i] * suffix[i];
        return result;
    }
};

// ============= Variation 3: Optimized O(1) Space =============
// Algorithm: Use the output array to store the prefix product. Then iterate
// again backwards storing a running right multiplier and multiply it in-place.
// Time: O(n)  Space: O(1)
class Solution_v3 {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, 1);
        int prefix = 1;
        for (int i = 0; i < n; i++) { result[i] = prefix; prefix *= nums[i]; }
        int suffix = 1;
        for (int i = n-1; i >= 0; i--) { result[i] *= suffix; suffix *= nums[i]; }
        return result;
    }
};

int main() {
    vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    auto run = [&](auto sol, string name, int var) {
        vector<int> data = nums;
        auto start = chrono::high_resolution_clock::now();
        auto res = sol.productExceptSelf(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var" << var << " (" << name << "): time = " << us << " µs" << endl;
    };

    run(Solution_v1(), "Brute Force", 1);
    run(Solution_v2(), "Prefix+Suffix", 2);
    run(Solution_v3(), "Optimized O(1)", 3);
    return 0;
}

// var1 mem = N/A and time = 0.933 µs
// var2 mem = N/A and time = 0.665 µs
// var3 mem = N/A and time = 0.291 µs
