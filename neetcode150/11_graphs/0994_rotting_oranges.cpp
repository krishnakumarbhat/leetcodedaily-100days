#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 994: Rotting Oranges - Medium */
int main(){
    vector<vector<int>> g={{2,1,1},{1,1,0},{0,1,1}};
    int rows=g.size(),cols=g[0].size(),fresh=0;
    deque<tuple<int,int,int>> q;
    for(int r=0;r<rows;r++) for(int c=0;c<cols;c++){ if(g[r][c]==2) q.push_back({r,c,0}); else if(g[r][c]==1) fresh++; }
    auto s=chrono::high_resolution_clock::now();
    int tmax=0;
    while(!q.empty()){ auto[r,c,t]=q.front(); q.pop_front(); tmax=max(tmax,t); int dr[]={1,-1,0,0},dc[]={0,0,1,-1}; for(int d=0;d<4;d++){ int nr=r+dr[d],nc=c+dc[d]; if(nr>=0&&nr<rows&&nc>=0&&nc<cols&&g[nr][nc]==1){g[nr][nc]=2;fresh--;q.push_back({nr,nc,t+1});} } }
    cout<<"var1: "<<(fresh==0?tmax:-1)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
