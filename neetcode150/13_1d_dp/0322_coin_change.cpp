#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 322: Coin Change - Medium */
int main(){
    vector<int> coins={1,5,11}; int amount=15;
    auto t=chrono::high_resolution_clock::now();
    vector<int> dp(amount+1,INT_MAX); dp[0]=0;
    for(int a=1;a<=amount;a++) for(int c:coins) if(c<=a&&dp[a-c]!=INT_MAX) dp[a]=min(dp[a],dp[a-c]+1);
    cout<<"var1: "<<(dp[amount]==INT_MAX?-1:dp[amount])<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
