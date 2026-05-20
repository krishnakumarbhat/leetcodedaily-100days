#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<pair<int,int>> iv={{1,4},{2,4},{3,6},{4,4}}; vector<int> q={2,3,4,5};
    auto t=chrono::high_resolution_clock::now();
    int n=q.size(); vector<int> res(n,-1);
    sort(iv.begin(),iv.end()); vector<int> idx(n); iota(idx.begin(),idx.end(),0); sort(idx.begin(),idx.end(),[&](int a,int b){return q[a]<q[b];});
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<>> h; int i=0;
    for(int qi:idx){int qv=q[qi];while(i<(int)iv.size()&&iv[i].first<=qv){h.push({iv[i].second-iv[i].first+1,iv[i].second});i++;}while(!h.empty()&&h.top().second<qv)h.pop();if(!h.empty())res[qi]=h.top().first;}
    for(int x:res)cout<<x<<" ";cout<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
