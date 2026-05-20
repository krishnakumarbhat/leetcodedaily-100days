#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 5: Longest Palindromic Substring - Medium */
string expand(const string& s, int l, int r){ while(l>=0&&r<(int)s.size()&&s[l]==s[r]){l--;r++;} return s.substr(l+1,r-l-1); }
int main(){
    string s="babad";
    auto t=chrono::high_resolution_clock::now();
    string res="";
    for(int i=0;i<(int)s.size();i++){
        string a=expand(s,i,i),b=expand(s,i,i+1);
        if(a.size()>res.size()) res=a;
        if(b.size()>res.size()) res=b;
    }
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl; // Note: reusing s for time here
}
// var1 mem = {} and time = {}
