#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 39: Combination Sum - Medium */
void bt(vector<int>& c, int i, int rem, vector<int>& cur, vector<vector<int>>& res){
    if(rem==0){ res.push_back(cur); return; }
    for(int j=i;j<(int)c.size();j++){
        if(c[j]>rem) break;
        cur.push_back(c[j]); bt(c,j,rem-c[j],cur,res); cur.pop_back();
    }
}
int main(){
    vector<int> cand={2,3,6,7}; sort(cand.begin(),cand.end());
    auto s=chrono::high_resolution_clock::now();
    vector<vector<int>> res; vector<int> cur; bt(cand,0,7,cur,res);
    cout<<"var1: "<<res.size()<<" combinations"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
