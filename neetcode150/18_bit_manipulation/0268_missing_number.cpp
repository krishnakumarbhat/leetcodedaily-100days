#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> nums = {3,0,1};
    auto t=chrono::high_resolution_clock::now();
    int res = nums.size();
    for(int i=0; i<nums.size(); i++) res ^= (i ^ nums[i]);
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
