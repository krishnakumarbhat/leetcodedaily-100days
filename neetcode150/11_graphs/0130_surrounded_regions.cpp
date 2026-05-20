#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 130: Surrounded Regions - Medium */
int RR,CC; vector<vector<char>>* BB;
void dfs2(int r,int c){ if(r<0||r>=RR||c<0||c>=CC||(*BB)[r][c]!='O') return; (*BB)[r][c]='T'; dfs2(r+1,c);dfs2(r-1,c);dfs2(r,c+1);dfs2(r,c-1); }
int main(){
    vector<vector<char>> b={{'X','X','X','X'},{'X','O','O','X'},{'X','X','O','X'},{'X','O','X','X'}};
    BB=&b; RR=b.size(); CC=b[0].size();
    auto s=chrono::high_resolution_clock::now();
    for(int r=0;r<RR;r++){dfs2(r,0);dfs2(r,CC-1);}
    for(int c=0;c<CC;c++){dfs2(0,c);dfs2(RR-1,c);}
    for(int r=0;r<RR;r++) for(int c=0;c<CC;c++){ if(b[r][c]=='O') b[r][c]='X'; else if(b[r][c]=='T') b[r][c]='O'; }
    cout<<"var1 done"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
