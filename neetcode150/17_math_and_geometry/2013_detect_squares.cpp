#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    auto t=chrono::high_resolution_clock::now();
    unordered_map<int, unordered_map<int, int>> ptsCount; vector<pair<int, int>> pts;
    auto add = [&](int x, int y){ ptsCount[x][y]++; pts.push_back({x, y}); };
    auto count = [&](int px, int py){ int res = 0; for(auto& p : pts){ int x = p.first, y = p.second; if(abs(py - y) != abs(px - x) || x == px || y == py) continue; res += ptsCount[x][py] * ptsCount[px][y]; } return res; };
    add(3,10); add(11,2); add(3,2); int res = count(11,10);
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
