#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 778: Swim in Rising Water - Hard */
int main(){
    vector<vector<int>> grid={{0,2},{1,3}}; int n=grid.size();
    priority_queue<tuple<int,int,int>,vector<tuple<int,int,int>>,greater<>> pq;
    pq.push({grid[0][0],0,0}); vector<vector<bool>> vis(n,vector<bool>(n,false));
    auto s=chrono::high_resolution_clock::now();
    int ans=0;
    while(!pq.empty()){ auto[t,r,c]=pq.top();pq.pop(); if(vis[r][c]) continue; vis[r][c]=true; ans=max(ans,t); if(r==n-1&&c==n-1){cout<<"var1: "<<ans<<endl;break;} int dr[]={1,-1,0,0},dc[]={0,0,1,-1}; for(int d=0;d<4;d++){int nr=r+dr[d],nc=c+dc[d]; if(nr>=0&&nr<n&&nc>=0&&nc<n&&!vis[nr][nc]) pq.push({max(t,grid[nr][nc]),nr,nc});} }
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
