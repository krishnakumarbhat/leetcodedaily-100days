#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 261: Graph Valid Tree - Medium */
int par2[100];
int find2(int x){while(par2[x]!=x){par2[x]=par2[par2[x]];x=par2[x];}return x;}
int main(){
    int n=5; vector<pair<int,int>> edges={{0,1},{0,2},{0,3},{1,4}};
    if((int)edges.size()!=n-1){cout<<"var1: false"<<endl;return 0;}
    for(int i=0;i<n;i++) par2[i]=i;
    auto s=chrono::high_resolution_clock::now();
    bool ok=true;
    for(auto[a,b]:edges){int pa=find2(a),pb=find2(b);if(pa==pb){ok=false;break;}par2[pb]=pa;}
    cout<<"var1: valid_tree="<<ok<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
