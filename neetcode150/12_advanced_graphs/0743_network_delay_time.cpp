#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 743: Network Delay Time - Medium */
int main(){
    int n=4,k=2;
    vector<tuple<int,int,int>> times={{2,1,1},{2,3,1},{3,4,1}};
    vector<vector<pair<int,int>>> g(n+1);
    for(auto[u,v,w]:times) g[u].push_back({v,w});
    auto s=chrono::high_resolution_clock::now();
    vector<int> dist(n+1,INT_MAX); dist[k]=0;
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<>> pq; pq.push({0,k});
    while(!pq.empty()){ auto[d,u]=pq.top();pq.pop(); if(d>dist[u]) continue; for(auto[v,w]:g[u]) if(dist[u]+w<dist[v]){dist[v]=dist[u]+w;pq.push({dist[v],v});} }
    int mx=*max_element(dist.begin()+1,dist.end());
    cout<<"var1: "<<(mx==INT_MAX?-1:mx)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
