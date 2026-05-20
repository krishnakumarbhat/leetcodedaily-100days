#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 746: Min Cost Climbing Stairs - Easy */
int main(){
    vector<int> cost={10,15,20,5,12,7,3,8}; int n=cost.size();
    auto s=chrono::high_resolution_clock::now();
    for(int i=2;i<n;i++) cost[i]+=min(cost[i-1],cost[i-2]);
    cout<<"var1: "<<min(cost[n-1],cost[n-2])<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
