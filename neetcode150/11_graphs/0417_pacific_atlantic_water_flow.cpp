#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 417: Pacific Atlantic Water Flow - Medium */
int R,C; vector<vector<int>>* H;
void dfs(int r,int c,set<pair<int,int>>& vis,int ph){
    if(r<0||r>=R||c<0||c>=C||vis.count({r,c})||(*H)[r][c]<ph) return;
    vis.insert({r,c}); for(auto [dr,dc]:vector<pair<int,int>>{{1,0},{-1,0},{0,1},{0,-1}}) dfs(r+dr,c+dc,vis,(*H)[r][c]);
}
int main(){
    vector<vector<int>> h={{1,2,2,3,5},{3,2,3,4,4},{2,4,5,3,1},{6,7,1,4,5},{5,1,1,2,4}};
    H=&h; R=h.size(); C=h[0].size();
    set<pair<int,int>> pac,atl;
    auto s=chrono::high_resolution_clock::now();
    for(int c=0;c<C;c++){dfs(0,c,pac,h[0][c]);dfs(R-1,c,atl,h[R-1][c]);}
    for(int r=0;r<R;r++){dfs(r,0,pac,h[r][0]);dfs(r,C-1,atl,h[r][C-1]);}
    int cnt=0; for(auto& p:pac) if(atl.count(p)) cnt++;
    cout<<"var1: "<<cnt<<" cells"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
