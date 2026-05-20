#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string s1="abcde",s2="ace"; int m=s1.size(),n=s2.size();
    auto t=chrono::high_resolution_clock::now();
    vector<vector<int>> dp(m+1,vector<int>(n+1,0));
    for(int i=1;i<=m;i++) for(int j=1;j<=n;j++) dp[i][j]=s1[i-1]==s2[j-1]?1+dp[i-1][j-1]:max(dp[i-1][j],dp[i][j-1]);
    cout<<"var1: "<<dp[m][n]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
