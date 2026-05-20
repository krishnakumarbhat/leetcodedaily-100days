/*
 * LeetCode 3: Longest Substring Without Repeating Characters
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Sliding Window Set =============
// Algorithm: Standard window that shrinks from left whenever a dupe hits.
// Time: O(n)  Space: O(min(n,m))
class Solution_v1 {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> cs; int l = 0, res = 0;
        for (int r = 0; r < s.size(); r++) {
            while (cs.count(s[r])) { cs.erase(s[l]); l++; }
            cs.insert(s[r]); res = max(res, r - l + 1);
        }
        return res;
    }
};

// ============= Variation 2: Sliding Window Map =============
// Algorithm: Directly jumps left pointer to seen char map stored indexes natively.
// Time: O(n)  Space: O(min(n,m))
class Solution_v2 {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_map<char, int> mp; int l = 0, res = 0;
        for (int r = 0; r < s.size(); r++) {
            if (mp.count(s[r]) && mp[s[r]] >= l) l = mp[s[r]] + 1;
            mp[s[r]] = r; res = max(res, r - l + 1);
        }
        return res;
    }
};

int main() {
    string s = "abcabcbbdefgh";
    { auto st=chrono::high_resolution_clock::now(); int r=Solution_v1().lengthOfLongestSubstring(s); auto e=chrono::high_resolution_clock::now(); cout<<"var1 (SW Set): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-st).count()/1000.0<<" us"<<endl; }
    { auto st=chrono::high_resolution_clock::now(); int r=Solution_v2().lengthOfLongestSubstring(s); auto e=chrono::high_resolution_clock::now(); cout<<"var2 (SW Map): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-st).count()/1000.0<<" us"<<endl; }
    return 0;
}
// var1 mem = N/A and time = N/A
// var2 mem = N/A and time = N/A
