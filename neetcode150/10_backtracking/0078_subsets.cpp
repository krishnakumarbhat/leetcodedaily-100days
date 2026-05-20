#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 78: Subsets - Medium */
// var1: iterative
vector<vector<int>> v1(vector<int>& n){
    vector<vector<int>> res={{}};
    for(int x:n){ int sz=res.size(); for(int i=0;i<sz;i++){ res.push_back(res[i]); res.back().push_back(x); } }
    return res;
}
// var2: backtracking
void bt(vector<int>& n, int i, vector<int>& cur, vector<vector<int>>& res){
    res.push_back(cur);
    for(int j=i;j<(int)n.size();j++){ cur.push_back(n[j]); bt(n,j+1,cur,res); cur.pop_back(); }
}
vector<vector<int>> v2(vector<int>& n){ vector<vector<int>> res; vector<int> cur; bt(n,0,cur,res); return res; }
// var3: bitmask
vector<vector<int>> v3(vector<int>& n){
    int sz=n.size(); vector<vector<int>> res;
    for(int m=0;m<(1<<sz);m++){ vector<int> s; for(int i=0;i<sz;i++) if(m&(1<<i)) s.push_back(n[i]); res.push_back(s); }
    return res;
}
int main(){
    vector<int> nums={1,2,3};
    auto t1=chrono::high_resolution_clock::now(); cout<<"var1: "<<v1(nums).size()<<" subsets"<<endl;
    auto t2=chrono::high_resolution_clock::now(); cout<<"v1 time="<<chrono::duration_cast<chrono::nanoseconds>(t2-t1).count()/1000.0<<"us"<<endl;
    auto t3=chrono::high_resolution_clock::now(); cout<<"var2: "<<v2(nums).size()<<" subsets"<<endl;
    auto t4=chrono::high_resolution_clock::now(); cout<<"v2 time="<<chrono::duration_cast<chrono::nanoseconds>(t4-t3).count()/1000.0<<"us"<<endl;
    auto t5=chrono::high_resolution_clock::now(); cout<<"var3: "<<v3(nums).size()<<" subsets"<<endl;
    auto t6=chrono::high_resolution_clock::now(); cout<<"v3 time="<<chrono::duration_cast<chrono::nanoseconds>(t6-t5).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
// var3 mem = {} and time = {}
