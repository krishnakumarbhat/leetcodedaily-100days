#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 207: Course Schedule - Medium */
// var1: DFS cycle detection
bool dfs(int c, vector<vector<int>>& g, vector<int>& st){ if(st[c]==1) return false; if(st[c]==2) return true; st[c]=1; for(int nb:g[c]) if(!dfs(nb,g,st)) return false; st[c]=2; return true; }
int main(){
    int n=4; vector<pair<int,int>> pre={{1,0},{2,0},{3,1},{3,2}};
    vector<vector<int>> g(n); for(auto[c,p]:pre) g[c].push_back(p);
    auto s=chrono::high_resolution_clock::now();
    vector<int> st(n,0); bool ok=true; for(int i=0;i<n&&ok;i++) ok=dfs(i,g,st);
    cout<<"var1: can_finish="<<ok<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
