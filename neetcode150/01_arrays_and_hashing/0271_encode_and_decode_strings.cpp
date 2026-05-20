/*
 * LeetCode 271: Encode and Decode Strings (Premium)
 * Link: https://leetcode.com/problems/encode-and-decode-strings/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Length Prefix Encoding =============
// Algorithm: Add <length> + "#" in front of each string. During decoding, search 
// for '#' to parse the length, then substring exactly that many characters.
// Time: O(n)  Space: O(n)
class Solution_v1 {
public:
    string encode(vector<string>& strs) {
        string result;
        for (auto& s : strs)
            result += to_string(s.size()) + "#" + s;
        return result;
    }

    vector<string> decode(string s) {
        vector<string> result;
        int i = 0;
        while (i < s.size()) {
            int j = i;
            while (s[j] != '#') j++;
            int len = stoi(s.substr(i, j - i));
            result.push_back(s.substr(j + 1, len));
            i = j + 1 + len;
        }
        return result;
    }
};

// ============= Variation 2: Chunked Transfer Encoding =============
// Algorithm: Cast integer string length into a 4-byte char pointer and append it
// before the string to store length in strict raw binary format. 
// Time: O(n)  Space: O(n)
class Solution_v2 {
public:
    string encode(vector<string>& strs) {
        string result;
        for (auto& s : strs) {
            int len = s.size();
            result += string(reinterpret_cast<char*>(&len), 4) + s;
        }
        return result;
    }

    vector<string> decode(string s) {
        vector<string> result;
        int i = 0;
        while (i < s.size()) {
            int len;
            memcpy(&len, s.data() + i, 4);
            result.push_back(s.substr(i + 4, len));
            i += 4 + len;
        }
        return result;
    }
};

int main() {
    vector<string> strs = {"hello", "world", "foo#bar", "test", ""};

    {
        auto data = strs;
        auto start = chrono::high_resolution_clock::now();
        Solution_v1 sol;
        string encoded = sol.encode(data);
        auto decoded = sol.decode(encoded);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Length Prefix): decoded_size=" << decoded.size() << ", time = " << us << " µs" << endl;
    }
    {
        auto data = strs;
        auto start = chrono::high_resolution_clock::now();
        Solution_v2 sol;
        string encoded = sol.encode(data);
        auto decoded = sol.decode(encoded);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Chunked): decoded_size=" << decoded.size() << ", time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 14.429 µs
// var2 mem = N/A and time = 1.781 µs
