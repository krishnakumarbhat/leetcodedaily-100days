#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> n={1,3,1,5,8,1}; int sz=n.size();
    auto t=chrono::high_resolution_clock::now();
    vector<vector<int>> dp(sz,vector<int>(sz,0));
    for(int len=2;len<sz;len++) for(int l=0;l<sz-len;l++){int r=l+len; for(int k=l+1;k<r;k++) dp[l][r]=max(dp[l][r],n[l]*n[k]*n[r]+dp[l][k]+dp[k][r]);}
    cout<<"var1: "<<dp[0][sz-1]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
