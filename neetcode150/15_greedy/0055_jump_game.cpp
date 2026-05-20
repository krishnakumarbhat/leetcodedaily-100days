#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> n={2,3,1,1,4};
    auto t=chrono::high_resolution_clock::now();
    int reach=0;
    for(int i=0;i<(int)n.size();i++){if(i>reach){cout<<"var1: false"<<endl;return 0;}reach=max(reach,i+n[i]);}
    cout<<"var1: true"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
