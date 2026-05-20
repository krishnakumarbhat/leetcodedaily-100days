/* LeetCode 22: Generate Parentheses - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Backtracking =============
// Algorithm: Standard recursion maintaining open/close counters. Appends results 
// to a class-level vector once base case `size == 2n` is reached.
// Time: O(4^n/sqrt(n))  Space: O(n)
class Solution_v1 {
public:
    vector<string> res;
    void bt(string s, int o, int c, int n) {
        if (s.size()==2*n) { res.push_back(s); return; }
        if (o<n) bt(s+'(',o+1,c,n);
        if (c<o) bt(s+')',o,c+1,n);
    }
    vector<string> generateParenthesis(int n) { res.clear(); bt("",0,0,n); return res; }
};
int main() {
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().generateParenthesis(3); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Backtrack): count="<<r.size()<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
