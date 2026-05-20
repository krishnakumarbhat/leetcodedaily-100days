#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 332: Reconstruct Itinerary - Hard */
map<string,vector<string>> g12;
vector<string> route12;
void dfs12(const string& a){ while(!g12[a].empty()){ string nb=g12[a].back(); g12[a].pop_back(); dfs12(nb); } route12.push_back(a); }
int main(){
    vector<pair<string,string>> tickets={{"MUC","LHR"},{"JFK","MUC"},{"SFO","SJC"},{"LHR","SFO"}};
    for(auto&[s,d]:tickets) g12[s].push_back(d);
    for(auto&[k,v]:g12) sort(v.rbegin(),v.rend());
    auto s=chrono::high_resolution_clock::now();
    dfs12("JFK"); reverse(route12.begin(),route12.end());
    cout<<"var1: "; for(auto& x:route12) cout<<x<<" "; cout<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
