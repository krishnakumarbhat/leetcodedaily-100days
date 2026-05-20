#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 695: Max Area of Island - Medium */
int dfs(vector<vector<int>>& g, int r, int c){ if(r<0||r>=(int)g.size()||c<0||c>=(int)g[0].size()||g[r][c]!=1) return 0; g[r][c]=0; return 1+dfs(g,r+1,c)+dfs(g,r-1,c)+dfs(g,r,c+1)+dfs(g,r,c-1); }
int main(){
    vector<vector<int>> g={{0,0,1,0,0,0,0,1,0,0,0,0,0},{0,0,0,0,0,0,0,1,1,1,0,0,0},{0,1,1,0,1,0,0,0,0,0,0,0,0}};
    auto s=chrono::high_resolution_clock::now();
    int mx=0; for(int r=0;r<(int)g.size();r++) for(int c=0;c<(int)g[0].size();c++) mx=max(mx,dfs(g,r,c));
    cout<<"var1: max_area="<<mx<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
