#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    int m=3,n=7;
    auto t=chrono::high_resolution_clock::now();
    vector<int> dp(n,1);
    for(int r=1;r<m;r++) for(int c=1;c<n;c++) dp[c]+=dp[c-1];
    cout<<"var1: "<<dp[n-1]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
