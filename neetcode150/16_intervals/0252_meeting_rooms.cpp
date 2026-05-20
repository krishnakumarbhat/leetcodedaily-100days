#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<pair<int,int>> iv={{0,30},{5,10},{15,20}};
    auto t=chrono::high_resolution_clock::now();
    sort(iv.begin(),iv.end());
    bool ok=true;
    for(int i=1;i<(int)iv.size();i++) if(iv[i].first<iv[i-1].second){ok=false;break;}
    cout<<"var1: "<<ok<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
