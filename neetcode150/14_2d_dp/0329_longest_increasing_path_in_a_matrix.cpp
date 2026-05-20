#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int R,C; vector<vector<int>>* G; vector<vector<int>> memo;
int dfs(int r,int c){ if(memo[r][c]) return memo[r][c]; int best=1; int dr[]={1,-1,0,0},dc[]={0,0,1,-1}; for(int d=0;d<4;d++){int nr=r+dr[d],nc=c+dc[d];if(nr>=0&&nr<R&&nc>=0&&nc<C&&(*G)[nr][nc]>(*G)[r][c]) best=max(best,1+dfs(nr,nc));} return memo[r][c]=best; }
int main(){
    vector<vector<int>> g={{9,9,4},{6,6,8},{2,1,1}}; G=&g; R=g.size();C=g[0].size(); memo.assign(R,vector<int>(C,0));
    auto t=chrono::high_resolution_clock::now();
    int ans=0; for(int r=0;r<R;r++)for(int c=0;c<C;c++) ans=max(ans,dfs(r,c));
    cout<<"var1: "<<ans<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
