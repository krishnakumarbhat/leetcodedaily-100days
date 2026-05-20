#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string s="ababcbacadefegdehijhklij";
    auto t=chrono::high_resolution_clock::now();
    int last[26]={}; for(int i=0;i<(int)s.size();i++) last[s[i]-'a']=i;
    int start=0,end=0; vector<int> res;
    for(int i=0;i<(int)s.size();i++){end=max(end,last[s[i]-'a']);if(i==end){res.push_back(end-start+1);start=i+1;}}
    for(int x:res) cout<<x<<" "; cout<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
