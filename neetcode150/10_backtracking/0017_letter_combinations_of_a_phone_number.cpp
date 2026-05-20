#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 17: Letter Combinations of a Phone Number - Medium */
unordered_map<char,string> phone={{'2',"abc"},{'3',"def"},{'4',"ghi"},{'5',"jkl"},{'6',"mno"},{'7',"pqrs"},{'8',"tuv"},{'9',"wxyz"}};
// var1: DFS backtracking
void bt(const string& d, int i, string& cur, vector<string>& res){
    if(i==(int)d.size()){ res.push_back(cur); return; }
    for(char c:phone[d[i]]){ cur+=c; bt(d,i+1,cur,res); cur.pop_back(); }
}
// var2: BFS iterative
vector<string> bfs(const string& d){
    if(d.empty()) return {};
    vector<string> res={""};
    for(char digit:d){ vector<string> tmp; for(auto& s:res) for(char c:phone[digit]) tmp.push_back(s+c); res=tmp; }
    return res;
}
int main(){
    string d="23";
    auto t1=chrono::high_resolution_clock::now(); vector<string> r1; string cur; bt(d,0,cur,r1); cout<<"var1: "<<r1.size()<<" combos"<<endl;
    auto t2=chrono::high_resolution_clock::now(); cout<<"v1 time="<<chrono::duration_cast<chrono::nanoseconds>(t2-t1).count()/1000.0<<"us"<<endl;
    auto t3=chrono::high_resolution_clock::now(); auto r2=bfs(d); cout<<"var2: "<<r2.size()<<" combos"<<endl;
    auto t4=chrono::high_resolution_clock::now(); cout<<"v2 time="<<chrono::duration_cast<chrono::nanoseconds>(t4-t3).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
