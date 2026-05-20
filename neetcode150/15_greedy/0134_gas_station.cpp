#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> gas={1,2,3,4,5},cost={3,4,5,1,2};
    auto t=chrono::high_resolution_clock::now();
    int total=0,tank=0,start=0;
    for(int i=0;i<(int)gas.size();i++){int d=gas[i]-cost[i];total+=d;tank+=d;if(tank<0){start=i+1;tank=0;}}
    cout<<"var1: "<<(total>=0?start:-1)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
