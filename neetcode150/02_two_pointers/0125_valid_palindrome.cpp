/*
 * LeetCode 125: Valid Palindrome
 * Link: https://leetcode.com/problems/valid-palindrome/
 * Difficulty: Easy
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Filter + Reverse =============
// Algorithm: Filter string using isalnum into a new sequence. Copy the sequence, 
// reverse it sequentially and return bool equality check with itself. 
// Time: O(n)  Space: O(n)
class Solution_v1 {
public:
    bool isPalindrome(string s) {
        string filtered;
        for (char c : s) if (isalnum(c)) filtered += tolower(c);
        string rev = filtered;
        reverse(rev.begin(), rev.end());
        return filtered == rev;
    }
};

// ============= Variation 2: Two Pointers =============
// Algorithm: Loop one pointer forward and one backwards, ignoring symbols dynamically.
// Verify equality of parsed characters under tolower logic immediately.
// Time: O(n)  Space: O(1)
class Solution_v2 {
public:
    bool isPalindrome(string s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            while (l < r && !isalnum(s[l])) l++;
            while (l < r && !isalnum(s[r])) r--;
            if (tolower(s[l]) != tolower(s[r])) return false;
            l++; r--;
        }
        return true;
    }
};

int main() {
    string s = "A man, a plan, a canal: Panama";
    {
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v1().isPalindrome(s);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Filter+Reverse): result=" << res << ", time = " << us << " µs" << endl;
    }
    {
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v2().isPalindrome(s);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Two Pointers): result=" << res << ", time = " << us << " µs" << endl;
    }
    return 0;
}
// var1 mem = N/A and time = 10.277 µs
// var2 mem = N/A and time = 1.146 µs
