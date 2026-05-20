#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 647: Palindromic Substrings - Medium */
int main(){
    string s="aaa"; int count=0;
    auto t=chrono::high_resolution_clock::now();
    for(int i=0;i<(int)s.size();i++){
        for(int l=i,r=i;l>=0&&r<(int)s.size()&&s[l]==s[r];l--,r++) count++;
        for(int l=i,r=i+1;l>=0&&r<(int)s.size()&&s[l]==s[r];l--,r++) count++;
    }
    cout<<"var1: "<<count<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
