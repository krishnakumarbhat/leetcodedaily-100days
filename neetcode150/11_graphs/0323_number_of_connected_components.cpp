#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 323: Number of Connected Components - Medium */
int par[100],rnk[100];
int find(int x){while(par[x]!=x){par[x]=par[par[x]];x=par[x];}return x;}
int main(){
    int n=5; vector<pair<int,int>> edges={{0,1},{1,2},{3,4}};
    for(int i=0;i<n;i++){par[i]=i;rnk[i]=0;}
    auto s=chrono::high_resolution_clock::now();
    int cnt=n;
    for(auto[a,b]:edges){int pa=find(a),pb=find(b);if(pa==pb)continue;if(rnk[pa]<rnk[pb])swap(pa,pb);par[pb]=pa;if(rnk[pa]==rnk[pb])rnk[pa]++;cnt--;}
    cout<<"var1: components="<<cnt<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
