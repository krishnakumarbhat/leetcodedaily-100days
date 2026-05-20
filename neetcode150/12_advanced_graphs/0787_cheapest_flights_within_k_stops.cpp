#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 787: Cheapest Flights Within K Stops - Medium */
int main(){
    int n=3,src=0,dst=2,k=1;
    vector<tuple<int,int,int>> flights={{0,1,100},{1,2,100},{0,2,500}};
    auto s=chrono::high_resolution_clock::now();
    vector<int> prices(n,INT_MAX); prices[src]=0;
    for(int i=0;i<=k;i++){ vector<int> tmp=prices; for(auto[u,v,w]:flights) if(prices[u]!=INT_MAX&&prices[u]+w<tmp[v]) tmp[v]=prices[u]+w; prices=tmp; }
    cout<<"var1: "<<(prices[dst]==INT_MAX?-1:prices[dst])<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
