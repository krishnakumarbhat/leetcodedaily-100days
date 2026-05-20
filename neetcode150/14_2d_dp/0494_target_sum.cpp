#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> nums={1,1,1,1,1}; int target=3;
    auto t=chrono::high_resolution_clock::now();
    unordered_map<int,int> dp; dp[0]=1;
    for(int n:nums){ unordered_map<int,int> nd; for(auto&[s,c]:dp){nd[s+n]+=c;nd[s-n]+=c;} dp=nd; }
    cout<<"var1: "<<dp[target]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
