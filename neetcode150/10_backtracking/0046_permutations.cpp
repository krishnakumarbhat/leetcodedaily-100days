#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 46: Permutations - Medium */
// var1: swap in-place
void bt(vector<int>& n, int s, vector<vector<int>>& res){
    if(s==(int)n.size()){ res.push_back(n); return; }
    for(int i=s;i<(int)n.size();i++){ swap(n[s],n[i]); bt(n,s+1,res); swap(n[s],n[i]); }
}
// var2: next_permutation
vector<vector<int>> v2(vector<int> n){
    sort(n.begin(),n.end()); vector<vector<int>> res;
    do { res.push_back(n); } while(next_permutation(n.begin(),n.end()));
    return res;
}
int main(){
    vector<int> nums={1,2,3};
    auto t1=chrono::high_resolution_clock::now(); vector<vector<int>> r1; bt(nums,0,r1); cout<<"var1: "<<r1.size()<<" perms"<<endl;
    auto t2=chrono::high_resolution_clock::now(); cout<<"v1 time="<<chrono::duration_cast<chrono::nanoseconds>(t2-t1).count()/1000.0<<"us"<<endl;
    auto t3=chrono::high_resolution_clock::now(); auto r2=v2(nums); cout<<"var2: "<<r2.size()<<" perms"<<endl;
    auto t4=chrono::high_resolution_clock::now(); cout<<"v2 time="<<chrono::duration_cast<chrono::nanoseconds>(t4-t3).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
