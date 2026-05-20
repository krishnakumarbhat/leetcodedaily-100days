#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<pair<int,int>> iv={{1,3},{6,9}},res; pair<int,int> nw={2,5};
    auto t=chrono::high_resolution_clock::now();
    int i=0,n=iv.size();
    while(i<n&&iv[i].second<nw.first) res.push_back(iv[i++]);
    while(i<n&&iv[i].first<=nw.second){nw.first=min(nw.first,iv[i].first);nw.second=max(nw.second,iv[i].second);i++;}
    res.push_back(nw);
    while(i<n) res.push_back(iv[i++]);
    for(auto&p:res) cout<<"["<<p.first<<","<<p.second<<"] "; cout<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
