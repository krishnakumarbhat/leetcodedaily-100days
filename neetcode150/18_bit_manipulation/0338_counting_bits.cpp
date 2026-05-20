#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    int n = 5;
    auto t=chrono::high_resolution_clock::now();
    vector<int> dp(n + 1, 0);
    for(int i=1; i<=n; i++) dp[i] = dp[i & (i - 1)] + 1;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
