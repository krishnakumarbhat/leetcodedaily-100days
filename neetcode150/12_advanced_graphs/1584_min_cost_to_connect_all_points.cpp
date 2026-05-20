#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 1584: Min Cost to Connect All Points - Medium */
int main(){
    vector<pair<int,int>> pts={{0,0},{2,2},{3,10},{5,2},{7,0}};
    int n=pts.size();
    // Prim
    auto s=chrono::high_resolution_clock::now();
    vector<bool> vis(n,false); priority_queue<pair<int,int>,vector<pair<int,int>>,greater<>> pq; pq.push({0,0});
    long long total=0; int cnt=0;
    while(cnt<n){
        auto[cost,u]=pq.top(); pq.pop();
        if(vis[u]) continue; vis[u]=true; total+=cost; cnt++;
        for(int v=0;v<n;v++) if(!vis[v]){ int d=abs(pts[u].first-pts[v].first)+abs(pts[u].second-pts[v].second); pq.push({d,v}); }
    }
    cout<<"var1 (Prim): "<<total<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
