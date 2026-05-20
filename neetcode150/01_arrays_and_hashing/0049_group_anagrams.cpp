/*
 * LeetCode 49: Group Anagrams
 * Link: https://leetcode.com/problems/group-anagrams/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Sorted Key =============
// Algorithm: Sort each string to generate a canonical form. Map this canonical
// string to a list of original strings. Returns all values from the hash map.
// Time: O(n * k log k)  Space: O(n * k)
class Solution_v1 {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> groups;
        for (auto& s : strs) {
            string key = s;
            sort(key.begin(), key.end());
            groups[key].push_back(s);
        }
        vector<vector<string>> result;
        for (auto& p : groups)
            result.push_back(p.second);
        return result;
    }
};

// ============= Variation 2: Character Count Key =============
// Algorithm: Map string counting properties into a 26-char string where each 
// char represents the frequency of 'a' through 'z'. Use this string as the hash map key.
// Time: O(n * k)  Space: O(n * k)
class Solution_v2 {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> groups;
        for (auto& s : strs) {
            string key(26, '0');
            for (char c : s) key[c - 'a']++;
            groups[key].push_back(s);
        }
        vector<vector<string>> result;
        for (auto& p : groups)
            result.push_back(p.second);
        return result;
    }
};

int main() {
    vector<string> strs = {"eat", "tea", "tan", "ate", "nat", "bat", "tab", "ant", "ten"};

    {
        vector<string> data = strs;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v1().groupAnagrams(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Sorted Key): groups=" << res.size() << ", time = " << us << " µs" << endl;
    }
    {
        vector<string> data = strs;
        auto start = chrono::high_resolution_clock::now();
        auto res = Solution_v2().groupAnagrams(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Char Count): groups=" << res.size() << ", time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 10.099 µs
// var2 mem = N/A and time = 11.411 µs
