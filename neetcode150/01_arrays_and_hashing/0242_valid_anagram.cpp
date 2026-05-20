/*
 * LeetCode 242: Valid Anagram
 * Link: https://leetcode.com/problems/valid-anagram/
 * Difficulty: Easy
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Sorting =============
// Algorithm: Sort both strings. Anagrams must match exactly when sorted.
// Time: O(n log n)  Space: O(n)
class Solution_v1 {
public:
    bool isAnagram(string s, string t) {
        sort(s.begin(), s.end());
        sort(t.begin(), t.end());
        return s == t;
    }
};

// ============= Variation 2: Hash Map =============
// Algorithm: Build frequency map for first string. Then decrement frequencies
// for characters in second string. Any negative frequency means invalid.
// Time: O(n)  Space: O(n)
class Solution_v2 {
public:
    bool isAnagram(string s, string t) {
        if (s.size() != t.size()) return false;
        unordered_map<char, int> count;
        for (char c : s) count[c]++;
        for (char c : t) {
            count[c]--;
            if (count[c] < 0) return false;
        }
        return true;
    }
};

// ============= Variation 3: Array Count (26 chars) =============
// Algorithm: Use a fixed array of size 26 for char counts. Increment for s,
// decrement for t. Pass if every element in the array is 0.
// Time: O(n)  Space: O(1)
class Solution_v3 {
public:
    bool isAnagram(string s, string t) {
        if (s.size() != t.size()) return false;
        int count[26] = {0};
        for (int i = 0; i < s.size(); i++) {
            count[s[i] - 'a']++;
            count[t[i] - 'a']--;
        }
        for (int c : count)
            if (c != 0) return false;
        return true;
    }
};

int main() {
    string s = "anagram", t = "nagaram";

    {
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v1().isAnagram(s, t);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Sorting): result=" << res << ", time = " << us << " µs" << endl;
    }
    {
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v2().isAnagram(s, t);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (HashMap): result=" << res << ", time = " << us << " µs" << endl;
    }
    {
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v3().isAnagram(s, t);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var3 (Array): result=" << res << ", time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 0.923 µs
// var2 mem = N/A and time = 6.386 µs
// var3 mem = N/A and time = 0.259 µs
