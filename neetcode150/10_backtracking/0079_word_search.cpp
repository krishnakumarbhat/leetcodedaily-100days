#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 79: Word Search - Medium */
bool dfs(vector<vector<char>>& b, string& w, int r, int c, int i){
    if(i==(int)w.size()) return true;
    if(r<0||r>=(int)b.size()||c<0||c>=(int)b[0].size()||b[r][c]!=w[i]) return false;
    char tmp=b[r][c]; b[r][c]='#';
    bool found=dfs(b,w,r+1,c,i+1)||dfs(b,w,r-1,c,i+1)||dfs(b,w,r,c+1,i+1)||dfs(b,w,r,c-1,i+1);
    b[r][c]=tmp; return found;
}
int main(){
    vector<vector<char>> b={{'A','B','C','E'},{'S','F','C','S'},{'A','D','E','E'}};
    string w="ABCCED";
    auto s=chrono::high_resolution_clock::now();
    bool res=false;
    for(int r=0;r<(int)b.size()&&!res;r++) for(int c=0;c<(int)b[0].size()&&!res;c++) res=dfs(b,w,r,c,0);
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
