#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<pair<int,int>> iv={{1,2},{2,3},{3,4},{1,3}};
    auto t=chrono::high_resolution_clock::now();
    sort(iv.begin(),iv.end(),[](auto&a,auto&b){return a.second<b.second;});
    int cnt=0,end=INT_MIN;
    for(auto&[s,e]:iv){if(s>=end)end=e;else cnt++;}
    cout<<"var1: "<<cnt<<endl;
    auto e2=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e2-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
