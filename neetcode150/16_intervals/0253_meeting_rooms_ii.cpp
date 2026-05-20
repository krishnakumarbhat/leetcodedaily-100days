#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<pair<int,int>> iv={{0,30},{5,10},{15,20}};
    auto t=chrono::high_resolution_clock::now();
    sort(iv.begin(),iv.end()); priority_queue<int,vector<int>,greater<int>> h;
    for(auto&[s,e]:iv){if(!h.empty()&&h.top()<=s)h.pop();h.push(e);}
    cout<<"var1: "<<h.size()<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
