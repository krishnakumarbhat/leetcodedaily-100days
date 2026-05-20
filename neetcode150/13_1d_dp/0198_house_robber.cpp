#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 198: House Robber - Medium */
int main(){
    vector<int> nums={2,7,9,3,1};
    auto s=chrono::high_resolution_clock::now();
    int a=0,b=0;
    for(int x:nums){int c=max(b,a+x);a=b;b=c;}
    cout<<"var1: "<<b<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
