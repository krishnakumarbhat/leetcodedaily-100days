/*
 * LeetCode 167: Two Sum II - Input Array Is Sorted
 * Link: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Loop through every pair sequentially starting from index 0 mapping 
// values. If target sum is struck, return indices mapping natively to +1 format.
// Time: O(n^2)  Space: O(1)
class Solution_v1 {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        for (int i = 0; i < numbers.size(); i++)
            for (int j = i + 1; j < numbers.size(); j++)
                if (numbers[i] + numbers[j] == target)
                    return {i + 1, j + 1};
        return {};
    }
};

// ============= Variation 2: Binary Search =============
// Algorithm: Iterate through every element `i`. Since it is sorted, run standard 
// binary bounds halving for remaining elements matching specifically `target - val[i]`.
// Time: O(n log n)  Space: O(1)
class Solution_v2 {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        for (int i = 0; i < numbers.size(); i++) {
            int comp = target - numbers[i];
            int lo = i + 1, hi = numbers.size() - 1;
            while (lo <= hi) {
                int mid = lo + (hi - lo) / 2;
                if (numbers[mid] == comp) return {i + 1, mid + 1};
                else if (numbers[mid] < comp) lo = mid + 1;
                else hi = mid - 1;
            }
        }
        return {};
    }
};

// ============= Variation 3: Two Pointers =============
// Algorithm: Begin at extremes. Shrinking bounds natively depending upon arithmetic.
// A sum larger than target -> decrement `r`. Smaller -> increment `l`.
// Time: O(n)  Space: O(1)
class Solution_v3 {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int l = 0, r = numbers.size() - 1;
        while (l < r) {
            int s = numbers[l] + numbers[r];
            if (s == target) return {l + 1, r + 1};
            else if (s < target) l++;
            else r--;
        }
        return {};
    }
};

int main() {
    vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 15};
    int target = 17;
    {
        auto d = numbers;
        auto s = chrono::high_resolution_clock::now();
        auto r = Solution_v1().twoSum(d, target);
        auto e = chrono::high_resolution_clock::now();
        cout << "var1 (Brute Force): [" << r[0] << "," << r[1] << "], time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    {
        auto d = numbers;
        auto s = chrono::high_resolution_clock::now();
        auto r = Solution_v2().twoSum(d, target);
        auto e = chrono::high_resolution_clock::now();
        cout << "var2 (BinSearch): [" << r[0] << "," << r[1] << "], time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    {
        auto d = numbers;
        auto s = chrono::high_resolution_clock::now();
        auto r = Solution_v3().twoSum(d, target);
        auto e = chrono::high_resolution_clock::now();
        cout << "var3 (Two Pointers): [" << r[0] << "," << r[1] << "], time = " << chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0 << " µs" << endl;
    }
    return 0;
}
// var1 mem = N/A and time = 0.715 µs
// var2 mem = N/A and time = 0.246 µs
// var3 mem = N/A and time = 0.128 µs
