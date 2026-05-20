#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 51: N-Queens - Hard */
int n_val;
set<int> cols_s, pd_s, nd_s;
vector<int> queens_s;
vector<vector<string>> res_s;
void bt(int r){
    if(r==n_val){ vector<string> board; for(int qc:queens_s){ string row(n_val,'.'); row[qc]='Q'; board.push_back(row); } res_s.push_back(board); return; }
    for(int c=0;c<n_val;c++){
        if(cols_s.count(c)||pd_s.count(r+c)||nd_s.count(r-c)) continue;
        cols_s.insert(c); pd_s.insert(r+c); nd_s.insert(r-c); queens_s.push_back(c);
        bt(r+1);
        cols_s.erase(c); pd_s.erase(r+c); nd_s.erase(r-c); queens_s.pop_back();
    }
}
int main(){
    n_val=4;
    auto s=chrono::high_resolution_clock::now();
    bt(0); cout<<"var1: "<<res_s.size()<<" solutions"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
