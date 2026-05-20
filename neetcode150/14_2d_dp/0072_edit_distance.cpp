#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string w1="horse",w2="ros"; int m=w1.size(),n=w2.size();
    auto t=chrono::high_resolution_clock::now();
    vector<int> dp(n+1); iota(dp.begin(),dp.end(),0);
    for(int i=1;i<=m;i++){int prev=dp[0];dp[0]=i;for(int j=1;j<=n;j++){int tmp=dp[j];dp[j]=w1[i-1]==w2[j-1]?prev:1+min({dp[j],dp[j-1],prev});prev=tmp;}}
    cout<<"var1: "<<dp[n]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
