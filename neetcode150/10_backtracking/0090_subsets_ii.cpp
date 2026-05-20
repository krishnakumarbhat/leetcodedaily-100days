#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 90: Subsets II - Medium */
void bt(vector<int>& n, int i, vector<int>& cur, vector<vector<int>>& res){
    res.push_back(cur);
    for(int j=i;j<(int)n.size();j++){
        if(j>i&&n[j]==n[j-1]) continue;
        cur.push_back(n[j]); bt(n,j+1,cur,res); cur.pop_back();
    }
}
int main(){
    vector<int> nums={1,2,2}; sort(nums.begin(),nums.end());
    auto s=chrono::high_resolution_clock::now();
    vector<vector<int>> res; vector<int> cur; bt(nums,0,cur,res);
    cout<<"var1: "<<res.size()<<" unique subsets"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
