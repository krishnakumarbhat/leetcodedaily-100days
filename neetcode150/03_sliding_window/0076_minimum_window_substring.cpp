/* LeetCode 76: Minimum Window Substring - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Sliding Window =============
// Algorithm: Using a single pass array tracking requirements. Move right window 
// boundary to form target. Shrink using left updating length to INT_MAX.
// Time: O(n+m)  Space: O(n+m)
class Solution_v1 {
public:
    string minWindow(string s, string t) {
        unordered_map<char,int> tc,wc;
        for(char c:t) tc[c]++;
        int req=tc.size(),formed=0,l=0,ans_len=INT_MAX,ans_l=0;
        for(int r=0;r<s.size();r++){
            wc[s[r]]++;
            if(tc.count(s[r])&&wc[s[r]]==tc[s[r]]) formed++;
            while(formed==req){
                if(r-l+1<ans_len){ans_len=r-l+1;ans_l=l;}
                wc[s[l]]--;
                if(tc.count(s[l])&&wc[s[l]]<tc[s[l]]) formed--;
                l++;
            }
        }
        return ans_len==INT_MAX?"":s.substr(ans_l,ans_len);
    }
};
int main(){
    string s="ADOBECODEBANC",t="ABC";
    auto st=chrono::high_resolution_clock::now(); auto r=Solution_v1().minWindow(s,t); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (SW): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-st).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
