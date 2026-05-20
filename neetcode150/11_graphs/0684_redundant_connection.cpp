#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 684: Redundant Connection - Medium */
int par3[1001],rnk3[1001];
int find3(int x){while(par3[x]!=x){par3[x]=par3[par3[x]];x=par3[x];}return x;}
int main(){
    vector<pair<int,int>> edges={{1,2},{1,3},{2,3}};
    for(int i=0;i<=1000;i++){par3[i]=i;rnk3[i]=0;}
    auto s=chrono::high_resolution_clock::now();
    pair<int,int> ans={-1,-1};
    for(auto[a,b]:edges){int pa=find3(a),pb=find3(b);if(pa==pb){ans={a,b};break;}if(rnk3[pa]<rnk3[pb])swap(pa,pb);par3[pb]=pa;if(rnk3[pa]==rnk3[pb])rnk3[pa]++;}
    cout<<"var1: redundant=["<<ans.first<<","<<ans.second<<"]"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
