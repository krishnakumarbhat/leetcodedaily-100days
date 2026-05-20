#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> coins={1,2,5}; int amount=5;
    auto t=chrono::high_resolution_clock::now();
    vector<long long> dp(amount+1,0); dp[0]=1;
    for(int c:coins) for(int a=c;a<=amount;a++) dp[a]+=dp[a-c];
    cout<<"var1: "<<dp[amount]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
