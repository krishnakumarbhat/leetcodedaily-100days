#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 213: House Robber II - Medium */
int robLinear(vector<int>& n,int l,int r){int a=0,b=0;for(int i=l;i<=r;i++){int c=max(b,a+n[i]);a=b;b=c;}return b;}
int main(){
    vector<int> nums={2,3,2}; int n=nums.size();
    auto s=chrono::high_resolution_clock::now();
    int res=n==1?nums[0]:max(robLinear(nums,0,n-2),robLinear(nums,1,n-1));
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
