#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 131: Palindrome Partitioning - Medium */
bool isPalin(const string& s, int l, int r){ while(l<r){ if(s[l]!=s[r]) return false; l++;r--; } return true; }
void bt(const string& s, int i, vector<string>& cur, vector<vector<string>>& res){
    if(i==(int)s.size()){ res.push_back(cur); return; }
    for(int j=i;j<(int)s.size();j++){
        if(isPalin(s,i,j)){ cur.push_back(s.substr(i,j-i+1)); bt(s,j+1,cur,res); cur.pop_back(); }
    }
}
int main(){
    string s="aab";
    auto t=chrono::high_resolution_clock::now();
    vector<vector<string>> res; vector<string> cur; bt(s,0,cur,res);
    cout<<"var1: "<<res.size()<<" partitions"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
