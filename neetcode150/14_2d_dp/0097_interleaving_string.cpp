#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string s1="aabcc",s2="dbbca",s3="aadbbcbcac";
    int m=s1.size(),n=s2.size();
    auto t=chrono::high_resolution_clock::now();
    if(m+n!=(int)s3.size()){cout<<"var1: false"<<endl;return 0;}
    vector<vector<bool>> dp(m+1,vector<bool>(n+1,false));
    dp[0][0]=true;
    for(int i=1;i<=m;i++) dp[i][0]=dp[i-1][0]&&s1[i-1]==s3[i-1];
    for(int j=1;j<=n;j++) dp[0][j]=dp[0][j-1]&&s2[j-1]==s3[j-1];
    for(int i=1;i<=m;i++) for(int j=1;j<=n;j++) dp[i][j]=(dp[i-1][j]&&s1[i-1]==s3[i+j-1])||(dp[i][j-1]&&s2[j-1]==s3[i+j-1]);
    cout<<"var1: "<<dp[m][n]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
