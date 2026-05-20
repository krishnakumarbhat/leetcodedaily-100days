#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<pair<int,int>> iv={{1,3},{2,6},{8,10},{15,18}};
    auto t=chrono::high_resolution_clock::now();
    sort(iv.begin(),iv.end());
    vector<pair<int,int>> res={iv[0]};
    for(auto&[s,e]:iv){if(s<=res.back().second)res.back().second=max(res.back().second,e);else res.push_back({s,e});}
    for(auto&p:res)cout<<"["<<p.first<<","<<p.second<<"] ";cout<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
