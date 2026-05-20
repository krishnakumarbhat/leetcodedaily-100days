/* LeetCode 567: Permutation in String - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Matches Object =============
// Algorithm: Track variables equality mapping numerically. Expand dynamically 
// and update exactly bounds differences for characters sliding linearly.
// Time: O(n)  Space: O(1)
class Solution_v1 {
public:
    bool checkInclusion(string s1, string s2) {
        if (s1.size()>s2.size()) return false;
        int c1[26]={0},c2[26]={0};
        for (int i=0;i<s1.size();i++){c1[s1[i]-'a']++;c2[s2[i]-'a']++;}
        int matches=0;
        for (int i=0;i<26;i++) if(c1[i]==c2[i]) matches++;
        for (int i=s1.size();i<s2.size();i++){
            if(matches==26) return true;
            int idx=s2[i]-'a'; c2[idx]++;
            if(c2[idx]==c1[idx]) matches++; else if(c2[idx]==c1[idx]+1) matches--;
            idx=s2[i-s1.size()]-'a'; c2[idx]--;
            if(c2[idx]==c1[idx]) matches++; else if(c2[idx]==c1[idx]-1) matches--;
        }
        return matches==26;
    }
};
int main(){
    string s1="ab",s2="eidbaooo";
    auto st=chrono::high_resolution_clock::now(); bool r=Solution_v1().checkInclusion(s1,s2); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Matches): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-st).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
