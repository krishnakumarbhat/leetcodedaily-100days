#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> n={2,3,1,1,4};
    auto t=chrono::high_resolution_clock::now();
    int jumps=0,cur=0,far=0;
    for(int i=0;i<(int)n.size()-1;i++){far=max(far,i+n[i]);if(i==cur){jumps++;cur=far;}}
    cout<<"var1: "<<jumps<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
