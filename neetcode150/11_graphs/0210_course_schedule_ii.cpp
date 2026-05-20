#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 210: Course Schedule II - Medium */
int main(){
    int n=4; vector<pair<int,int>> pre={{1,0},{2,0},{3,1},{3,2}};
    vector<vector<int>> g(n); vector<int> indeg(n,0);
    for(auto[c,p]:pre){g[p].push_back(c);indeg[c]++;}
    auto s=chrono::high_resolution_clock::now();
    queue<int> q; for(int i=0;i<n;i++) if(indeg[i]==0) q.push(i);
    vector<int> order;
    while(!q.empty()){int c=q.front();q.pop();order.push_back(c);for(int nb:g[c]){indeg[nb]--;if(indeg[nb]==0)q.push(nb);}}
    cout<<"var1: order_size="<<order.size()<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
