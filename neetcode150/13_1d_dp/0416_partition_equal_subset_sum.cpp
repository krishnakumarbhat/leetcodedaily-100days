#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 416: Partition Equal Subset Sum - Medium */
int main(){
    vector<int> nums={1,5,11,5}; int total=accumulate(nums.begin(),nums.end(),0);
    if(total%2){cout<<"var1: false"<<endl;return 0;}
    int target=total/2;
    auto t=chrono::high_resolution_clock::now();
    vector<bool> dp(target+1,false); dp[0]=true;
    for(int x:nums) for(int j=target;j>=x;j--) dp[j]=dp[j]||dp[j-x];
    cout<<"var1: "<<dp[target]<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
