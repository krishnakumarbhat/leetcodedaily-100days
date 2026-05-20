#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 286: Walls and Gates - Medium */
const int WINF=2147483647;
int main(){
    vector<vector<int>> g={{WINF,-1,0,WINF},{WINF,WINF,WINF,-1},{WINF,-1,WINF,-1},{0,-1,WINF,WINF}};
    int rows=g.size(),cols=g[0].size();
    deque<pair<int,int>> q;
    for(int r=0;r<rows;r++) for(int c=0;c<cols;c++) if(g[r][c]==0) q.push_back({r,c});
    auto s=chrono::high_resolution_clock::now();
    int dr[]={1,-1,0,0},dc[]={0,0,1,-1};
    while(!q.empty()){auto[r,c]=q.front();q.pop_front();for(int d=0;d<4;d++){int nr=r+dr[d],nc=c+dc[d];if(nr>=0&&nr<rows&&nc>=0&&nc<cols&&g[nr][nc]==WINF){g[nr][nc]=g[r][c]+1;q.push_back({nr,nc});}}}
    cout<<"var1 done"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
