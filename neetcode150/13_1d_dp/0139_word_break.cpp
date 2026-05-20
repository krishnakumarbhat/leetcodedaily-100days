#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 139: Word Break - Medium */
int main(){
    string s="leetcode"; unordered_set<string> words={"leet","code"};
    int n=s.size();
    auto t=chrono::high_resolution_clock::now();
    vector<bool> dp(n+1,false); dp[0]=true;
    for(int i=1;i<=n;i++) for(int j=0;j<i;j++) if(dp[j]&&words.count(s.substr(j,i-j))){dp[i]=true;break;}
    cout<<"var1: "<<dp[n]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
