#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 91: Decode Ways - Medium */
int main(){
    string s="226"; int n=s.size();
    auto t=chrono::high_resolution_clock::now();
    vector<int> dp(n+1,0); dp[0]=1; dp[1]=(s[0]!="0"[0])?1:0;
    for(int i=2;i<=n;i++){
        if(s[i-1]!="0") dp[i]+=dp[i-1];
        int two=stoi(s.substr(i-2,2));
        if(two>=10&&two<=26) dp[i]+=dp[i-2];
    }
    cout<<"var1: "<<dp[n]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
