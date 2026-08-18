/* LeetCode 424: Longest Repeating Character Replacement - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Sliding Window =============
// Algorithm: Store 26 map array occurrences. Track maximum frequency. Restrain 
// sliding bounds leftward continuously updating string replacements limit naturally.
// Time: O(n)  Space: O(26)
class Solution_v1 {
public:
    int characterReplacement(string s, int k) {
        int count[26]={0}, l=0, maxF=0, res=0;
        for (int r=0; r<s.size(); r++) {
            count[s[r]-'A']++; maxF=max(maxF,count[s[r]-'A']);
            while ((r-l+1)-maxF>k) { count[s[l]-'A']--; l++; }
            res=max(res,r-l+1);
        }
        return res;
    }
};
int main() {
    string s="AABABBA"; int k=2;
    auto st=chrono::high_resolution_clock::now(); int r=Solution_v1().characterReplacement(s,k); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (SW): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-st).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
