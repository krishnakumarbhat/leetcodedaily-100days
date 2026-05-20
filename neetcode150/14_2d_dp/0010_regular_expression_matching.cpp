#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string s="aab",p="c*a*b"; int m=s.size(),n=p.size();
    auto t=chrono::high_resolution_clock::now();
    vector<vector<bool>> dp(m+1,vector<bool>(n+1,false));
    dp[0][0]=true;
    for(int j=1;j<=n;j++) if(p[j-1]=='*') dp[0][j]=dp[0][j-2];
    for(int i=1;i<=m;i++) for(int j=1;j<=n;j++){
        if(p[j-1]=='*'){ dp[i][j]=dp[i][j-2]; if(p[j-2]=='.'||p[j-2]==s[i-1]) dp[i][j]=dp[i][j]||dp[i-1][j];
        }else if(p[j-1]=='.'||p[j-1]==s[i-1]) dp[i][j]=dp[i-1][j-1];
    }
    cout<<"var1: "<<dp[m][n]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
