#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string s="rabbbit",t="rabbit"; int m=s.size(),n=t.size();
    auto tv=chrono::high_resolution_clock::now();
    vector<vector<long long>> dp(m+1,vector<long long>(n+1,0));
    for(int i=0;i<=m;i++) dp[i][0]=1;
    for(int i=1;i<=m;i++) for(int j=1;j<=n;j++){dp[i][j]=dp[i-1][j];if(s[i-1]==t[j-1])dp[i][j]+=dp[i-1][j-1];}
    cout<<"var1: "<<dp[m][n]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-tv).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
